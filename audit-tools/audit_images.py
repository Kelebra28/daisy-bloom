#!/usr/bin/env python3
"""Auditoría reproducible y no destructiva de imágenes de Daisy Bloom."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import mimetypes
import os
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from PIL import Image


IMAGE_EXTENSIONS = {
    ".webp", ".avif", ".png", ".jpg", ".jpeg", ".svg", ".ico",
    ".gif", ".bmp", ".tif", ".tiff",
}
FORMAT_EXTENSIONS = {
    "WEBP": {".webp"}, "AVIF": {".avif"}, "PNG": {".png"},
    "JPEG": {".jpg", ".jpeg"}, "SVG": {".svg"}, "ICO": {".ico"},
    "GIF": {".gif"}, "BMP": {".bmp"}, "TIFF": {".tif", ".tiff"},
}
URL_RE = re.compile(
    r"(?:https?://[^\s\"'<>)]*)?(?:/|(?:\.\./|\./)*)assets/img/"
    r"[^\s\"'<>),]+\.(?:webp|avif|png|jpe?g|svg|ico|gif|bmp|tiff?)(?:[?#][^\s\"'<>)]*)?",
    re.I,
)
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)([^)'\"]+)\1\s*\)", re.I)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dhash(image: Image.Image) -> str:
    gray = image.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
    pixels = list(gray.getdata())
    bits = []
    for row in range(8):
        start = row * 9
        bits.extend(pixels[start + col] > pixels[start + col + 1] for col in range(8))
    return f"{sum((1 << index) for index, bit in enumerate(bits) if bit):016x}"


def hamming(left: str, right: str) -> int:
    return (int(left, 16) ^ int(right, 16)).bit_count()


def infer_function(name: str) -> str:
    lower = name.lower()
    if "logo" in lower or "emblema" in lower:
        return "logo/emblema"
    if "favicon" in lower or lower.endswith(".ico"):
        return "favicon"
    if "-og" in lower or "open-graph" in lower:
        return "Open Graph"
    if "hero" in lower:
        return "hero"
    if "cta" in lower or "whatsapp" in lower:
        return "CTA"
    if any(word in lower for word in ("decor", "fondo", "background")):
        return "decoración"
    return "contenido"


def parse_svg(path: Path) -> tuple[int | None, int | None, bool]:
    text = path.read_text(encoding="utf-8", errors="ignore")[:8192]
    width = re.search(r"\bwidth=[\"']([0-9.]+)", text, re.I)
    height = re.search(r"\bheight=[\"']([0-9.]+)", text, re.I)
    if width and height:
        return int(float(width.group(1))), int(float(height.group(1))), True
    viewbox = re.search(r"\bviewBox=[\"'][^\"']*?([0-9.]+)\s+([0-9.]+)[\"']", text, re.I)
    if viewbox:
        return int(float(viewbox.group(1))), int(float(viewbox.group(2))), True
    return None, None, True


def image_metadata(path: Path) -> dict:
    result = {
        "format_real": "DESCONOCIDO", "width": None, "height": None,
        "alpha": None, "dhash": None, "corrupt": False, "error": "",
    }
    try:
        if path.suffix.lower() == ".svg":
            width, height, alpha = parse_svg(path)
            result.update(format_real="SVG", width=width, height=height, alpha=alpha)
            return result
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            result["format_real"] = image.format or "DESCONOCIDO"
            result["width"], result["height"] = image.size
            result["alpha"] = image.mode in {"RGBA", "LA"} or "transparency" in image.info
            result["dhash"] = dhash(image)
    except Exception as exc:  # evidencia de archivo no decodificable
        result["corrupt"] = True
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def resolve_reference(raw: str, source: Path, root: Path) -> Path | None:
    cleaned = raw.strip().strip("'\"")
    if cleaned.startswith("data:"):
        return None
    parsed = urlparse(cleaned)
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc.lower() not in {"www.daisybloom.mx", "daisybloom.mx"}:
            return None
        cleaned = parsed.path
    else:
        cleaned = cleaned.split("?", 1)[0].split("#", 1)[0]
    cleaned = unquote(cleaned)
    if cleaned.startswith("/"):
        return (root / cleaned.lstrip("/")).resolve()
    return (source.parent / cleaned).resolve()


def line_kind(line: str) -> str:
    lower = line.lower()
    if "og:image" in lower:
        return "og:image"
    if "twitter:image" in lower:
        return "twitter:image"
    if "rel=\"icon" in lower or "rel='icon" in lower:
        return "favicon"
    if "preload" in lower and "image" in lower:
        return "preload"
    if "imageobject" in lower or "primaryimageofpage" in lower:
        return "JSON-LD"
    if "url(" in lower or "background-image" in lower:
        return "CSS"
    if "<img" in lower:
        return "img"
    return "referencia"


def extract_tag_attribute(fragment: str, attr: str) -> str:
    match = re.search(rf"\b{re.escape(attr)}\s*=\s*([\"'])(.*?)\1", fragment, re.I | re.S)
    return match.group(2).strip() if match else ""


def scan_references(root: Path, code_files: list[Path]) -> list[dict]:
    references: list[dict] = []
    for source in code_files:
        text = source.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        for number, line in enumerate(lines, 1):
            candidates = [match.group(0) for match in URL_RE.finditer(line)]
            candidates.extend(match.group(2) for match in CSS_URL_RE.finditer(line))
            seen_line = set()
            for raw in candidates:
                if raw in seen_line or not re.search(r"\.(?:webp|avif|png|jpe?g|svg|ico|gif|bmp|tiff?)(?:[?#].*)?$", raw, re.I):
                    continue
                seen_line.add(raw)
                resolved = resolve_reference(raw, source, root)
                if resolved is None:
                    continue
                references.append({
                    "raw": raw,
                    "resolved": str(resolved),
                    "source": source.relative_to(root).as_posix(),
                    "line": number,
                    "fragment": line.strip()[:500],
                    "kind": line_kind(line),
                    "alt": extract_tag_attribute(line, "alt") if "<img" in line.lower() else "",
                    "width": extract_tag_attribute(line, "width") if "<img" in line.lower() else "",
                    "height": extract_tag_attribute(line, "height") if "<img" in line.lower() else "",
                    "loading": extract_tag_attribute(line, "loading") if "<img" in line.lower() else "",
                    "fetchpriority": extract_tag_attribute(line, "fetchpriority") if "<img" in line.lower() else "",
                })
    return references


def audit(root: Path) -> dict:
    image_paths = sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    code_files = sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".html", ".css", ".js", ".json", ".webmanifest"}
        and "audit-tools" not in path.parts
    )
    references = scan_references(root, code_files)
    refs_by_path: dict[str, list[dict]] = defaultdict(list)
    for reference in references:
        refs_by_path[reference["resolved"]].append(reference)

    inventory = []
    for path in image_paths:
        rel = path.relative_to(root).as_posix()
        stat_result = path.stat()
        metadata = image_metadata(path)
        file_hash = sha256(path)
        refs = refs_by_path.get(str(path.resolve()), [])
        width, height = metadata["width"], metadata["height"]
        aspect = round(width / height, 4) if width and height else None
        expected_extensions = FORMAT_EXTENSIONS.get(metadata["format_real"], set())
        extension_matches = not expected_extensions or path.suffix.lower() in expected_extensions
        declared = sorted({
            f"{reference['width']}x{reference['height']}"
            for reference in refs if reference["width"] and reference["height"]
        })
        alts = sorted({reference["alt"] for reference in refs if reference["kind"] == "img"})
        pages = sorted({reference["source"] for reference in refs})
        ratio_mismatch = False
        if aspect:
            for item in declared:
                try:
                    dw, dh = (int(value) for value in item.split("x"))
                    if dh and abs((dw / dh) - aspect) / aspect > 0.04:
                        ratio_mismatch = True
                except ValueError:
                    pass
        function = infer_function(path.name)
        threshold = 500_000 if function in {"hero", "Open Graph"} else 300_000
        if function in {"logo/emblema", "favicon"}:
            threshold = 150_000
        convention = bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*\.(?:webp|avif|png|jpg|jpeg|svg|ico|gif)", path.name))
        issues = []
        if metadata["corrupt"]:
            issues.append("archivo no decodificable")
        if not extension_matches:
            issues.append("extensión no coincide con formato real")
        if not refs and rel.startswith("assets/img/"):
            issues.append("no utilizada")
        if stat_result.st_size > threshold and rel.startswith("assets/img/"):
            issues.append("peso alto")
        if ratio_mismatch:
            issues.append("relación declarada incompatible")
        if not convention and rel.startswith("assets/img/"):
            issues.append("nombre fuera de convención")
        if not issues:
            status = "correcto"
        elif "archivo no decodificable" in issues or "extensión no coincide con formato real" in issues:
            status = "sustituir"
        elif "peso alto" in issues:
            status = "optimizar"
        else:
            status = "revisar"
        inventory.append({
            "archivo": path.name,
            "ruta": rel,
            "ambito": "producción" if rel.startswith("assets/img/") else "documentación/legado",
            "extension": path.suffix.lower(),
            "formato_real": metadata["format_real"],
            "bytes": stat_result.st_size,
            "kilobytes": round(stat_result.st_size / 1024, 2),
            "ancho": width or "",
            "alto": height or "",
            "relacion_aspecto": aspect or "",
            "transparencia": "sí" if metadata["alpha"] else "no" if metadata["alpha"] is not None else "no verificable",
            "funcion": function,
            "utilizada": "sí" if refs else "no",
            "referencias": len(refs),
            "paginas_uso": " | ".join(pages),
            "dimension_declarada": " | ".join(declared),
            "alt": " | ".join(alts),
            "sha256": file_hash,
            "dhash": metadata["dhash"] or "",
            "extension_coincide": "sí" if extension_matches else "no",
            "nombre_convencion": "sí" if convention else "no",
            "estado": status,
            "recomendacion": "; ".join(issues) if issues else "conservar",
            "error": metadata["error"],
        })

    physical_by_resolved = {str((root / row["ruta"]).resolve()): row for row in inventory}
    lower_lookup = defaultdict(list)
    for resolved, row in physical_by_resolved.items():
        lower_lookup[resolved.lower()].append(row["ruta"])
    missing = []
    for reference in references:
        if reference["resolved"] in physical_by_resolved:
            continue
        case_candidates = lower_lookup.get(reference["resolved"].lower(), [])
        item = dict(reference)
        item["case_candidates"] = case_candidates
        item["expected_relative"] = os.path.relpath(reference["resolved"], root)
        missing.append(item)

    exact_groups = []
    hashes = defaultdict(list)
    for row in inventory:
        hashes[row["sha256"]].append(row["ruta"])
    for digest, paths in hashes.items():
        if len(paths) > 1:
            exact_groups.append({"sha256": digest, "paths": sorted(paths)})

    production = [row for row in inventory if row["ambito"] == "producción"]
    similar_pairs = []
    for index, left in enumerate(production):
        if not left["dhash"]:
            continue
        for right in production[index + 1:]:
            if not right["dhash"] or left["sha256"] == right["sha256"]:
                continue
            distance = hamming(left["dhash"], right["dhash"])
            if distance <= 3:
                similar_pairs.append({"left": left["ruta"], "right": right["ruta"], "distance": distance})

    img_refs = [reference for reference in references if reference["kind"] == "img"]
    summary = {
        "physical_total": len(inventory),
        "production_images": len(production),
        "documentation_images": len(inventory) - len(production),
        "reference_occurrences": len(references),
        "referenced_unique": len({reference["resolved"] for reference in references}),
        "missing_occurrences": len(missing),
        "missing_unique": len({item["resolved"] for item in missing}),
        "unused_production": sum(row["utilizada"] == "no" for row in production),
        "exact_duplicate_groups": len(exact_groups),
        "exact_duplicate_files": sum(len(group["paths"]) for group in exact_groups),
        "perceptual_similar_pairs": len(similar_pairs),
        "heavy_over_500kb": sum(row["bytes"] > 500_000 for row in production),
        "heavy_over_1mb": sum(row["bytes"] > 1_000_000 for row in production),
        "format_mismatches": sum(row["extension_coincide"] == "no" for row in inventory),
        "corrupt": sum(bool(row["error"]) for row in inventory),
        "ratio_mismatches": sum("relación declarada incompatible" in row["recomendacion"] for row in production),
        "img_tags": len(img_refs),
        "img_missing_alt": sum(reference["alt"] == "" for reference in img_refs),
        "img_missing_dimensions": sum(not reference["width"] or not reference["height"] for reference in img_refs),
        "img_lazy": sum(reference["loading"] == "lazy" for reference in img_refs),
        "img_eager_or_default": sum(reference["loading"] != "lazy" for reference in img_refs),
        "img_high_priority": sum(reference["fetchpriority"] == "high" for reference in img_refs),
    }
    return {
        "root": str(root), "summary": summary, "inventory": inventory,
        "references": references, "missing": missing,
        "exact_duplicates": exact_groups, "similar_pairs": similar_pairs,
    }


def write_csv(data: dict, output: Path) -> None:
    fields = [
        "archivo", "ruta", "ambito", "extension", "formato_real", "bytes",
        "kilobytes", "ancho", "alto", "relacion_aspecto", "transparencia",
        "dimension_declarada", "paginas_uso", "referencias", "alt", "funcion",
        "utilizada", "sha256", "dhash", "extension_coincide", "nombre_convencion",
        "estado", "recomendacion", "error",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in data["inventory"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    data = audit(root)
    write_csv(data, args.csv)
    args.json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
