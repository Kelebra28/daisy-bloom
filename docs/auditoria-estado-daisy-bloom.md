# Auditoría de estado Daisy Bloom

**Fecha de corte:** 19 de junio de 2026  
**Fuente oficial evaluada:** `daisy-bloom-public_html/`  
**Dictamen:** `BLOQUEADO POR ELEMENTOS CRÍTICOS`

## Resumen ejecutivo

| Indicador | Resultado | Base verificable |
| --- | ---: | --- |
| Avance estructural | 100% | 22 de 22 rutas esperadas |
| Páginas creadas | 100% | 22 archivos `index.html` |
| Contenido sustantivo | 100% | 22 páginas con H1, secciones, CTA y FAQ |
| Imágenes integradas | 44.0% | 66 de 150 imágenes únicas |
| SEO técnico | 92.4% | Metadatos completos; OG físicas incompletas |
| Revisión técnica | 90% | Falta QA visual interactivo |
| Preparación de publicación | 65% | Imágenes y QA bloquean el cierre |
| Avance general | 84.5% | Promedio simple de los siete indicadores anteriores |

- Páginas esperadas y encontradas: **22/22**.
- Imágenes únicas referenciadas: **150**.
- Imágenes existentes físicamente con coincidencia exacta: **66**.
- Imágenes faltantes: **84**.
- Apariciones de recursos gráficos inexistentes: **121**.
- Páginas completas técnicamente: **8**; páginas afectadas: **14**.
- Hipervínculos internos rotos: **0**.
- Páginas completamente verificadas: **0**, porque el QA responsive visual sigue pendiente.

## Estado por área

### Arquitectura y contenido

Las 22 rutas aprobadas existen físicamente y contienen contenido coherente. No hay landings huérfanas ni páginas públicas vacías. Inicio y los cuatro pilares están presentes con todas sus hijas.

### Imágenes

El bloqueo principal está en `assets/img/`: 84 rutas documentadas y utilizadas por el HTML no tienen archivo físico. Las ausencias incluyen hero, Open Graph, CTA, imágenes de Daisy, cards y contenido editorial. Inicio, Belleza madre, Cuidado Facial, Cuidado Corporal, Vida Natural madre, Descanso, Hábitos e Hidratación no tienen imágenes faltantes; las otras 14 páginas sí.

### Navegación

No se localizaron enlaces internos hacia páginas inexistentes. Los enlaces `href="#"` pertenecen exclusivamente a WhatsApp y son convertidos por JavaScript. Las hijas de Vida Natural no incluyen consistentemente `Crece con Daisy Bloom` en el menú; `Hábitos Saludables` también presenta menos enlaces hermanos que el resto.

### SEO y schema

Las 22 páginas tienen title, description, canonical, Open Graph, Twitter Card, un H1 y JSON-LD sintácticamente válido. Los schemas incluyen `WebSite`, `WebPage`, `ImageObject`, `BreadcrumbList`, `Person`, `Brand` y `FAQPage`. Varios `ImageObject` y OG son operativamente inválidos porque el archivo de imagen no existe. El sitemap contiene las 22 URLs y `robots.txt` declara el sitemap correcto.

### WhatsApp

Todas las páginas utilizan `5215537629786`. Los mensajes se adaptan a la landing y se codifican con `encodeURIComponent`. El JavaScript no presenta errores sintácticos. Falta la comprobación final en dispositivos móviles reales.

### Responsive y accesibilidad

El CSS incluye breakpoints móviles, reorganización de grids y `prefers-reduced-motion`. Imágenes, menús, FAQ y botones incorporan alt/ARIA. La prueba visual interactiva quedó `NO VERIFICABLE`; debe repetirse con las imágenes completas en 320, 375, 768, 1024 px y escritorio.

### Técnica y seguridad

No se encontraron credenciales, claves API, datos sensibles, URLs locales, TODO, FIXME ni Lorem Ipsum. No hay IDs duplicados ni `aria-controls` huérfanos. Los 22 scripts pasan comprobación sintáctica. CSS y JavaScript están embebidos y muy duplicados, pero no se autoriza refactorizarlos en esta etapa.

## Hallazgos priorizados

| ID | Severidad | Evidencia | Riesgo | Acción | Esfuerzo |
| --- | --- | --- | --- | --- | --- |
| DB-001 | CRÍTICO | 84 ausencias en `assets/img/` | 121 solicitudes 404 | Producir e integrar assets | Alto |
| DB-002 | CRÍTICO | Hero y OG faltantes | Primer viewport, schema y redes rotos | Resolver P0 primero | Alto |
| DB-003 | CRÍTICO | 14 páginas afectadas | Sitio visualmente incompleto | No publicar aún | Alto |
| DB-004 | ALTO | `ImageObject` sin archivo físico | Datos estructurados inconsistentes | Integrar y revalidar | Medio |
| DB-005 | ALTO | Menú de Vida Natural inconsistente | Descubrimiento desigual | Unificar después de imágenes | Bajo |
| DB-006 | ALTO | QA visual pendiente | Riesgo responsive | Pruebas multidispositivo | Medio |
| DB-007 | MEDIO | CSS/JS repetidos | Mantenimiento costoso | Refactor futuro, no ahora | Medio |
| DB-008 | MEDIO | Sin `404.html` | Mala experiencia ante URL errónea | Crear en fase de cierre | Bajo |
| DB-009 | MEDIO | Documentos previos declaran cierre | Falsa sensación de terminación | Usar esta auditoría como estado oficial | Bajo |
| DB-010 | BAJO | `.DS_Store`, `__MACOSX` y copias antiguas | Ruido del paquete | Excluir del ZIP final | Bajo |
| DB-011 | BAJO | Sin favicon alternativo | Compatibilidad parcial | Añadir ICO/PNG aprobado | Bajo |

## Inventario técnico resumido

| Tipo | Cantidad | Condición |
| --- | ---: | --- |
| HTML | 22 | Sustantivos |
| WebP físicos | 69 | 66 integrados; 3 no referenciados |
| Markdown previos | 26 | Varios desactualizados |
| Sitemap / robots / htaccess | 1 de cada uno | Presentes |
| CSS/JS externos | 0 | Código embebido |
| Archivos vacíos | 0 | Ninguno |
| `.DS_Store` | 2 | Excluir de producción |

## Dictamen de publicación

`BLOQUEADO POR ELEMENTOS CRÍTICOS`. La estructura es compatible con `public_html`, pero el sitio no puede declararse completo ni listo para publicación mientras falten 84 imágenes, existan 121 referencias gráficas rotas y no se complete QA responsive, accesibilidad y móvil.

## Criterio de desbloqueo

Se podrá reevaluar como candidato a publicación cuando existan 150/150 imágenes, haya cero recursos locales 404, los P0 estén aprobados y validados, y las pruebas responsive, schema, WhatsApp y Lighthouse estén documentadas.
