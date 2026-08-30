#!/usr/bin/env python3
"""Genera el informe Markdown reproducible a partir de audit-data.json."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "audit-tools/audit-data.json").read_text(encoding="utf-8"))
INVENTORY = DATA["inventory"]
REFERENCES = DATA["references"]
MISSING = DATA["missing"]
SUMMARY = DATA["summary"]


def esc(value: object) -> str:
    return str(value if value not in (None, "") else "—").replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out.extend("| " + " | ".join(esc(cell) for cell in row) + " |" for row in rows)
    return "\n".join(out)


def page_label(path: str) -> str:
    if path == "index.html":
        return "Inicio"
    return path.removesuffix("/index.html").replace("-", " ").title()


def main() -> None:
    production = [row for row in INVENTORY if row["ambito"] == "producción"]
    documentation = [row for row in INVENTORY if row["ambito"] != "producción"]
    missing_unique = {row["resolved"]: row for row in MISSING}
    missing_by_page: dict[str, set[str]] = defaultdict(set)
    refs_by_page: dict[str, list[dict]] = defaultdict(list)
    for row in REFERENCES:
        refs_by_page[row["source"]].append(row)
    for row in MISSING:
        missing_by_page[row["source"]].add(row["resolved"])

    physical_by_stem: dict[str, list[dict]] = defaultdict(list)
    for row in production:
        physical_by_stem[PurePosixPath(row["ruta"]).stem].append(row)

    missing_rows = []
    missing_with_source = 0
    missing_without_source = 0
    for absolute, row in sorted(missing_unique.items(), key=lambda item: item[1]["raw"]):
        stem = PurePosixPath(row["raw"]).stem
        candidates = physical_by_stem.get(stem, [])
        if candidates:
            missing_with_source += 1
            candidate = ", ".join(item["ruta"] for item in candidates)
            action = "Generar WebP con el nombre esperado desde la fuente física; validar encuadre y compresión."
        else:
            missing_without_source += 1
            normalized_candidates = [
                item for item in production
                if PurePosixPath(item["ruta"]).stem.rstrip(".") == stem.rstrip(".")
            ]
            if normalized_candidates:
                candidate = "Posible error de nombre: " + ", ".join(item["ruta"] for item in normalized_candidates)
                action = "Aprobar el renombrado/mapeo y generar el WebP final."
            elif stem == "daisy-bloom-daisy-guia-maquillaje-seytu":
                candidate = "Alternativa semántica probable: assets/img/daisy-bloom-daisy-guia-maquillaje-natural.png"
                action = "Validar visualmente la equivalencia, aprobar el mapeo y generar el WebP final."
            else:
                candidate = "No hay coincidencia exacta por nombre base"
                action = "Resolver mapeo semántico o crear/regenerar el recurso antes de publicar."
        uses = sorted({m["source"] for m in MISSING if m["resolved"] == absolute})
        kinds = sorted({m["kind"] for m in MISSING if m["resolved"] == absolute})
        occurrences = sum(m["resolved"] == absolute for m in MISSING)
        missing_rows.append([row["raw"], occurrences, ", ".join(kinds), "<br>".join(uses), candidate, action])

    unused = [row for row in production if row["utilizada"] == "no"]
    unused_rows = []
    missing_stems = {PurePosixPath(row["raw"]).stem for row in MISSING}
    for row in unused:
        is_source = PurePosixPath(row["ruta"]).stem in missing_stems
        classification = "Fuente de recuperación para ruta WebP ausente" if is_source else "Sin referencia ni correspondencia exacta con faltante"
        recommendation = "Conservar; convertir y verificar" if is_source else "Revisión humana; no eliminar todavía"
        unused_rows.append([row["ruta"], row["bytes"], f'{row["ancho"]}×{row["alto"]}', row["formato_real"], classification, recommendation])

    page_rows = []
    html_pages = sorted(path for path in refs_by_page if path.endswith(".html"))
    for page in html_pages:
        refs = refs_by_page[page]
        unique_refs = {row["resolved"] for row in refs}
        misses = missing_by_page.get(page, set())
        missing_names = sorted(Path(path).name for path in misses)
        og_broken = any(row["source"] == page and row["kind"] in {"og:image", "twitter:image"} for row in MISSING)
        img_broken = sum(1 for row in MISSING if row["source"] == page and row["kind"] == "img")
        status = "NO PUBLICAR" if misses else "Apta tras QA visual y rendimiento"
        page_rows.append([
            page_label(page), page, len(unique_refs), len(misses), img_broken,
            "sí" if og_broken else "no", status,
            "<br>".join(missing_names) if missing_names else "—",
        ])

    master_rows = []
    for row in production:
        master_rows.append([
            row["archivo"], row["ruta"], row["formato_real"], row["bytes"],
            f'{row["ancho"]}×{row["alto"]}', row["relacion_aspecto"], row["transparencia"],
            row["funcion"], row["utilizada"], row["paginas_uso"], row["dimension_declarada"],
            row["alt"], row["estado"], row["recomendacion"], row["sha256"],
        ])

    duplicate_rows = []
    for group in DATA["exact_duplicates"]:
        duplicate_rows.append([group["sha256"], "<br>".join(group["paths"]), "Duplicado binario exacto", "Conservar una copia documental si ambas no son necesarias"])

    ratio_rows = [
        [row["ruta"], f'{row["ancho"]}×{row["alto"]}', row["dimension_declarada"], "Revisar recorte CSS y declarar proporción intrínseca real"]
        for row in production if "relación declarada incompatible" in row["recomendacion"]
    ]
    naming_rows = [
        [row["ruta"], "Nombre fuera de convención", "Corregir doble punto mediante migración controlada de ruta"]
        for row in production if row["nombre_convencion"] == "no"
    ]

    total_prod = sum(row["bytes"] for row in production)
    total_used = sum(row["bytes"] for row in production if row["utilizada"] == "sí")
    total_unused = sum(row["bytes"] for row in production if row["utilizada"] == "no")
    formats = Counter(row["formato_real"] for row in production)
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    sections: list[str] = []
    sections.append("# AUDITORÍA INTEGRAL DE IMÁGENES — DAISY BLOOM")
    sections.append(f"""**Fecha de auditoría:** {now}  
