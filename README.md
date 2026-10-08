# Juan Uribe · IA & Marketing

Sitio personal estático: portada, directorio de herramientas y guía de creación de contenido con IA. Mantiene HTML, CSS y JavaScript sin framework ni paso de compilación.

## Desarrollo local

Desde la raíz del repositorio:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Las rutas principales son `/`, `/herramientas/` y `/contenido-ia/`. `CNAME` conserva el dominio `juanuribeia.com`.

## Diseño y archivos

- `assets/site.css`: tokens, tipografía, navegación, botones y accesibilidad compartidos.
- `assets/home.css`: composición de la portada.
- `assets/resources.css`: estilo de las dos páginas de recursos.
- `assets/guide-layout.css`: layouts especializados de la guía existente.
- `assets/site.js`: menú móvil y apariciones progresivas; respeta movimiento reducido.
- `assets/home.js`: solicitud de guías, carga, errores y reintentos.
- `assets/fonts/`: Archivo variable alojada localmente, con su licencia OFL.
- `.agents/skills/`: skills proporcionadas por el usuario; consulta `.agents/README.md`.

El sistema visual usa fondo claro, texto oscuro y verde profundo como único acento. La composición editorial usa un nombre de gran escala, fotos sin marcos, columnas asimétricas y enlaces tipográficos. Los recursos se organizan como un directorio; el formulario por correo se despliega a petición del visitante. Las fotos y videos provienen del contenido original. Se conservan los originales; las versiones WebP reducen el peso de las imágenes de presentación.

## Solicitudes de guías

Los enlaces de descarga permanecen disponibles sin enviar datos. El formulario conserva el webhook existente y su petición `no-cors`. La respuesta es opaca: el navegador no puede verificar el estado HTTP ni la entrega del correo. Por eso el sitio lo indica y ofrece descarga directa. Los fallos de red y los tiempos de espera muestran un error y permiten reintentar.

Confirmar entregas por correo requerirá que el servicio permita CORS y devuelva una respuesta verificable. Las pruebas interceptan el webhook y no envían solicitudes reales ni datos a terceros.

## Prueba de navegador

Con Playwright disponible y el servidor en marcha:

```sh
node tests/smoke.cjs
```

Para instalar la herramienta fuera del checkout:

```sh
npm install --prefix /tmp/juan-qa playwright
NODE_PATH=/tmp/juan-qa/node_modules node tests/smoke.cjs
```

La prueba usa `/usr/bin/chromium`. Puedes establecer `CHROMIUM_PATH` para otro ejecutable y `SITE_URL` para otra dirección del servidor. Comprueba las tres páginas en varios tamaños, menú, anchors, assets, estados del formulario, descargas sin JavaScript y movimiento reducido. Una comprobación automatizada no sustituye la revisión visual ni confirma servicios externos.
