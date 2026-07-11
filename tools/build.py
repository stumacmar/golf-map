#!/usr/bin/env python3
"""Build Mark's Golf Map into two self-contained files:
  - index.html     full standalone page (open directly in any browser)
  - artifact.html  body fragment for hosts that supply their own <html> skeleton
Everything (Leaflet, course image, georeference) is inlined — no network needed.
"""
import base64, json, pathlib

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent

body = (HERE / "app_body.html").read_text()
leaflet_js = (HERE / "leaflet.js").read_text()
leaflet_css = (HERE / "leaflet.css").read_text()
transform = json.loads((HERE / "transform_final.json").read_text())
img_b64 = base64.b64encode((ROOT / "assets" / "course-map.jpg").read_bytes()).decode()

body = body.replace("/*__LEAFLET_CSS__*/", leaflet_css)
body = body.replace("/*__LEAFLET_JS__*/", leaflet_js)
body = body.replace("/*__TRANSFORM_JSON__*/", json.dumps({
    "lat0": transform["lat0"], "lon0": transform["lon0"],
    "mlat": transform["mlat"], "mlon": transform["mlon"],
    "M": transform["M"], "t": transform["t"],
    "ctrl": transform["ctrl"], "w": transform["w"], "aff": transform["aff"],
}))
body = body.replace("/*__IMG_DATA__*/", json.dumps("data:image/jpeg;base64," + img_b64))

(ROOT / "artifact.html").write_text(body)

standalone = (
    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
    + "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
)
(ROOT / "index.html").write_text(standalone)
print("built: index.html (%.1f MB), artifact.html" % ((ROOT / "index.html").stat().st_size / 1e6))
