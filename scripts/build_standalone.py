"""Genera app/gre-movil.html: la app entera en UN solo archivo.

`app/index.html` carga los datos con <script src="../data/data.js">, lo que obliga a
conservar la carpeta al lado. En el móvil eso no vale: lo que se manda por AirDrop,
Drive o WhatsApp tiene que ser un archivo suelto que abra al tocarlo.

Este script mete data.js dentro del HTML y escribe el resultado aparte. No toca
`app/index.html`, que sigue siendo el que se edita.

    python3 scripts/build_standalone.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "app" / "index.html"
DATA = ROOT / "data" / "data.js"
OUT = ROOT / "app" / "gre-movil.html"

TAG = '<script src="../data/data.js"></script>'


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    if TAG not in html:
        print(f"ERROR: no encuentro {TAG!r} en {SRC.relative_to(ROOT)}.")
        print("       Si cambió la forma de cargar los datos, actualiza este script.")
        return 1

    data = DATA.read_text(encoding="utf-8")
    # Un "</script>" dentro del JSON cerraría la etiqueta antes de tiempo.
    data = data.replace("</script", "<\\/script")

    out = html.replace(TAG, "<script>\n" + data + "\n</script>")
    OUT.write_text(out, encoding="utf-8")

    kb = OUT.stat().st_size / 1024
    print(f"escrito: {OUT.relative_to(ROOT)}  ({kb:.0f} KB, un solo archivo)")
    print("         mándatelo al móvil y ábrelo: no necesita servidor ni carpeta al lado.")
    return 0


raise SystemExit(main())