**Ruta analizada:** `{ROOT}`  
**Modalidad:** solo lectura sobre archivos de producción; los únicos archivos creados son este informe, el CSV y utilidades dentro de `audit-tools/`.  
**Alcance:** 22 documentos HTML, 148 imágenes de producción y 53 capturas/recursos documentales. No se encontraron CSS ni JavaScript externos; las referencias relevantes están embebidas en HTML.

## 1. Dictamen ejecutivo

**Dictamen: NO PUBLICAR en el estado actual. Puntuación: 46/100.**

La identidad visual es cálida y razonablemente coherente, pero la integración técnica está incompleta: 84 rutas únicas apuntan a archivos inexistentes y afectan 14 de 22 landings. En 73 casos existe un PNG fuente con el mismo nombre base, por lo que la reparación principal consiste en generar los WebP esperados, no en rediseñar todo el universo visual. Once rutas requieren mapeo o creación específica.

| Categoría | Peso | Resultado | Motivo principal |
|---|---:|---:|---|
| Integridad y cobertura | 30 | 8 | 84 recursos únicos ausentes; 121 ocurrencias rotas |
| Rendimiento | 20 | 8 | 79 PNG superan 1 MB; repositorio de producción pesa {total_prod:,} bytes |
| SEO social y semántico | 15 | 6 | 12 páginas tienen `og:image` y `twitter:image` rotos |
| Accesibilidad | 15 | 13 | Todas las imágenes tienen dimensiones; 22 `alt` vacíos corresponden al emblema, aunque 10 usos deben explicitar mejor su carácter decorativo |
| Marca y calidad visual | 15 | 8 | Paleta coherente, pero Daisy no mantiene identidad facial consistente y hay repetición de escenas |
| Gobernanza de activos | 5 | 3 | 82 archivos no referenciados, tres nombres con doble punto y dos duplicados documentales exactos |
| **Total** | **100** | **46** | **Bloqueo P0 por integridad** |

## 2. Resumen cuantitativo

