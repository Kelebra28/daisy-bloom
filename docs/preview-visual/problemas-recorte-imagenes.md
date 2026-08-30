# Problemas de recorte de imágenes

## Criterio común

En las seis páginas, las fotos usan `object-fit: cover` y `object-position: 50% 50%`. El emblema usa `contain`; el logo principal usa `fill`. La calidad aparente de los archivos presentes es buena, pero el encuadre móvil no es confiable porque las cajas exceden el viewport. Los estados siguientes no implican aprobación creativa final.

## Identidad compartida

| Archivo | Páginas/sección | Real | Contenedor escritorio / móvil | Fit/posición | Diagnóstico | Estado |
| --- | --- | ---: | --- | --- | --- | --- |
| `daisy-bloom-logo-emblema.webp` | Todas / header | 512×512 | 48×48 / 48×48 | contain / centro | Correcto, nítido y coherente. | SE VE CORRECTA |
| `daisy-bloom-logo-principal.webp` | Todas / hero y footer | 1448×1086 | 230–250×1086; footer 190×1086 en todos los anchos | fill / centro | No es horizontal; fuerza 1086 px de alto y estrecha la marca. Requiere CSS primero y después decidir si se genera variante 640×240 transparente. | REQUIERE AJUSTE CSS |

## Inicio

| Archivo | Sección | Real | Contenedor desktop / móvil | Recorte y calidad | Estado |
| --- | --- | ---: | --- | --- | --- |
| `daisy-bloom-hero-bienestar-belleza-crecimiento.webp` | Hero | 1086×1448 | 418×560 / 418×560 | Ratio coherente; rostro y manos deben confirmarse tras corregir ancho móvil. | REQUIERE REVISIÓN HUMANA |
| `daisy-bloom-bienestar-diario-suplementos-nutricion.webp` | Rutas | 1512×1040 | 232×174 / 316×174 | En móvil pasa a una caja más panorámica; recorte vertical moderado. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-belleza-que-florece-autocuidado.webp` | Rutas | 1512×1040 | 232×174 / 316×174 | Misma pérdida vertical; calidad correcta. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-vida-natural-consejos-bienestar.webp` | Rutas | 1526×1030 | 232×174 / 316×174 | Misma pérdida vertical; revisar objetos centrales. | REQUIERE REVISIÓN HUMANA |
| `daisy-bloom-crece-emprendimiento-femenino.webp` | Rutas | 1512×1040 | 232×174 / 316×174 | Misma pérdida vertical. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-daisy-guia-bienestar-belleza.webp` | Daisy guía | 1122×1402 | 377×470 / 669×470 | Escritorio respeta ratio; móvil convierte retrato en panorámica y corta cuerpo/manos. | REQUIERE AJUSTE CSS |
| `daisy-bloom-cta-florecer-con-daisy.webp` | CTA | 1122×1402 | 331×470 / 587×470 | Móvil sobredimensionado y panorámico. | REQUIERE AJUSTE CSS |

## Belleza que Florece

| Archivo | Sección | Real | Contenedor desktop / móvil | Recorte y calidad | Estado |
| --- | --- | ---: | --- | --- | --- |
| `daisy-bloom-belleza-que-florece-seytu-hero.webp` | Hero | 1086×1448 | 418×560 / 667×560 | Escritorio correcto; móvil corta gran parte superior/inferior del retrato. | REQUIERE AJUSTE CSS |
| `daisy-bloom-rutas-belleza-seytu.webp` | Primera sección | 1122×1402 | 375×470 / 667×470 | Correcta en desktop; panorámica en móvil. | REQUIERE AJUSTE CSS |
| `daisy-bloom-cuidado-facial-seytu.webp` | Cómo ayuda Daisy | 1122×1402 | 375×470 / 667×470 | Riesgo de cortar rostro/manos/productos. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-daisy-guia-belleza-seytu.webp` | Daisy guía | 1122×1402 | 375×470 / 667×470 | Calidad aparente buena; caja móvil incorrecta. | REQUIERE AJUSTE CSS |
| `daisy-bloom-whatsapp-belleza-seytu.webp` | CTA | 1122×1402 | 329×470 / 585×470 | Recorte móvil excesivo. | REQUIERE AJUSTE CSS |

## Cuidado Facial

