# Reporte de previsualización visual — Daisy Bloom

Fecha: 19 de junio de 2026  
Fuente revisada: `/Users/danielfuentes/Documents/Daisy bloom 2/daisy-bloom-public_html/`

## Entorno local

- Comando: `python3 -m http.server 8000 --bind 127.0.0.1`
- Puerto: `8000`
- URL: `http://127.0.0.1:8000/` (equivalente local: `http://localhost:8000/`)
- Resultado: el sitio abre por HTTP; las rutas internas, estilos embebidos, JavaScript, imágenes integradas y enlaces de las seis páginas prioritarias responden.
- Pruebas: 320, 375, 768, 1024 y 1440 px.
- Interacciones: el menú móvil abre y cierra; la FAQ abre y cierra; footer y botón de WhatsApp están presentes en las seis páginas.

## Conclusión ejecutiva

Las seis páginas prioritarias están **completas en archivos**, pero todavía no son aptas para una presentación libre. El problema dominante es de CSS: `daisy-bloom-logo-principal.webp` mide 1448×1086 px y se muestra con una altura de 1086 px en hero y footer. Esto alarga cada portada y pie, deforma la composición y distrae. En 375 px varias imágenes conservan cajas de 585–669 px dentro de una página útil de 360 px; el contenido queda recortado por contenedores, aunque no aparezca una barra horizontal.

La opción segura actual es un **recorrido local guiado** por URL directa, presentándolo expresamente como revisión. Antes de enseñarlo a Daisy conviene autorizar una corrección CSS acotada y repetir capturas. Un staging privado es viable después de esa corrección, nunca en el dominio público principal.

## Estado de páginas prioritarias

| Página | Desktop | Tablet | Móvil | Hero | Imágenes | Menú | CTA | Footer | WhatsApp | Apta para Daisy | Observaciones |
| ------ | ------- | ------ | ----- | ---- | -------- | ---- | --- | ------ | -------- | --------------- | ------------- |
| Inicio | REQUIERE AJUSTE | REQUIERE AJUSTE | BLOQUEADO | REQUIERE AJUSTE | PARCIAL | CORRECTO | CORRECTO | REQUIERE AJUSTE | CORRECTO | PARCIAL | Logo de 1086 px de alto; cards y retratos exceden la caja móvil. |
| Belleza que Florece | REQUIERE AJUSTE | REQUIERE AJUSTE | BLOQUEADO | REQUIERE AJUSTE | PARCIAL | CORRECTO | CORRECTO | REQUIERE AJUSTE | CORRECTO | PARCIAL | Todas las imágenes existen; recorte móvil agresivo. |
| Cuidado Facial | REQUIERE AJUSTE | REQUIERE AJUSTE | BLOQUEADO | REQUIERE AJUSTE | PARCIAL | CORRECTO | CORRECTO | REQUIERE AJUSTE | CORRECTO | PARCIAL | Imágenes de 667×540 en viewport de 375 px. |
| Cuidado Corporal | REQUIERE AJUSTE | REQUIERE AJUSTE | BLOQUEADO | REQUIERE AJUSTE | PARCIAL | CORRECTO | CORRECTO | REQUIERE AJUSTE | CORRECTO | PARCIAL | Mismo patrón de logo y cajas móviles sobredimensionadas. |
| Vida Natural Bloom | REQUIERE AJUSTE | REQUIERE AJUSTE | BLOQUEADO | REQUIERE AJUSTE | PARCIAL | CORRECTO | CORRECTO | REQUIERE AJUSTE | CORRECTO | PARCIAL | Hero móvil 667×430: recorte fuerte de una imagen vertical. |
| Descanso, Calma y Equilibrio | REQUIERE AJUSTE | REQUIERE AJUSTE | BLOQUEADO | REQUIERE AJUSTE | PARCIAL | CORRECTO | CORRECTO | REQUIERE AJUSTE | CORRECTO | PARCIAL | Estructura completa; hero y editoriales requieren reglas móviles. |

## Evidencias y limitación de capturas

Se guardaron **43 capturas diagnósticas** en `desktop/`, `tablet/`, `mobile/` y `secciones/`. Son útiles para documentar el logo estirado, el encuadre y las áreas ocultas, pero **no deben utilizarse como material de presentación**: el motor de captura agotó tiempo al intentar páginas completas largas y algunas tomas se produjeron antes de que terminara la animación `reveal`. Por esta razón, las capturas completas de Descanso y algunas variantes de Vida Natural quedaron `NO VERIFICABLE` y no se fabricaron sustitutos engañosos.

## Problemas visuales prioritarios

1. Logo principal: archivo 1448×1086 frente a la expectativa horizontal 640×240; la regla actual fija ancho pero no limita altura.
2. Hero: entre 2202 y 2540 px de alto en escritorio, principalmente por el logo.
3. Footer: entre 1309 y 1358 px de alto por el mismo recurso.
4. Móvil: imágenes de 585–669 px dentro de 375 px; el desbordamiento queda oculto y se percibe como recorte.
5. Todos los contenidos visuales usan `object-position: 50% 50%`; un encuadre único no protege rostros, manos o productos en todos los formatos.
6. La animación de entrada necesita espera y desplazamiento; una captura o demostración demasiado rápida puede mostrar bloques temporalmente vacíos.

## Recomendación de staging

Es viable después del ajuste CSS y nueva QA: copia separada, `noindex, nofollow`, fuera del sitemap, protegida con contraseña cuando sea posible y con aviso “versión en revisión”. No usar todavía el dominio público ni modificar la fuente oficial para construir el staging.

## Siguiente acción recomendada

Autorizar únicamente una corrección CSS controlada para: limitar el logo, hacer imágenes y grids fluidos en móvil y revisar `object-position` por sección. Después, repetir las capturas completas y aprobar las seis páginas antes de cualquier staging.

## Confirmación de alcance

No se modificó HTML público, CSS ni JavaScript; no se renombraron ni editaron imágenes; no se publicó en Hostinger; no se modificaron sitemap, robots, canonicals ni schema. Solo se inició un servidor local, se realizaron pruebas y se generaron documentación/capturas dentro de `docs/preview-visual/`.
