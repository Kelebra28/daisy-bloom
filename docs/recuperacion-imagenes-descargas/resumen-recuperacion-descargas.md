# Resumen de recuperación desde Descargas

## Dictamen general

`RECUPERACIÓN PARCIAL CON CORRESPONDENCIAS FUERTES`.

Se localizaron candidatos para **28 de las 112 imágenes faltantes**: 27 correspondencias confirmables en PNG y un WebP exacto clasificado como candidata fuerte hasta validar su recorte. Permanecen **84** imágenes sin localizar.

## Confirmación de acceso y alcance

Se obtuvo acceso de solo lectura a `/Users/danielfuentes/Downloads/` y se revisaron sus 8,889 subcarpetas. La comparación utilizó el inventario oficial, el plan de producción, `assets/img/README.md` y las referencias de los 22 HTML.

Los conteos maestros quedaron confirmados: **150 imágenes únicas**, **38 integradas**, **112 faltantes**, distribuidas en **30 P0**, **41 P1** y **41 P2**.

## Conteos finales

| Métrica | Total |
| --- | ---: |
| Archivos revisados en Descargas | 57,539 |
| Subcarpetas revisadas | 8,889 |
| Imágenes analizadas | 662 |
| PNG analizados | 484 |
| Imágenes probablemente relacionadas con Daisy Bloom | 39 |
| PNG probablemente relacionados | 38 |
| Archivos con nombre exacto para faltantes | 29 archivos / 28 IDs |
| IDs con nombre exacto en PNG | 27 |
| Candidata fuerte con mismo nombre/formato | 1 |
| Imágenes relevantes con nombre genérico | 7 |
| Duplicados exactos relevantes | 0 |
| Duplicados visuales relevantes | 6 |
| Grupos de duplicados/variantes | 9 |
| Candidatas posibles adicionales | 1 variante; no suma recuperación |
| Imágenes no encontradas | 84 |
| Recuperables potenciales | 28 |
| Producción provisional pendiente | 84 |

En el conjunto completo existen 54 grupos de SHA duplicado, equivalentes a 124 copias adicionales. Ninguno pertenece a los candidatos Daisy Bloom relevantes.

## Metodología

1. Confirmación de los conteos actuales del inventario.
2. Recorrido recursivo de nombres, extensiones, rutas y fechas.
3. Comparación exacta y normalizada de nombres.
4. Asociación por palabras clave y contexto de landing.
5. SHA-256 para duplicados exactos.
6. dHash de 256 bits para versiones convertidas o redimensionadas.
7. Revisión visual de candidatos genéricos y variantes.
8. Registro de dimensión, peso y fecha sin modificar originales.

## Correspondencias confirmables

- **27 IDs** tienen PNG de nombre base exacto y escena coherente.
- Todos pertenecen a Vida Natural Bloom.
- `DB-IMG-070` tiene dos PNG diferentes para el mismo destino. Debe revisarse primero la versión más reciente: `/Users/danielfuentes/Downloads/daisy-bloom-descanso-calma-equilibrio-og.png`.
- Los archivos conservan dimensiones generativas —1731×909, 1122×1402, 1254×1254 o similares— y todavía requieren conversión y recorte en otra fase.

## Candidata fuerte

`DB-IMG-038` corresponde a:

`/Users/danielfuentes/Downloads/daisy-bloom-cta-hidratacion-alimentacion-consciente.webp`

Tiene nombre y formato exactos, pero mide 1024×1024 frente a 1400×900 esperado. Confianza: **99%**; pendiente de revisión humana del encuadre.

## Archivos genéricos

Seis PNG UUID descargados el 6 de junio son fuentes visuales de imágenes que ya están integradas: OG y hero de Vida Natural madre, rutas, hábitos, Daisy guía y CTA. Se documentan como duplicados visuales, no como recuperación de las 112 faltantes.

La captura `/Users/danielfuentes/Downloads/73392465-97b1-4b3e-a21e-715206487b60.png` muestra una propuesta completa del sitio; se conserva como referencia histórica, pero no es un asset editorial aislado.

## Variantes

- **V1:** dos escenas para `daisy-bloom-descanso-calma-equilibrio-og.webp`; revisar primero la más reciente.
- **V2:** versiones de alimentación consciente con una y dos mujeres; el nombre exacto es la candidata principal.
- **V3:** `rutina-semanal-realista` frente a `sostener-estilo-vida-claro`; priorizar el nombre exacto.
- **D1–D6:** fuentes PNG frente a WebP ya integrados.

## Conciliación

```text
112 imágenes técnicamente faltantes
– 27 correspondencias confirmables
= 85 sin confirmación definitiva
```

```text
112 imágenes técnicamente faltantes
– 27 correspondencias confirmables
– 1 candidata fuerte pendiente de aprobación
= 84 posible faltante después de revisión humana
```

## Hojas de contacto

- `contact-sheets/vida-natural-01.jpg`
- `contact-sheets/vida-natural-02.jpg`
- `contact-sheets/sin-clasificacion-01.jpg`
- `contact-sheets/sin-clasificacion-02.jpg`
- `contact-sheets/duplicados-variantes-01.jpg`

No se generaron hojas vacías para Bienestar, Belleza o Crece porque no se localizaron candidatos con confianza mínima de 60% para esos pilares.

## Lista priorizada para revisión humana

1. Hero de Hábitos, Descanso, Hidratación y Organización.
2. OG de Hábitos, Descanso —dos variantes— e Hidratación.
3. CTA de Hábitos y Descanso, seguido por la candidata fuerte de Hidratación.
4. Daisy como guía de Hábitos, Descanso e Hidratación.
5. Editoriales de las cuatro hijas de Vida Natural.
6. Variantes V1–V3.
7. Genéricos G-001–G-007 como referencia, no como recuperaciones.
8. Las 84 imágenes no encontradas, empezando por las P0.

## Próxima acción recomendada

Revisar visualmente los 27 PNG exactos y `DB-IMG-038`, registrar aprobación o rechazo humano y solo después autorizar una fase separada de copia, conversión, redimensionamiento e integración.

## Confirmación de restricciones

No se modificó HTML, CSS, JavaScript, inventario maestro ni imagen original. No se movieron, renombraron, convirtieron o copiaron imágenes hacia `assets/img/`. Solo se generaron matrices, informes y miniaturas de auditoría dentro de `docs/recuperacion-imagenes-descargas/`.
