"""Generate the public static site. Python standard library only."""

from pathlib import Path
from html import escape
import re, json

ROOT = Path(__file__).resolve().parents[1]
IG = "https://www.instagram.com/juanuribe.ia/"
TK = "https://www.tiktok.com/@juanuribe.ia"
YT = "https://www.youtube.com/@JuanUribeIA"
WA = "https://wa.me/573006773413"
# Reuse the original contact URL, including its chosen number and message.
old = (ROOT / "_site-content/home-original.html").read_text()
wa = re.search(r'href="(https://wa.me/[^\"]+)"', old)
if wa:
    WA = wa.group(1)
PROMPT = (
    "https://drive.google.com/file/d/1fCTSggOJ6U7pu9TWRM_bC2EglcOgmagn/view?usp=sharing"
)
TOOLS = (
    "https://drive.google.com/file/d/1M2VywKTa9xz9Zi6I-hS4RYZtp8-ADnHU/view?usp=sharing"
)
VERTICAL = (
    "https://drive.google.com/file/d/1CUzY2h8OqxDw9Mat3KaLEUUJMjLE5flA/view?usp=sharing"
)
DESIGN = "https://drive.google.com/drive/folders/1CTheHwRKN50d2Rg-Jh3o-TYYjUuzmXOd?usp=sharing"
VIDEO = "https://drive.google.com/drive/folders/1cQSxuQySnNRcJcst5mmK90lcAWgStlnu?usp=sharing"
ARROW = '<svg class="arrow" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 19 19 5M5 5h14v14"/></svg>'


def link(url, label, cls="text-link", external=None):
    ext = url.startswith("https:") if external is None else external
    return (
        f'<a class="{cls}" href="{escape(url, quote=True)}"'
        + (' target="_blank" rel="noopener noreferrer"' if ext else "")
        + f">{label}{ARROW}</a>"
    )


def breadcrumb(label, parent=None):
    return (
        '<nav class="breadcrumb" aria-label="Ubicación">'
        + link("/", "Inicio", "", False)
        + (
            f'<span aria-hidden="true">/</span>{link(parent[0], parent[1], "", False)}'
            if parent
            else ""
        )
        + f'<span aria-hidden="true">/</span><span aria-current="page">{label}</span></nav>'
    )


def hero(kicker, title, desc, actions="", cls=""):
    return f'<section class="page-hero {cls}"><p class="overline">{kicker}</p><h1>{title}</h1><p class="lead">{desc}</p><div class="actions">{actions}</div></section>'


def follow(
    title="Nos vemos en la próxima prueba.",
    desc="Aprende conmigo y comparte lo que estás creando con IA.",
):
    return f'<section class="follow-band" id="social"><div><h2>{title}</h2><p>{desc}</p></div>{link(IG, "Seguir a @juanuribe.ia", "button button-light")}</section>'


def portrait(cls="portrait", lazy=True):
    return (
        f'<img class="{cls}" src="/assets/juan-uribe.webp" width="1000" height="1241" alt="Juan Uribe" '
        + ('loading="lazy"' if lazy else 'fetchpriority="high"')
        + ">"
    )


def video(cls=""):
    return f'<video class="{cls}" controls muted playsinline preload="none" poster="/assets/ugc-preview.webp" width="1000" height="558" aria-label="Demostración de Florencia, un avatar generado con IA, en un video estilo UGC"><source src="/contenido-ia/assets/florencia-ugc.mp4" type="video/mp4">Tu navegador no puede reproducir este video. {link("/contenido-ia/assets/florencia-ugc.mp4", "Abrir el video")}</video>'


NAV = [
    ("/aprender/", "Aprender"),
    ("/recursos/", "Recursos"),
    ("/trabaja-conmigo/", "Mi trabajo"),
    ("/sobre-mi/", "Sobre mí"),
]
PAGES = {}