| Indicador | Resultado |
|---|---:|
| Imágenes físicas totales | {SUMMARY['physical_total']} |
| Imágenes en `assets/img` | {SUMMARY['production_images']} |
| Capturas/recursos en documentación | {SUMMARY['documentation_images']} |
| PNG / WebP en producción | {formats.get('PNG', 0)} / {formats.get('WEBP', 0)} |
| Peso total de producción | {total_prod:,} bytes |
| Peso de recursos actualmente referenciados | {total_used:,} bytes |
| Peso de recursos no referenciados | {total_unused:,} bytes |
| Ocurrencias de referencias | {SUMMARY['reference_occurrences']} |
| Rutas referenciadas únicas | {SUMMARY['referenced_unique']} |
| Ocurrencias rotas / rutas rotas únicas | {SUMMARY['missing_occurrences']} / {SUMMARY['missing_unique']} |
| Rutas faltantes con fuente física por nombre base | {missing_with_source} |
| Rutas faltantes sin fuente exacta por nombre base | {missing_without_source} |
| Imágenes de producción no referenciadas | {SUMMARY['unused_production']} |
| Imágenes mayores de 1 MB | {SUMMARY['heavy_over_1mb']} |
| Imágenes con proporción declarada incompatible | {SUMMARY['ratio_mismatches']} |
| Etiquetas `<img>` / lazy / alta prioridad | {SUMMARY['img_tags']} / {SUMMARY['img_lazy']} / {SUMMARY['img_high_priority']} |
| Archivos corruptos | {SUMMARY['corrupt']} |

## 3. Hallazgos prioritarios

### P0 — Bloquean publicación

1. **84 rutas únicas inexistentes.** Producen 121 referencias rotas entre imágenes visibles, preload, JSON-LD/referencias y metadatos sociales.
2. **14 de 22 landings están afectadas.** Las ocho sin rutas faltantes también requieren QA final, pero no presentan el bloqueo técnico principal.
3. **12 páginas carecen de imagen social efectiva.** La misma ausencia afecta Open Graph y Twitter Cards.

### P1 — Corregir antes del QA de aceptación

1. **79 PNG pesan más de 1 MB.** En conjunto, los 82 no referenciados ocupan {total_unused:,} bytes; 73 son fuentes útiles y no deben borrarse antes de convertirlas.
2. **Continuidad de Daisy.** Las piezas llamadas `daisy-guia-*` muestran distintas protagonistas (cabello, rasgos, edad aparente y tono de piel). Si Daisy es un personaje único, la continuidad visual no está resuelta.
3. **27 discrepancias de proporción intrínseca.** El HTML declara relaciones diferentes de las imágenes. `object-fit` puede hacer el recorte intencional, pero debe comprobarse en móvil/escritorio para evitar CLS, deformación o cortes de rostro/manos.
4. **Tres nombres con doble punto.** Son señales de integración frágil y uno corresponde a un OG redundante.

### P2 — Refinamiento

