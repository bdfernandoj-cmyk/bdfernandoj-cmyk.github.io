# Web de servicios de Fernando + plantilla "Web esencial"

```bash
pip install jinja2 pyyaml
python build.py          # genera docs/ (GitHub Pages sirve esa carpeta)
```

- `src/textos.yaml`: textos ES/CA/FR y datos (precios, contacto).
- `src/plantillas/servicios.html.j2`: la web de servicios.
- `src/plantillas/esencial.html.j2`: la plantilla "Web esencial" (una página, móvil primero).
- `src/negocios/*.yaml`: una ficha por negocio → `docs/ejemplo/<slug>/`. `cal-ginebro` es ficticio.

Referencias de diseño elegidas: ver `REFERENCIAS.md`.
