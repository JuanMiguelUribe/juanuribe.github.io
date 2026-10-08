# Juan Uribe · IA aplicada

Sitio estático orientado a enseñanza y comunidad. La portada y las landing conectan prácticas abiertas, recursos y seguimiento en Instagram. El trabajo profesional mantiene un recorrido propio. HTML, CSS y JavaScript nativos; GitHub Pages no necesita instalar dependencias ni compilar la web.

## Páginas

| Ruta                        | Contenido                                                               |
| --------------------------- | ----------------------------------------------------------------------- |
| `/`                         | Portada, invitación a aprender, Florencia, recursos y comunidad.        |
| `/aprender/`                | Selección de prácticas.                                                 |
| `/aprender/llms/`           | Contexto, evaluación de respuestas, ejercicio y estructura copiable.    |
| `/aprender/imagen-y-video/` | Brief visual, continuidad y proceso de Florencia.                       |
| `/aprender/automatizacion/` | Entrada, pasos, salida y revisión de un flujo.                          |
| `/aprender/musica/`         | Dirección musical, comparación e iteración.                             |
| `/recursos/`                | Biblioteca: búsqueda, filtros, enlace compartible y descargas directas. |
| `/comunidad/`               | Objetivo actual, participación y enlaces de redes.                      |
| `/sobre-mi/`                | Práctica y enfoque de Juan.                                             |
| `/trabaja-conmigo/`         | Contenido, video, automatización, portafolios y contacto.               |
| `/herramientas/`            | Directorio original y categorías conservadas.                           |
| `/contenido-ia/`            | Guía original y ejemplos de imagen, animación y UGC.                    |

`404.html` ofrece salida para direcciones no existentes. Cada página tiene título, descripción, canonical y metadatos sociales; `sitemap.xml` incluye las doce rutas públicas. `CNAME` mantiene `juanuribeia.com`. Los cursos se presentan solo como intención futura, según el objetivo declarado por el usuario.

## Desarrollo

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Para modificar el contenido de las nuevas páginas y el marco común, editar `scripts/build_site.py` y regenerar:

```sh
python3 scripts/build_site.py
```

El script usa solo la biblioteca estándar de Python. `_site-content/` conserva fragmentos originales, el formulario y resultados de la versión anterior. Los fragmentos `tools-original.html` y `guide-original.html` alimentan las dos páginas de referencia. Tras regenerar se puede aplicar Prettier a los HTML y assets para mantener el formato. No es una dependencia de ejecución.

## Componentes

- `assets/site.css`: tokens, Archivo variable local, layouts, navegación, responsive y accesibilidad.
- `assets/site.js`: menú móvil y mejora progresiva de apariciones.
- `assets/library.js`: búsqueda sin tildes, filtros, recuento, estado vacío, reinicio y estado en URL.
- `assets/lesson.js`: copia de estructuras y selección de texto cuando no está disponible el portapapeles.
- `assets/home.js`: petición opcional de guías; estados de carga, error, reintento y tiempo de espera.
- `assets/guide-layout.css`, `resources.css` y `legacy-polish.css`: layouts y estilos de las páginas de referencia.
- `assets/fonts/`: Archivo y sus licencias; Outfit se conserva de la versión anterior.

Fotos y videos proceden del contenido original. Imágenes WebP, dimensiones reservadas, carga diferida y videos con controles y `preload="none"`. No hay videos de fondo ni bibliotecas de animación. Sin JavaScript siguen disponibles contenido, enlaces, guías y estructuras de los prompts.

## Formulario

Las descargas permanecen abiertas. El formulario conserva el webhook existente y `no-cors`: su respuesta opaca no permite confirmar estado HTTP ni entrega del correo. El texto lo indica y ofrece acceso directo. Las pruebas interceptan el endpoint y nunca envían datos reales.

## Comprobaciones

Con Playwright y Chromium disponibles:

```sh
node tests/smoke.cjs
node tests/journeys.cjs
```

`SITE_URL` permite otra dirección de prueba y `CHROMIUM_PATH` otro ejecutable. Playwright puede instalarse fuera del checkout:

```sh
npm install --prefix /tmp/juan-qa playwright
NODE_PATH=/tmp/juan-qa/node_modules node tests/smoke.cjs
```

Smoke: doce páginas en cinco anchos, menú, imágenes, anchors, formulario, contenido sin JavaScript y movimiento reducido. Journeys: recorrido de aprendizaje, filtros, tildes, URL, estado vacío, copia y fallback, enlaces internos y metadatos. La revisión automatizada de accesibilidad no sustituye la visual ni verifica servicios externos.

## Publicación y material interno

Se publican los archivos estáticos generados. `_config.yml` excluye tooling, fuentes de plantillas y material de marca de GitHub Pages. `.agents/`, `AGENTS.md` y `brand-knowledge/` son contexto local de trabajo; no se incluyen en la publicación de este rediseño. El diseño conserva la identidad verde y Archivo; UI UX Pro Max se aplicó a jerarquía e interacción. La skill Apple Design específica no estaba disponible en cloud; se usaron principios generales de interfaz como complemento, sin afirmar que se ejecutó esa skill.