1. La paleta crema/rosa/verde, luz suave y atmósfera doméstica son coherentes, pero abundan cocina, taza/vaso, libreta y blusas claras; la repetición reduce diferenciación entre landings.
2. La apariencia muy pulida y homogénea puede percibirse como banco de imágenes o generación sintética. No se observaron defectos anatómicos graves en las hojas de contacto, pero la validación al 100 % debe incluir manos, etiquetas de producto y textos a resolución completa.
3. En `bienestar-femenino-40`, la representación es plausible, aunque algunas modelos pueden percibirse menores de 40; Daisy tampoco domina siempre la jerarquía visual del grupo.
""")

    sections.append("## 4. Inventario maestro de imágenes de producción\n\nEl CSV adjunto contiene además los 53 recursos documentales. Esta tabla enumera individualmente los 148 activos de `assets/img`.\n\n" + table(
        ["Archivo", "Ruta", "Formato", "Bytes", "Dimensiones", "Ratio", "Alpha", "Función", "Usada", "Páginas", "Declaración", "Alt", "Estado", "Recomendación", "SHA-256"], master_rows
    ))

    sections.append("## 5. Auditoría por landing\n\n" + table(
        ["Landing", "Ruta", "Recursos únicos", "Faltantes únicos", "`<img>` rotos", "OG/Twitter roto", "Dictamen", "Archivos faltantes"], page_rows
    ))

    sections.append("## 6. Imágenes faltantes y referencias rotas\n\n" + table(
        ["Ruta solicitada", "Ocurrencias", "Contextos", "Páginas", "Fuente candidata", "Acción"], missing_rows
    ))

    sections.append("## 7. Imágenes no utilizadas\n\n**No deben eliminarse en bloque.** La mayoría son PNG fuente para WebP faltantes. Tras separar 73 fuentes directas y tres candidatos de mapeo/renombrado, quedan seis posibles obsoletos que requieren una decisión humana.\n\n" + table(
        ["Ruta", "Bytes", "Dimensiones", "Formato", "Clasificación", "Recomendación"], unused_rows
    ))

    sections.append("## 8. Duplicados, similitud y nomenclatura\n\n### Duplicados binarios exactos\n\n" + table(
        ["SHA-256", "Rutas", "Tipo", "Acción"], duplicate_rows
    ) + "\n\nLos dos grupos están dentro de documentación, no en `assets/img`. El hash perceptual dHash no detectó pares de producción a distancia ≤3; esta prueba no sustituye una comparación semántica.\n\n### Nombres fuera de convención\n\n" + table(
        ["Ruta", "Problema", "Acción"], naming_rows
    ))

    sections.append("## 9. Rendimiento, responsive y carga\n\n" + f"""- Hay {SUMMARY['heavy_over_1mb']} archivos de producción por encima de 1 MB; todos son PNG.
- Los 69 WebP existentes tienen pesos moderados, pero gran parte del sitio intenta cargar WebP que aún no existen.
- Las 197 etiquetas `<img>` incluyen `width` y `height`; esto es favorable para estabilidad de layout.
- 131 imágenes usan `loading=lazy`. Hay 66 eager/por defecto y 52 con `fetchpriority=high`; la prioridad alta aparece también en emblemas repetidos y debe reservarse para el LCP real.
- No se hallaron `srcset` ni `<picture>` en el inventario de referencias. Para héroes y piezas de contenido conviene generar al menos variantes móvil/escritorio y AVIF/WebP con fallback si el diseño lo exige.
- Los OG correctos miden 1200×630 en varias secciones; otros recursos fuente usan 1731×909 o 1728×910. Normalizar la salida social final a 1200×630 evita recortes inconsistentes.

### Proporciones que deben verificarse visualmente

""" + table(["Ruta", "Real", "Declarada", "Acción"], ratio_rows))

    sections.append("""## 10. Plan de corrección priorizado

### Bloque 1 — Integridad P0

1. Congelar las 84 rutas objetivo y aprobar el mapa fuente→destino.
2. Generar los 73 WebP desde PNG homónimos, manteniendo exactamente el nombre esperado por el HTML.
3. Resolver las 11 rutas sin homónimo: dos provienen de nombres con doble punto, una tiene alternativa semántica probable y ocho requieren selección o creación específica.
4. Repetir rastreo hasta obtener **0 referencias rotas**, incluidos preload, OG, Twitter y datos estructurados.

### Bloque 2 — Rendimiento y responsive P1

5. Optimizar las 79 fuentes PNG y definir presupuesto: hero ≤250 KB, contenido/CTA ≤180 KB y OG ≤150 KB como metas iniciales, sujetas a calidad visual.
6. Crear variantes responsive donde el ancho real exceda claramente el render y validar `sizes/srcset`.
7. Corregir las 27 declaraciones de proporción o documentar el recorte intencional; probar 360, 390, 768, 1024 y 1440 px.
8. Limitar `fetchpriority=high` al LCP de cada página.

### Bloque 3 — Marca y limpieza P1/P2

9. Aprobar una ficha de identidad visual de Daisy y sustituir piezas que no representen a la misma protagonista cuando el nombre/relato la identifique explícitamente.
10. Revisar las siete imágenes sin uso ni correspondencia; archivar antes de cualquier eliminación.
11. Corregir los tres nombres con doble punto mediante migración controlada y volver a rastrear referencias.
12. Ejecutar QA visual al 100 %: rostro, manos, textos/etiquetas, recortes, contraste y relevancia semántica.

