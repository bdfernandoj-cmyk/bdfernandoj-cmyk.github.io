#!/usr/bin/env python3
"""Genera la web estática en docs/ (GitHub Pages sirve esa carpeta).

  python build.py

- docs/index.html, docs/ca/, docs/fr/        -> web de servicios (ES/CA/FR)
- docs/ejemplo/<slug>/, .../ca/, .../fr/      -> webs "esencial" generadas desde src/negocios/*.yaml
"""
from datetime import date
from pathlib import Path

import yaml
from jinja2 import ChainableUndefined, Environment, FileSystemLoader

RAIZ = Path(__file__).parent
OUT = RAIZ / "docs"
IDIOMAS = ["es", "ca", "fr"]
BASE_URL = "https://bdfernandoj-cmyk.github.io/"
env = Environment(loader=FileSystemLoader(RAIZ / "src/plantillas"), undefined=ChainableUndefined, autoescape=True)


def ruta_idioma(l):
    return "" if l == "es" else f"{l}/"


def escribir(rel, html):
    p = OUT / rel / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    return p


def main():
    textos = yaml.safe_load((RAIZ / "src/textos.yaml").read_text())
    negocios = [yaml.safe_load(p.read_text()) for p in sorted((RAIZ / "src/negocios").glob("*.yaml"))]
    demo = negocios[0]["slug"]
    hechos = []
    # Web de servicios
    rutas = {l: ruta_idioma(l) for l in IDIOMAS}
    for l in IDIOMAS:
        rel = "../" if l != "es" else ""
        demo_ruta = f"ejemplo/{demo}/{ruta_idioma(l)}"
        html = env.get_template("servicios.html.j2").render(
            t=textos[l], d=textos["datos"], idiomas=IDIOMAS, rutas=rutas, rel=rel,
            base_url=BASE_URL, demo_ruta=demo_ruta, anyo=date.today().year)
        hechos.append(escribir(ruta_idioma(l), html))
    # Web de servicios v3 (propuesta, solo castellano por ahora) en docs/nueva/
    html = env.get_template("servicios4.html.j2").render(
        t=textos["es"], v=textos["es"]["v3"], d=textos["datos"], rel="../",
        demo_ruta=f"ejemplo/{demo}/", anyo=date.today().year)
    hechos.append(escribir("nueva/", html))
    # Webs esencial de cada negocio
    for n in negocios:
        for l in IDIOMAS:
            if l not in n["textos"]:
                continue
            base = f"ejemplo/{n['slug']}/"
            # rutas relativas entre idiomas del propio negocio
            prof = "../" if l != "es" else ""
            rutas_n = {k: prof + ruta_idioma(k) if k != "es" else (prof or "./") for k in IDIOMAS}
            img_dir = OUT / base / "img"
            grandes = {p.name[:-len("-1600.webp")] for p in img_dir.glob("*-1600.webp")}
            html = env.get_template(n.get("plantilla", "esencial") + ".html.j2").render(
                e=n["estilo"], n=n, t=n["textos"][l], idiomas=[k for k in IDIOMAS if k in n["textos"]],
                rutas=rutas_n, anyo=date.today().year, img=prof + "img/", grandes=grandes,
                credito_url=("../../../" if l != "es" else "../../") + ruta_idioma(l))
            hechos.append(escribir(base + ruta_idioma(l), html))
        # Variantes de estilo para elegir (solo castellano): ejemplo/<slug>/estilos/<clave>/
        for k, v in (n.get("estilos_demo") or {}).items():
            nv = {**n, "colores": v["colores"]}
            html = env.get_template("esencial.html.j2").render(
                e=v["estilo"], n=nv, t=n["textos"]["es"], idiomas=["es"], rutas={"es": "../../"},
                anyo=date.today().year, img="../../img/", grandes=grandes, credito_url="../../../../")
            hechos.append(escribir(f"ejemplo/{n['slug']}/estilos/{k}/", html))
    (OUT / ".nojekyll").write_text("")
    for h in hechos:
        print("ok", h.relative_to(RAIZ))


if __name__ == "__main__":
    main()