| Archivo | Sección | Real | Contenedor desktop / móvil | Recorte y calidad | Estado |
| --- | --- | ---: | --- | --- | --- |
| `daisy-bloom-cuidado-facial-seytu-hero.webp` | Hero | 1086×1448 | 375×540 / 667×540 | Ligero recorte desktop; fuerte recorte móvil alrededor del rostro/mano. | REQUIERE AJUSTE CSS |
| `daisy-bloom-rutina-facial-seytu.webp` | Primera sección | 1122×1402 | 375×540 / 667×540 | Móvil pierde mucho del encuadre vertical. | REQUIERE AJUSTE CSS |
| `daisy-bloom-productos-seytu-cuidado-facial.webp` | Productos | 1024×1536 | 375×540 / 667×540 | Producto puede quedar cortado; necesita posición específica. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-daisy-guia-cuidado-facial-seytu.webp` | Daisy guía | 1122×1402 | 375×540 / 667×540 | Calidad buena; caja móvil incorrecta. | REQUIERE AJUSTE CSS |
| `daisy-bloom-whatsapp-cuidado-facial-seytu.webp` | CTA | 1122×1402 | 329×540 / 585×540 | Sobredimensión móvil y recorte lateral/vertical. | REQUIERE AJUSTE CSS |

## Cuidado Corporal

| Archivo | Sección | Real | Contenedor desktop / móvil | Recorte y calidad | Estado |
| --- | --- | ---: | --- | --- | --- |
| `daisy-bloom-cuidado-corporal-seytu-hero.webp` | Hero | 1122×1402 | 375×540 / 667×540 | Escritorio razonable; móvil panorámico. | REQUIERE AJUSTE CSS |
| `daisy-bloom-rutina-corporal-seytu.webp` | Primera sección | 1122×1402 | 375×540 / 667×540 | Riesgo de cortar manos/cuerpo. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-productos-seytu-cuidado-corporal.webp` | Productos | 1024×1536 | 375×540 / 667×540 | Objeto/producto necesita posición focal. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-daisy-guia-cuidado-corporal-seytu.webp` | Daisy guía | 1122×1402 | 375×540 / 667×540 | Calidad buena; caja móvil incorrecta. | REQUIERE AJUSTE CSS |
| `daisy-bloom-whatsapp-cuidado-corporal-seytu.webp` | CTA | 1122×1402 | 329×540 / 585×540 | Recorte móvil excesivo. | REQUIERE AJUSTE CSS |

## Vida Natural Bloom

| Archivo | Sección | Real | Contenedor desktop / móvil | Recorte y calidad | Estado |
| --- | --- | ---: | --- | --- | --- |
| `daisy-bloom-vida-natural-bloom-hero.webp` | Hero | 1200×1500 | 418×560 / 667×430 | Móvil cambia retrato a panorámica; puede perder cuerpo y contexto. | REQUIERE AJUSTE CSS |
| `daisy-bloom-rutas-vida-natural.webp` | Primera sección | 1200×1200 | 375×470 / 667×470 | Cuadrada forzada a vertical en desktop y panorámica en móvil. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-habitos-saludables.webp` | Hábitos | 1200×1500 | 375×470 / 667×470 | Desktop casi correcto; móvil recorte fuerte. | REQUIERE AJUSTE CSS |
| `daisy-bloom-daisy-guia-vida-natural.webp` | Daisy guía | 1200×1500 | 375×470 / 667×470 | Móvil requiere ratio y foco propios. | REQUIERE AJUSTE CSS |
| `daisy-bloom-cta-vida-natural.webp` | CTA | 1200×1500 | 329×470 / 585×470 | Móvil panorámico y sobredimensionado. | REQUIERE AJUSTE CSS |

## Descanso, Calma y Equilibrio

| Archivo | Sección | Real | Contenedor desktop / móvil | Recorte y calidad | Estado |
| --- | --- | ---: | --- | --- | --- |
| `daisy-bloom-descanso-calma-equilibrio-hero.webp` | Hero | 1122×1402 | 418×560 / 667×430 | Imagen coherente y de buena calidad; móvil pierde cama/cuerpo por caja panorámica. | REQUIERE AJUSTE CSS |
| `daisy-bloom-pausas-conscientes.webp` | Introducción y pausas | 1254×1254 | 375×470 / 667×470 | Se usa dos veces; recorte opuesto entre desktop y móvil. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-rutina-noche-calma.webp` | Rutina de noche | 1254×1254 | 585×470 / 667×470 | Recorte horizontal moderado; calidad correcta. | REQUIERE REVISIÓN HUMANA |
| `daisy-bloom-ambiente-descanso.webp` | Ambiente | 1254×1254 | 375×470 / 667×470 | Revisar objetos de borde en ambos formatos. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-equilibrio-suave.webp` | Equilibrio | 1254×1254 | 585×470 / 667×470 | Recorte horizontal moderado. | REQUIERE REVISIÓN HUMANA |
| `daisy-bloom-habitos-saludables.webp` | Conexión hábitos | 1200×1500 | 375×470 / 667×470 | Desktop casi correcto; móvil fuerte. | REQUIERE AJUSTE CSS |
| `daisy-bloom-daisy-guia-descanso-calma.webp` | Daisy guía | 1254×1254 | 375×470 / 667×470 | Necesita ratio/foco responsive. | REQUIERE AJUSTE DE RECORTE |
| `daisy-bloom-cta-descanso-calma-equilibrio.webp` | CTA | 1254×1254 | 329×470 / 585×470 | Corta contenido cuadrado de forma distinta en cada ancho. | REQUIERE AJUSTE CSS |

## Conclusión

No se recomienda regenerar las fotos todavía: la mayoría tiene buena resolución y coherencia. Primero deben corregirse las cajas y ratios CSS; después se decide imagen por imagen si basta `object-position` o si alguna requiere regeneración. El logo principal sí necesita una decisión de marca: CSS inmediato y, posiblemente, una variante horizontal transparente posterior.