### Estimación operativa de imágenes

| Acción | Cantidad estimada | Observación |
|---|---:|---|
| Crear o regenerar | 8 | Rutas sin fuente exacta ni sustituto evidente |
| Renombrar/mapear | 3 | Dos dobles puntos y una guía de maquillaje con alternativa probable |
| Optimizar/convertir | 79 | PNG de producción mayores de 1 MB; incluye las fuentes de recuperación |
| Sustituir en referencias | 0–84 | Cero si se generan exactamente los nombres esperados; hasta 84 rutas si se cambia la nomenclatura |
| Eliminar más adelante | Hasta 6 candidatas | Solo tras revisión humana, respaldo y verificación de cero uso; los 73 PNG fuente no se eliminan antes de aprobar los WebP |

**Recomendación de ejecución:** por bloques controlados, no en una sola operación. Primero Bienestar (36 faltantes), luego Crece (37), después Belleza (8) y Organización (3); cerrar cada bloque con rastreo y QA antes del siguiente.

## 11. Checklist de publicación y criterios de aprobación

- [ ] Cero rutas de imagen faltantes en HTML, CSS inline, JS inline, preload, JSON-LD, OG y Twitter.
- [ ] Las 22 landings cargan sin 404 de imágenes.
- [ ] Cada landing tiene hero, contenido, guía/CTA y recurso social según diseño.
- [ ] OG/Twitter válidos, accesibles y preferentemente 1200×630.
- [ ] Un solo recurso `fetchpriority=high` por página salvo justificación medida.
- [ ] Todas las imágenes informativas tienen `alt` específico; las decorativas usan `alt=""` y se ocultan correctamente a tecnología asistiva.
- [ ] Las dimensiones intrínsecas o `aspect-ratio` coinciden con el comportamiento responsive.
- [ ] Presupuesto de peso aprobado y sin PNG >1 MB servido al usuario.
- [ ] Daisy mantiene identidad visual aprobada en todas las piezas que la nombran.
- [ ] Revisión humana a tamaño completo de manos, rostros, ojos, producto, envases y texto visible.
- [ ] Cero duplicados o nombres ambiguos en producción, salvo excepción documentada.
- [ ] Prueba móvil/escritorio y Lighthouse/WebPageTest ejecutada en un servidor local o staging accesible.

### Evidencia, método y limitaciones

**Herramientas:** script reproducible `audit-tools/audit_images.py`, Pillow para metadatos y decodificación, SHA-256 para duplicados exactos, dHash para similitud aproximada, análisis de referencias por HTML/CSS/JS/JSON y hojas de contacto para revisión visual.

**Comandos reproducibles:**

```sh
python3 audit-tools/audit_images.py . \\
  --csv inventario-imagenes-daisy-bloom.csv \\
  --json audit-tools/audit-data.json
```

**Limitaciones:** el navegador integrado no pudo acceder al servidor local por la política de navegación de la sesión; por ello la revisión visual se realizó sobre los archivos físicos y hojas de contacto, no sobre el layout renderizado. El análisis sintáctico por expresiones regulares cubre las referencias estáticas presentes, pero una URL construida dinámicamente en tiempo de ejecución requeriría instrumentación del navegador. La evaluación de edad aparente, identidad y apariencia sintética es cualitativa y requiere aprobación humana de marca.

### Cierre solicitado

**Estado para publicación:** no listo.

**Cinco problemas principales:** 84 rutas inexistentes; 14 landings afectadas; 12 imágenes sociales rotas; 79 PNG superiores a 1 MB; continuidad visual inconsistente de Daisy.

**Orden exacto:** mapa de activos → generar/migrar WebP → cero referencias rotas → optimización responsive → continuidad de marca → QA visual y técnico → publicación.

La reparación debe ejecutarse **por landing/bloques controlados**, con verificación entre bloques. No se recomienda una sustitución masiva única.
""")

    output = ROOT / "AUDITORIA_IMAGENES_DAISY_BLOOM.md"
    output.write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
