# Plan de cierre Daisy Bloom

El sitio permanece `BLOQUEADO POR ELEMENTOS CRÍTICOS`. Las fases deben ejecutarse en este orden.

Estado técnico vigente: **66/150 imágenes integradas (44.0%)**, **84 faltantes**, **121 apariciones rotas**, **8/22 páginas completas** y **14/22 afectadas**.

| Orden | Actividad | Archivos/área | Dependencia | Criterio de aceptación | Riesgo |
| ---: | --- | --- | --- | --- | --- |
| 1 | Congelar versión oficial | `daisy-bloom-public_html/` | Ninguna | Fuente identificada y respaldada | Trabajar sobre copias antiguas |
| 2 | Completar documentación | `docs/` | Paso 1 | Seis documentos reconciliados | Estados contradictorios |
| 3 | Producir imágenes P0 | `assets/img/` | Briefs aprobados | 23 P0 faltantes generadas | Incoherencia visual |
| 4 | Integrar y validar P0 | 14 páginas afectadas | Paso 3 | Hero/OG/schema sin 404 | Primer viewport roto |
| 5 | Producir imágenes P1 | `assets/img/` | P0 validado | 35 P1 faltantes generadas | Retrabajo de modelos |
| 6 | Integrar y validar P1 | Landings afectadas | Paso 5 | Recorte y responsive aprobados | Layout inestable |
| 7 | Producir imágenes P2 | `assets/img/` | Sistema visual estable | 26 P2 faltantes generadas | Variación excesiva |
| 8 | Integrar y validar P2 | Landings afectadas | Paso 7 | 150/150 presentes | Recursos residuales 404 |
| 9 | Revisar navegación de Vida Natural | Menús y enlaces relacionados | Imágenes cerradas | Cuatro pilares visibles consistentemente | Descubrimiento desigual |
| 10 | Crear página 404 | `/404.html` | Navegación aprobada | 404 útil y coherente | URLs erróneas sin salida |
| 11 | Añadir favicon alternativo | Identidad global | Asset aprobado | ICO/PNG probado | Compatibilidad parcial |
| 12 | QA responsive | 22 páginas | 150 imágenes integradas | 320/375/768/1024/escritorio aprobados | Desbordamientos |
| 13 | Accesibilidad | 22 páginas | Paso 12 | Teclado, foco, contraste, alt y ARIA revisados | Barreras de uso |
| 14 | Lighthouse | Sitio completo | Paso 13 | Resultados registrados y bloqueos corregidos | Rendimiento bajo |
| 15 | Validar HTML y schema | 22 páginas | Paso 14 | Sin errores críticos ni imágenes ausentes | Indexación defectuosa |
| 16 | Probar WhatsApp móvil | 22 páginas | Dominio/staging accesible | Número y mensaje correctos | Conversión rota |
| 17 | Limpiar macOS/copias | Paquete de despliegue | Todo aprobado | Sin `.DS_Store`, `__MACOSX` ni copias | Contaminación del paquete |
| 18 | Crear ZIP limpio | Entregable Hostinger | Paso 17 | ZIP contiene solo fuente oficial | Publicar versión errónea |
| 19 | Publicar en Hostinger | `public_html` | ZIP aprobado | 22 URLs con HTTP 200 | Fallos de servidor |
| 20 | QA posterior | Dominio público | Paso 19 | URLs, OG, sitemap, schema, WhatsApp y Search Console verificados | Fallos invisibles en local |

## Puerta de publicación

No avanzar al paso 18 hasta cumplir simultáneamente: 150/150 imágenes físicas, 0 recursos locales 404, navegación aprobada, QA responsive documentado, WhatsApp móvil correcto, schema válido y ausencia de datos sensibles.