def page(
    path, title, desc, content, active=None, body="site-page", styles=(), scripts=()
):
    earlystyles = "".join(
        f'<link rel="stylesheet" href="{s}">'
        for s in styles
        if s == "/assets/guide-layout.css"
    )
    styles = tuple(s for s in styles if s != "/assets/guide-layout.css")
    nav = "".join(
        f'<li><a href="{u}"'
        + (
            (' aria-current="page"' if path == u else ' aria-current="location"')
            if active == u
            else ""
        )
        + f">{n}</a></li>"
        for u, n in NAV
    )
    menu = (
        "".join(link(u, n, "", False) for u, n in NAV)
        + link("/comunidad/", "Comunidad", "", False)
        + link("/herramientas/", "Herramientas", "", False)
        + link("/contenido-ia/", "Guía de contenido IA", "", False)
    )
    form = (
        '<script src="/assets/home.js" defer></script>'
        if 'id="guide-form"' in content
        else ""
    )
    canonical = "https://juanuribeia.com" + path
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title + " | Juan Uribe",
        "description": desc,
        "url": canonical,
        "isPartOf": {
            "@type": "WebSite",
            "name": "juanuribe.ia",
            "url": "https://juanuribeia.com/",
        },
    }
    if path == "/":
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                schema,
                {
                    "@type": "Person",
                    "@id": "https://juanuribeia.com/#juan",
                    "name": "Juan Uribe",
                    "url": "https://juanuribeia.com/sobre-mi/",
                    "sameAs": [IG, TK, YT],
                    "knowsAbout": [
                        "Inteligencia artificial",
                        "LLMs",
                        "Diseño",
                        "Música",
                        "Automatización",
                    ],
                },
            ],
        }
    structured = (
        '<script type="application/ld+json">'
        + json.dumps(schema, ensure_ascii=False).replace("</", "<\\/")
        + "</script>"
    )
    html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Juan Uribe</title><meta name="description" content="{escape(desc, quote=True)}"><link rel="canonical" href="{canonical}"><meta name="theme-color" content="#f7f8f4"><meta property="og:title" content="{escape(title, quote=True)} | Juan Uribe"><meta property="og:description" content="{escape(desc, quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://juanuribeia.com/assets/juan-uribe.webp"><meta name="twitter:card" content="summary_large_image">{structured}<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="preload" href="/assets/fonts/archivo-latin-standard-normal.woff2" as="font" type="font/woff2" crossorigin>{earlystyles}<link rel="stylesheet" href="/assets/site.css">{"".join(f'<link rel="stylesheet" href="{s}">' for s in styles)}<script src="/assets/site.js" defer></script>{"".join(f'<script src="{s}" defer></script>' for s in scripts)}{form}</head><body class="{body}"><a class="skip-link" href="#main-content">Saltar al contenido</a><header class="site-header"><nav class="site-nav" aria-label="Navegación principal"><a class="site-brand" href="/">juanuribe<span>.ia</span></a><ul class="site-nav-links">{nav}</ul>{link(IG, "Seguir en Instagram", "nav-cta")}<button class="menu-toggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="mobile-menu">Menú <span aria-hidden="true">+</span></button></nav><nav class="mobile-menu" id="mobile-menu" aria-label="Menú móvil" hidden>{menu}</nav></header><noscript><nav class="nojs-links" aria-label="Explorar el sitio">{menu}</nav></noscript><main id="main-content" tabindex="-1">{content}</main><footer class="site-footer"><div class="footer-top"><div><a class="site-brand" href="/">juanuribe<span>.ia</span></a><p>IA aplicada.<br>Procesos que puedes aprender.</p></div><nav aria-label="Aprendizaje"><p>Para aprender</p>{link("/aprender/", "Por dónde empezar", "", False)}{link("/recursos/", "Recursos gratis", "", False)}{link("/herramientas/", "Herramientas", "", False)}{link("/contenido-ia/", "Contenido con IA", "", False)}</nav><nav aria-label="Juan Uribe"><p>Más de Juan</p>{link("/sobre-mi/", "Sobre mí", "", False)}{link("/comunidad/", "Comunidad", "", False)}{link("/trabaja-conmigo/", "Trabaja conmigo", "", False)}</nav><nav aria-label="Redes sociales"><p>Nos encontramos en</p>{link(IG, "Instagram", "")}{link(TK, "TikTok", "")}{link(YT, "YouTube", "")}</nav></div><div class="footer-bottom"><span>© 2026 Juan Uribe</span><span>Inteligencia artificial. Criterio humano.</span></div></footer></body></html>'''
    out = ROOT / (
        "index.html"
        if path == "/"
        else path.lstrip("/")
        if path.endswith(".html")
        else path.strip("/") + "/index.html"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    PAGES[path] = {"title": title, "file": str(out.relative_to(ROOT))}


# Home: follow and learn before professional conversion.
form = (ROOT / "_site-content/form.html").read_text()
home = f"""<section class="home-hero" id="hero"><div class="hero-copy"><p class="overline">Juan Uribe · IA aplicada</p><h1>Aprende IA.<br><span>Úsala de verdad.</span></h1><p class="lead">Una imagen, una canción, una idea o un sistema. Comparto cómo los construyo con IA para que tú también puedas hacerlo.</p><div class="actions">{link("/aprender/", "Empezar a aprender", "button")}{link(IG, "Seguir mis pruebas")}</div><p class="hero-footnote">Desde mi práctica con empresas de Estados Unidos y Colombia.</p></div><figure class="hero-photo">{portrait(lazy=False)}<figcaption>Pruebo. Creo. Lo comparto.</figcaption></figure></section>
<section class="section start-section"><div class="section-heading"><h2>Empieza por algo<br>que quieras crear.</h2><p>Elige algo que quieras crear y empieza por una práctica.</p></div><div class="path-list"><a href="/aprender/llms/"><h3>Una idea mejor explicada.</h3><p>Aprende a dar contexto a un LLM y a revisar sus respuestas.</p><span>Trabajar con LLMs {ARROW}</span></a><a href="/aprender/imagen-y-video/"><h3>Una imagen que cobra vida.</h3><p>Del prompt a un personaje y de ese personaje al video.</p><span>Crear imagen y video {ARROW}</span></a><a href="/aprender/automatizacion/"><h3>Una tarea que deja de repetirse.</h3><p>Entiende un flujo antes de automatizar tu trabajo.</p><span>Explorar automatización {ARROW}</span></a></div><div class="section-end">{link("/aprender/musica/", "¿Quieres crear música? Empieza aquí")}</div></section>
<section class="case-feature section" id="portfolio"><div class="section-heading"><div><p class="overline">Una práctica para empezar</p><h2>Una imagen.<br>Todo un personaje.</h2></div><div><p>Florencia es un avatar generado con IA. Una misma identidad pasa de una foto a un video de marca. Aquí puedes ver el resultado y entender el proceso.</p>{link("/contenido-ia/#ejemplo", "Ver cómo se hizo", "text-link")}</div></div><div class="case-media"><figure><img src="/assets/florencia.webp" width="670" height="1200" loading="lazy" alt="Florencia, un personaje generado con IA"><figcaption>La imagen de partida.</figcaption></figure><figure>{video()}<figcaption>El resultado: video estilo UGC.</figcaption></figure></div></section>
<section class="section resources-preview" id="guides"><div class="section-heading"><h2>De la curiosidad<br>a la práctica.</h2><p>Recursos abiertos para que tengas por dónde empezar. Puedes acceder directamente.</p></div><div class="guides-grid"><article class="guide-card" id="featured"><p class="resource-type">Prompt + guía</p><h3>Del producto al anuncio.</h3><p>Una plantilla editable y ejemplos para convertir una foto de producto en una idea de anuncio con IA.</p>{link(PROMPT, "Descargar prompt")}</article><article class="guide-card"><p class="resource-type">Guía paso a paso</p><h3>De horizontal a vertical.</h3><p>Adapta un video para Reels, TikTok y Shorts con el proceso de la guía.</p>{link(VERTICAL, "Descargar guía")}</article></div><div class="section-end">{link("/recursos/", "Ver todos los recursos")}</div>{form}</section>
<section class="section home-about"><figure>{portrait()}</figure><div><p class="overline">Detrás de juanuribe.ia</p><h2>La práctica es<br>el punto de partida.</h2><p>Trabajo con IA en proyectos de empresas de Estados Unidos y Colombia. Uso LLMs, diseño, generación de contenido, música y automatización.</p><p>Ahora quiero compartir esa práctica, enseñar y construir una comunidad que aprenda haciendo.</p>{link("/sobre-mi/", "Conoce mi enfoque")}</div></section>
{follow("Lo que pruebo,<br>lo comparto.", "Sígueme en Instagram y trae tus preguntas. Quiero que esta comunidad se construya también con lo que tú quieres aprender.")}
<span id="results" class="anchor-target"></span><section class="section business-bridge" id="services"><div id="contact"><h2>¿Y si lo llevamos<br>a tu negocio?</h2><p>Contenido de marca, video y automatización aplicada a un problema concreto.</p></div>{link("/trabaja-conmigo/", "Conoce mi trabajo")}</section>"""
page(
    "/",
    "Aprende IA creando",
    "Procesos, recursos y prácticas de IA con Juan Uribe. Aprende a crear con LLMs, imagen, video, música y automatización.",
    home,
    body="site-page home",
)

ROUTES = [
    (
        "llms",
        "Pensar y trabajar con LLMs",
        "Aprende a pedir contexto, comparar resultados y revisar una respuesta antes de usarla.",
        "Texto · Contexto · Criterio",
    ),
    (
        "imagen-y-video",
        "Crear imagen y video",
        "Construye una imagen con intención y entiende cómo convertirla en un personaje en movimiento.",
        "Imagen · Personajes · Video",
    ),
    (
        "automatizacion",
        "Construir una automatización",
        "Dibuja una tarea repetitiva, define sus pasos y reconoce qué tiene sentido automatizar.",
        "Procesos · n8n · Flujos",
    ),
    (
        "musica",
        "Empezar a crear música",
        "Usa una intención musical como punto de partida y aprende a iterar sobre el resultado.",
        "Música · Dirección · Iteración",
    ),
]
route_html = "".join(
    f'<a class="learning-route" href="/aprender/{slug}/"><div><p class="resource-type">{topics}</p><h2>{title}</h2></div><div><p>{desc}</p><span>Empezar la práctica {ARROW}</span></div></a>'
    for slug, title, desc, topics in ROUTES
)
learn = (
    breadcrumb("Aprender")
    + hero(
        "Aprende con Juan",
        "Elige una idea.<br>Hazla realidad.",
        "No necesitas conocer todas las herramientas para empezar. Estas prácticas te ayudan a entender qué pedir, qué evaluar y qué hacer después.",
    )
    + f'<section class="section learning-routes">{route_html}</section>'
    + f'<section class="section split-note"><h2>Aprender también<br>es probar.</h2><div><p>Estas páginas son un punto de partida. Usa un ejemplo propio, revisa el resultado y cambia una cosa a la vez. Si algo no funciona, esa pregunta también merece una explicación.</p>{link("/comunidad/", "Comparte la pregunta con la comunidad")}</div></section>'
    + follow()
)
page(
    "/aprender/",
    "Por dónde empezar con IA",
    "Elige una práctica de LLMs, imagen y video, automatización o música. Aprende IA haciendo.",
    learn,
    active="/aprender/",
)

resources = [
    (
        "crear",
        "Prompt + guía",
        "Del producto al anuncio",
        "Plantilla editable y ejemplos para transformar una foto de producto en una idea de anuncio.",
        PROMPT,
        "Descargar prompt",
        "Producto imagen publicidad diseño",
    ),
    (
        "crear",
        "Guía",
        "Horizontal a vertical con IA",
        "Un proceso paso a paso para adaptar video a Reels, TikTok y Shorts.",
        VERTICAL,
        "Descargar guía",
        "video reels vertical shorts",
    ),
    (
        "pensar crear automatizar",
        "Guía",
        "Herramientas IA que uso",
        "La selección que acompaña mis procesos de creación y automatización.",
        TOOLS,
        "Descargar guía",
        "llms imagen música audio herramientas",
    ),
    (
        "pensar crear automatizar",
        "Directorio",
        "Explorar herramientas",
        "Opciones organizadas por asistentes, imagen, video, audio, automatización y productividad.",
        "/herramientas/",
        "Abrir directorio",
        "llms imagen video audio automatizar",
    ),
    (
        "crear",
        "Caso explicado",
        "El proceso de Florencia",
        "De imagen a video y UGC: una demostración visual con un personaje generado con IA.",
        "/contenido-ia/#ejemplo",
        "Ver el proceso",
        "avatar personaje imagen video UGC",
    ),
    (
        "pensar",
        "Práctica en la web",
        "Dar contexto a un LLM",
        "Una estructura para pedir algo concreto y revisar la respuesta que recibes.",
        "/aprender/llms/",
        "Empezar la práctica",
        "llm prompt texto contexto",
    ),
    (
        "automatizar",
        "Práctica en la web",
        "Diseñar tu primer flujo",
        "Mapea una tarea repetitiva antes de abrir una herramienta de automatización.",
        "/aprender/automatizacion/",
        "Empezar la práctica",
        "n8n proceso tarea automatización",
    ),
    (
        "crear",
        "Práctica en la web",
        "Una idea musical con IA",
        "Define dirección, escucha variantes y registra qué quieres cambiar.",
        "/aprender/musica/",
        "Empezar la práctica",
        "música audio canción suno",
    ),
]
entries = "".join(
    f'<article class="resource-entry" data-resource data-category="{cat}" data-search="{escape(title + " " + desc + " " + tags, quote=True)}"><p class="resource-type">{typ}</p><h2>{title}</h2><p>{desc}</p>{link(url, label)}</article>'
    for cat, typ, title, desc, url, label, tags in resources
)
library = (
    breadcrumb("Recursos")
    + hero(
        "Para tener a mano",
        "Recursos para<br>tu próxima idea.",
        "Guías, prompts y prácticas para llevar una idea al siguiente paso. Las descargas están abiertas.",
    )
    + f"""<section class="section library" data-library><div class="library-controls" hidden><div class="search-field"><label for="resource-search">¿Qué quieres crear o aprender?</label><input id="resource-search" type="search" placeholder="Prueba «video», «prompt» o «música»" autocomplete="off"></div><div class="filter-group" role="group" aria-label="Filtrar recursos por tema"><button type="button" data-filter="todos" aria-pressed="true">Todo</button><button type="button" data-filter="pensar" aria-pressed="false">Pensar</button><button type="button" data-filter="crear" aria-pressed="false">Crear</button><button type="button" data-filter="automatizar" aria-pressed="false">Automatizar</button></div><p id="resource-count" class="library-count" role="status" aria-live="polite"></p></div><div class="resource-grid">{entries}</div><div id="resource-empty" class="empty-state" hidden><h2>Probemos con otra búsqueda.</h2><p>Prueba «video», «prompt» o «música», o vuelve a ver todos los recursos.</p><button class="button" type="button" data-reset>Ver todos los recursos</button></div><div class="resource-mail"><h2>¿Los prefieres por correo?</h2><p>También puedes solicitar las dos guías originales sin perder el acceso a las descargas directas.</p>{form}</div></section>"""
    + follow()
)
page(
    "/recursos/",
    "Recursos gratuitos de IA",
    "Guías, prompts, herramientas y prácticas de IA. Busca recursos para pensar, crear y automatizar.",
    library,
    active="/recursos/",
    scripts=("/assets/library.js",),
)

community = (
    breadcrumb("Comunidad")
    + f"""<section class="community-hero page-hero"><div><p class="overline">Aprendemos mejor cuando compartimos</p><h1>La próxima idea<br>puede ser tuya.</h1><p class="lead">Estoy retomando juanuribe.ia para enseñar IA desde la práctica y construir una comunidad. Un lugar para probar, preguntar y compartir lo que vamos creando.</p>{link(IG, "Seguir a @juanuribe.ia", "button")}</div><figure>{portrait(lazy=False)}<figcaption>Juan Uribe · Aprender haciendo.</figcaption></figure></section><section class="section split-note"><h2>Así quiero<br>compartir la IA.</h2><div class="plain-list"><article><h3>Resultados que puedas entender.</h3><p>Mostrar lo que sale y explicar las decisiones que hay detrás.</p></article><article><h3>Preguntas que abren una práctica.</h3><p>Lo que cuesta, lo que falla y lo que quieres aprender también puede convertirse en contenido.</p></article><article><h3>Recursos para volver a intentarlo.</h3><p>Guías y ejemplos que puedas consultar mientras trabajas en tu propia idea.</p></article></div></section><section class="section community-invitation"><h2>¿Qué estás<br>intentando crear?</h2><p>Una imagen, un video, una canción, una respuesta mejor o una automatización. Cuéntamelo en Instagram: esa pregunta puede ser el siguiente punto de partida.</p>{link(IG, "Llevar mi pregunta a Instagram", "text-link")}<div class="social-links">{link(TK, "También en TikTok")}{link(YT, "También en YouTube")}</div></section><section class="section split-note quiet-section"><h2>Primero aprender.<br>Después, profundizar.</h2><div><p>Quiero desarrollar cursos en el futuro. Ahora el foco está en compartir prácticas y conocer qué quiere aprender la comunidad.</p>{link("/aprender/", "Empieza con una práctica")}</div></section>"""
)
page(
    "/comunidad/",
    "La comunidad de juanuribe.ia",
    "Aprendamos IA desde la práctica. Sigue a Juan Uribe, comparte tus preguntas y explora recursos gratuitos.",
    community,
)

about = (
    breadcrumb("Sobre mí")
    + f"""<section class="about-hero page-hero"><figure>{portrait(lazy=False)}</figure><div><p class="overline">Soy Juan Uribe</p><h1>Pruebo la IA.<br>Creo con ella.<br>Comparto el proceso.</h1><p class="lead">Trabajo con empresas de Estados Unidos y Colombia en proyectos de IA. Mi práctica conecta LLMs, diseño, generación de contenido, música y automatización.</p>{link(IG, "Acompaña mis pruebas")}</div></section><section class="section split-note"><h2>Del trabajo real<br>a lo que enseño.</h2><div><p>Me interesa lo que puedes hacer con la IA cuando una herramienta deja de ser una novedad y empieza a resolver una tarea concreta.</p><p>Por eso quiero compartir resultados junto con decisiones, pasos y límites. Ahora mi objetivo con juanuribe.ia es enseñar, retener audiencia y crear comunidad.</p></div></section><section class="section personal-practice"><p class="overline">Una práctica, muchos lenguajes</p><h2>Texto. Imagen.<br>Movimiento. Música.</h2><div class="practice-grid"><p>Los LLMs ayudan a pensar y trabajar con información. El diseño y el video llevan una idea al terreno visual. La música abre otra forma de crear. La automatización conecta pasos para que un proceso funcione.</p><div>{link("/aprender/", "Explora lo que puedes aprender")}{link("/trabaja-conmigo/", "Conoce mi trabajo con empresas")}</div></div></section>"""
    + follow()
)
page(
    "/sobre-mi/",
    "Sobre Juan Uribe",
    "Conoce la práctica de Juan Uribe en IA, LLMs, diseño, música y automatización para empresas de Estados Unidos y Colombia.",
    about,
    active="/sobre-mi/",
)

results = (
    (ROOT / "_site-content/results.html")
    .read_text()
    .replace('<h2 class="sr-only">', "<h2>")
)
work = (
    breadcrumb("Mi trabajo")
    + hero(
        "IA aplicada a empresas",
        "IA para crear contenido<br>y conectar procesos.",
        "Trabajo con empresas de Estados Unidos y Colombia en contenido, video y automatización con IA. El punto de partida es lo que tu proyecto necesita resolver.",
        link(WA, "Cuéntame tu proyecto", "button")
        + link("#trabajo", "Ver posibilidades", "text-link", False),
    )
    + f"""<section class="section work-services" id="trabajo"><div class="section-heading"><h2>Crear y construir.<br>Con intención.</h2><p>Estas son las áreas de trabajo que presento en mi portafolio.</p></div><div class="service-list"><article><h3>Contenido de marca.</h3><div><p>Imágenes, piezas gráficas, carruseles y assets visuales generados con IA y editados con criterio profesional.</p>{link(DESIGN, "Ver portafolio de diseño")}</div></article><article><h3>Video y producción.</h3><div><p>Reels, anuncios, personajes y contenido audiovisual con herramientas de IA generativa.</p>{link(VIDEO, "Ver portafolio de video")}</div></article><article><h3>Automatización de procesos.</h3><div><p>Flujos con n8n, Make, Zapier y APIs para reducir pasos manuales: documentos, marketing y procesos operativos.</p>{link(WA, "Hablar de un proceso")}</div></article></div></section><section class="section work-case"><div class="section-heading"><h2>De un prompt<br>a contenido de marca.</h2><div><p>Florencia muestra un proceso de creación: imagen, animación y video UGC con un avatar generado con IA.</p>{link("/contenido-ia/#ejemplo", "Explora la demostración")}</div></div>{video()}</section><div class="section legacy-results">{results}</div><section class="section split-note"><h2>Empecemos por<br>la tarea correcta.</h2><div><p>Cuéntame qué quieres crear, qué proceso repites y cómo trabajas ahora. Con ese contexto podemos hablar de una solución y de lo que habría que comprobar.</p>{link(WA, "Escríbeme por WhatsApp", "button")}</div></section>"""
)
page(
    "/trabaja-conmigo/",
    "IA para tu proyecto",
    "Contenido de marca, video y automatización con IA. Conoce el trabajo de Juan Uribe y habla de tu proyecto.",
    work,
    active="/trabaja-conmigo/",
)

# Learning pages: actual small practices, not fictitious paid courses.
LESSONS = {
    "llms": {
        "title": "Una buena respuesta empieza por el contexto.",
        "intro": "Un LLM es un modelo que trabaja con lenguaje. Puede ayudar a desarrollar ideas, transformar texto y explorar opciones. Para usarlo bien, define la tarea y revisa lo que produce.",
        "outcome": "Un encargo más claro y una forma sencilla de evaluar la respuesta.",
        "needs": "Un asistente de texto y una tarea que conozcas. Empieza con material propio que puedas compartir.",
        "steps": [
            (
                "Define una tarea pequeña.",
                "Elige algo que puedas comprobar: resumir un texto, ordenar ideas para un post o proponer una estructura. «Haz mi estrategia» es difícil de evaluar; «propón tres estructuras para este post» es un punto de partida más concreto.",
            ),
            (
                "Añade el contexto que cambia la respuesta.",
                "Explica para quién es el resultado, qué material debe usar, qué límites tiene y cómo quieres recibirlo. Si falta información, pide que lo señale en lugar de completarla como si fuera un hecho.",
            ),
            (
                "Decide cómo vas a revisarlo.",
                "Comprueba que usa tu material, respeta el formato y distingue datos de suposiciones. Una respuesta convincente todavía puede ser incorrecta.",
            ),
            (
                "Cambia una cosa y compara.",
                "Ajusta una instrucción, vuelve a probar y compara con el mismo criterio. Guarda lo que mejoró para reutilizarlo en tareas parecidas.",
            ),
        ],
        "prompt": "Tarea: propón tres estructuras para una publicación educativa.\nContexto: quiero enseñar [tema] a [audiencia].\nMaterial: [pega aquí tus notas o ejemplo].\nLímites: usa solo el material y señala lo que falta.\nFormato: título, idea principal y tres pasos por estructura.\nRevisión: explica qué estructura es más fácil de llevar a la práctica y por qué.",
        "exercise": "Toma una idea que ya domines. Haz una petición sin contexto y otra con esta estructura. Señala dos diferencias y revisa si alguna respuesta inventó información.",
        "limit": "Si la respuesta contiene hechos que no están en tu material, busca una fuente adecuada antes de repetirlos. Pedir que revise su propia respuesta no garantiza que detecte todos los errores.",
        "next": ("/herramientas/#categoria-1", "Explorar asistentes de texto"),
    },
    "imagen-y-video": {
        "title": "Una imagen con intención.<br>Un video con continuidad.",
        "intro": "El proceso de Florencia permite ver cómo una imagen generada se convierte en animación y contenido estilo UGC. Empieza por una escena pequeña y decide qué debe mantenerse cuando llegue el movimiento.",
        "outcome": "Un brief visual y una lista de continuidad para pasar de imagen a video.",
        "needs": "Una idea de escena y una herramienta de imagen o video. La demostración de Florencia está disponible sin generar nada.",
        "steps": [
            (
                "Escribe el brief antes del prompt.",
                "Define sujeto, acción, entorno, iluminación y encuadre. «Una imagen bonita» admite demasiados resultados; una escena concreta te permite decidir si lo que sale sirve.",
            ),
            (
                "Genera una imagen y examínala.",
                "Revisa manos, objetos, texturas, proporciones y cualquier texto. No pases al video solo porque la primera impresión funciona. Corrige o elige una base que sostenga el siguiente paso.",
            ),
            (
                "Pide un movimiento pequeño.",
                "Describe una acción o movimiento de cámara. Anota qué debe permanecer igual: identidad, producto, ropa o escenario. Cuantos más cambios simultáneos pidas, más difícil será evaluar continuidad.",
            ),
            (
                "Edita el resultado con un propósito.",
                "Selecciona los fragmentos útiles, revisa transiciones y añade voz o subtítulos si ayudan a entender el mensaje. Mantén visibles los detalles importantes al adaptar el formato.",
            ),
        ],
        "exercise": "Mira los ejemplos de Florencia y escribe cinco elementos que se conservan entre la imagen y el video. Después redacta un brief propio de una escena y una acción de cinco segundos.",
        "limit": "La continuidad no está garantizada entre generaciones. Trata cada resultado como una propuesta que necesitas revisar, especialmente cuando representa un producto o una persona.",
        "next": ("/contenido-ia/#ejemplo", "Ver imagen, animación y UGC de Florencia"),
    },
    "automatizacion": {
        "title": "Antes del flujo,<br>entiende la tarea.",
        "intro": "Automatizar conecta pasos para que una tarea se ejecute con menos intervención manual. El primer trabajo no está en una herramienta: está en definir qué entra, qué debe pasar y qué salida necesitas.",
        "outcome": "Un mapa de una tarea, con entrada, decisiones, salida y un punto de revisión.",
        "needs": "Una tarea repetitiva que conozcas. Para la primera prueba, usa datos de ejemplo y una copia del proceso.",
        "steps": [
            (
                "Describe entrada y salida.",
                "Anota qué inicia la tarea y cómo sabrás que terminó. Por ejemplo: llega un texto de prueba y se guarda un resumen con un título y una fecha.",
            ),
            (
                "Dibuja los pasos en lenguaje normal.",
                "Escribe cada transformación o decisión antes de elegir nodos. Si una persona necesita adivinar qué hacer, probablemente falta una regla.",
            ),
            (
                "Conecta una versión pequeña.",
                "Empieza con un disparador manual, material de prueba y una salida fácil de inspeccionar. Herramientas como n8n permiten conectar esos pasos; algunas integraciones pueden requerir cuentas o un plan de pago.",
            ),
            (
                "Comprueba también los fallos.",
                "Prueba una entrada vacía, un formato inesperado y una ejecución repetida. Define cómo se detectará el error y qué acción necesita una revisión humana.",
            ),
        ],
        "exercise": "Elige una tarea que hagas a menudo. Dibuja tres pasos y señala cuál puede resolverse con una regla, cuál necesita una herramienta y cuál requiere tu criterio. No conectes todavía una acción que envíe o publique contenido real.",
        "limit": "Una automatización puede repetir un error muy rápido. Mantén un punto de revisión antes de acciones externas hasta que hayas probado entradas normales y excepciones.",
        "next": (
            "/herramientas/#categoria-5",
            "Explorar herramientas de automatización",
        ),
    },
    "musica": {
        "title": "Empieza por<br>lo que quieres escuchar.",
        "intro": "La generación musical sirve para explorar ideas, estilos y estructuras. Un encargo musical claro te ayuda a escuchar con criterio, comparar versiones y decidir qué dirección seguir.",
        "outcome": "Una dirección musical y un registro de cambios para comparar versiones.",
        "needs": "Una idea propia y una herramienta de generación musical. Puedes empezar escribiendo el encargo, sin abrir una cuenta.",
        "steps": [
            (
                "Define intención y contexto.",
                "¿La pieza acompaña un video, explora una canción o busca una textura? Anota qué debería hacer sentir y cuánto espacio necesita dejar para voz u otros sonidos.",
            ),
            (
                "Describe decisiones musicales.",
                "Piensa en ritmo, instrumentos, energía, voz o ausencia de voz y estructura. Es más útil pedir características que esperar que una referencia vaga produzca exactamente lo que tienes en mente.",
            ),
            (
                "Escucha versiones con la misma pregunta.",
                "Compara inicio, desarrollo, transiciones y final. Registra qué funciona para tu intención y qué te distrae. No confundas una sorpresa interesante con una pieza que ya está lista.",
            ),
            (
                "Itera sobre un cambio concreto.",
                "Ajusta energía, instrumentación o estructura, una a la vez. Guarda las versiones y tus notas para entender por qué prefieres una sobre otra.",
            ),
        ],
        "prompt": "Uso: acompañar un video de [tema].\nCarácter: [calmo, enérgico, tenso u otro].\nInstrumentos: [elige pocos elementos].\nVoz: [instrumental o descripción de la voz].\nEstructura: inicio [descripción], desarrollo [descripción], final [descripción].\nCriterio: debe dejar espacio para [narración, diálogo o el foco del video].",
        "exercise": "Redacta dos encargos para el mismo video: uno tranquilo y otro enérgico. Si generas versiones, escucha ambas junto al video y anota cuál sostiene mejor la intención.",
        "limit": "Las opciones, planes y permisos de uso dependen de la herramienta. Revisa sus condiciones para el uso que necesitas y conserva el origen de cada pieza.",
        "next": ("https://suno.com", "Explorar Suno"),
    },
}
for slug, record in LESSONS.items():
    title = next(t for s, t, _, _ in ROUTES if s == slug)
    steps = "".join(f"<li><h2>{t}</h2><p>{d}</p></li>" for t, d in record["steps"])
    snippet = ""
    if "prompt" in record:
        snippet = f'<section class="prompt-example"><div><h2>Una estructura para probar.</h2><p>Rellena los campos con tu propio contexto.</p></div><pre id="example-prompt"><code>{escape(record["prompt"])}</code></pre><button type="button" class="text-button copy-prompt" data-copy="example-prompt" hidden>Copiar estructura {ARROW}</button><p class="copy-status" role="status" aria-live="polite"></p></section>'
    illustration = (
        f'<figure class="lesson-visual"><img src="/assets/florencia.webp" width="670" height="1200" alt="Florencia, personaje generado con IA" loading="lazy"><figcaption>Florencia: la imagen de partida del ejemplo.</figcaption></figure>'
        if slug == "imagen-y-video"
        else ""
    )
    lesson = (
        breadcrumb(title, ("/aprender/", "Aprender"))
        + hero("Práctica abierta", record["title"], record["intro"])
        + f'<div class="lesson-layout"><aside class="lesson-sidebar" aria-label="Antes de empezar"><h2>Qué vas a practicar</h2><p>{record["outcome"]}</p><h2>Qué necesitas</h2><p>{record["needs"]}</p>{link("#practica", "Ir al ejercicio", "text-link", False)}{illustration}</aside><div class="lesson-body"><ol class="lesson-steps">{steps}</ol>{snippet}<section class="exercise" id="practica"><p class="overline">Tu turno</p><h2>Llévalo a una idea propia.</h2><p>{record["exercise"]}</p></section><section class="lesson-limit"><h2>Qué conviene revisar.</h2><p>{record["limit"]}</p></section><section class="lesson-next"><h2>Sigue explorando.</h2>{link(record["next"][0], record["next"][1])}{link("/recursos/", "Encuentra recursos para la práctica")}</section></div></div>'
        + follow(
            "¿Qué parte quieres<br>que expliquemos mejor?",
            "Lleva tu duda a Instagram. Puede ser el punto de partida de la siguiente práctica.",
        )
    )
    page(
        "/aprender/" + slug + "/",
        title,
        record["outcome"] + " Una práctica de IA con Juan Uribe.",
        lesson,
        active="/aprender/",
        scripts=("/assets/lesson.js",),
    )

# Keep original resource directories and their deep links.
for slug, source, title, desc, cls in [
    (
        "herramientas",
        "tools",
        "Herramientas IA que uso",
        "Herramientas que uso para pensar, crear y automatizar, organizadas por categoría.",
        "tools-page",
    ),
    (
        "contenido-ia",
        "guide",
        "Crear contenido con IA",
        "El proceso para crear imagen, video y contenido de marca con IA. Incluye la demostración de Florencia.",
        "guide-page",
    ),
]:
    body = (ROOT / f"_site-content/{source}-original.html").read_text()
    body = body.replace("hoy. probado", "hoy: probado")
    page(
        "/" + slug + "/",
        title,
        desc,
        breadcrumb(title, ("/recursos/", "Recursos")) + body,
        active="/recursos/",
        body="site-page resource-page " + cls,
        styles=(("/assets/guide-layout.css",) if source == "guide" else ())
        + ("/assets/resources.css", "/assets/legacy-polish.css"),
    )
# A dedicated fallback for GitHub Pages, excluded from indexing and sitemap.
page(
    "/404.html",
    "Volvamos a una buena idea",
    "Encuentra prácticas y recursos de IA en el sitio de Juan Uribe.",
    hero(
        "Esta dirección no está disponible",
        "Volvamos a<br>una buena idea.",
        "Puedes empezar por una práctica o explorar los recursos de la web.",
        link("/aprender/", "Ir a aprender", "button")
        + link("/recursos/", "Explorar recursos"),
    ),
)
error = ROOT / "404.html"
error.write_text(
    error.read_text().replace(
        "<title>", '<meta name="robots" content="noindex"><title>', 1
    )
)
PAGES.pop("/404.html")
# Structured data and discovery use public pages only.
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    + "".join(f"<url><loc>https://juanuribeia.com{p}</loc></url>" for p in PAGES)
    + "</urlset>"
)
(ROOT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\nDisallow: /brand-knowledge/\nDisallow: /_site-content/\nDisallow: /.agents/\nSitemap: https://juanuribeia.com/sitemap.xml\n"
)
(ROOT / "scripts/public-pages.json").write_text(
    json.dumps(PAGES, indent=2, ensure_ascii=False)
)
print("Generated", len(PAGES), "public pages")
