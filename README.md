# Mark's Golf Map ⛳

A live "you are here" map for the **Genesis Scottish Open** at The Renaissance Club,
built from a photo of the official spectator course board. Open it on an iPhone,
allow location, and a blue dot tracks you around the course on the actual event map.

**Everything is inlined in a single file — `index.html` works offline** (handy when
the mobile signal dies in the crowds). Save it to the Files app or host it anywhere
over HTTPS (geolocation requires a secure origin).

## Features

- **Live GPS dot** with accuracy ring and compass heading cone
- **Follow-me mode** with screen wake-lock (tap the target button; drag the map to pause it)
- **Tap anywhere** to get the distance from where you stand, in yards
- **Quick-jump chips** — Clubhouse, 18th Green, Fanzone, beach holes 4–7, entrances
- **Fine-tune calibration** (pencil button): stand somewhere recognisable, drag the map
  so the dot is exactly there, tap Done. Stored on the device; Reset to undo.
- **Off-map arrow** points toward you when your position is outside the visible map
- **Demo mode** — append `?demo=1` to simulate a walk of the course from the sofa

## How the map was georeferenced

The course board is an artist's rendering, not a true orthophoto, so a plain
rotation/scale doesn't fit it. The pipeline (see `tools/`):

1. Cropped and cleaned the board photo (`assets/course-map.jpg`, 2200×1310)
2. Pulled the real course geometry from OpenStreetMap (18 hole lines, greens,
   coastline, roads) and stitched Esri satellite tiles for visual matching
3. Identified 8 anchor points (greens, clubhouse features) on both the board
   and the real world
4. Fitted a **similarity transform (with reflection — image y points down)**
   plus a **smoothed thin-plate-spline** to absorb the board's artistic warp
   (~±90 px regionally). Anchor residuals after fitting: under 5 px.
5. `tools/transform_final.json` holds the fitted parameters; the app evaluates
   the same math in ~20 lines of JS.

Accuracy over the playing areas is roughly 20–50 m — good enough to know which
fairway you're standing on; use the calibration nudge on site to tighten it further.

## Rebuilding

```
python3 tools/build.py
```

Inputs: `tools/app_body.html` (app source), `tools/leaflet.{js,css}` (Leaflet 1.9.4),
`tools/transform_final.json`, `assets/course-map.jpg`.
Outputs: `index.html` (standalone) and `artifact.html` (body fragment for hosts
that provide their own HTML skeleton).

## Credits

Course board © Genesis Scottish Open / DP World Tour. Geodata © OpenStreetMap
contributors (ODbL). Satellite reference imagery © Esri. Map engine: Leaflet.
