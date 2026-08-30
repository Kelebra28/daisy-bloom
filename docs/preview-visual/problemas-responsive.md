# Problemas responsive

## Pruebas realizadas

Se revisaron las seis páginas prioritarias en 320, 375, 768, 1024 y 1440 px. En las 30 combinaciones el documento no reportó desbordamiento horizontal y las imágenes integradas no mostraron iconos rotos. El menú móvil, una FAQ, footer y WhatsApp se verificaron funcionalmente.

## Hallazgos

| Prioridad | Hallazgo | Evidencia | Impacto | Ajuste propuesto, no aplicado |
| --- | --- | --- | --- | --- |
| CRÍTICA | Logo principal sin límite de altura | 1448×1086 real; 230–250×1086 en hero y 190×1086 en footer | Hero de 2202–2540 px y footer de 1309–1358 px | `height:auto`, límite de altura/relación y variante horizontal. |
| CRÍTICA | Cajas de imagen mayores que el móvil | En 375 px: 585–669 px de ancho frente a 360 px útiles | Recorte lateral oculto; usuario no puede ver toda la imagen | `width:100%`, `max-width:100%`, revisar anchos de grid y wrappers. |
| ALTA | Hero vertical forzado a caja horizontal en móvil | Vida/Descanso: 667×430 con `object-fit:cover` y centro | Pérdida fuerte de contexto; posible corte de cuerpo/objetos | Caja vertical o cuadrada y `object-position` específico. |
| ALTA | Retratos verticales dentro de cajas 667×470 o 667×540 | Belleza, facial, corporal, guía y CTA | Recorte notable de cabeza, manos o producto según imagen | Altura automática o ratio móvil dedicado. |
| MEDIA | El overflow se oculta | `scrollWidth` no supera `innerWidth`, aunque la caja sí | Oculta el defecto a pruebas automáticas simples | Revisar geometría real, no solo scrollbar. |
| MEDIA | Animaciones `reveal` dependen de tiempo/scroll | Un bloque de Inicio seguía en opacity 0 al muestreo temprano de 1440 px | Capturas o demo rápida pueden parecer vacías | Soporte `prefers-reduced-motion` y estado inicial más robusto. |
| BAJA | Cambio de menú en 1024 px | El botón móvil sigue presente hasta 1024 px; escritorio aparece en 1440 px | Funciona, pero conviene validar intención de breakpoint | Confirmar breakpoint de diseño. |

## Geometría de página observada

| Página | Alto 375 px | Alto 768 px | Alto 1440 px |
| --- | ---: | ---: | ---: |
| Inicio | 15,227 | 11,036 | 10,059 |
| Belleza | 15,263 | 12,432 | 11,419 |
| Cuidado Facial | 20,129 | 15,948 | 14,510 |
| Cuidado Corporal | 20,589 | 15,990 | 14,829 |
| Vida Natural | 17,371 | 13,607 | 12,200 |
| Descanso | 19,897 | 17,012 | 14,980 |

Estas longitudes son excesivas para el contenido disponible y se explican principalmente por el logo y por cajas de imagen no fluidas.

## Interacciones

- Menú móvil: `aria-expanded` cambió de `false` a `true` y volvió a cerrar correctamente.
- FAQ: la primera pregunta cambió de `false` a `true` y regresó a `false`.
- WhatsApp: presente en las seis prioritarias.
- Rutas: las 22 páginas abrieron por HTTP local.

## Criterio de salida

Repetir las 30 combinaciones después de corregir CSS. Una página no debe pasar a `APTA PARA DEMOSTRACIÓN` hasta que todas las cajas respeten el ancho móvil, el logo deje de dominar la altura y se validen capturas completas tras terminar las animaciones.
