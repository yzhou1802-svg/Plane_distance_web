# CLAUDE.md — Plane–Point Distance Calculator

## Project overview
Flask web app that computes the perpendicular distance from a 3D point to a plane.
Supports three plane representations: Parameterform, Koordinatenform, Normaleform.
Originated from a CLI Python script; converted to a single-page web app with a REST API.

## Stack
- **Backend**: Python 3 + Flask (no ORM, no DB, no auth)
- **Frontend**: Single HTML file (`templates/index.html`) — vanilla JS, no build step, no npm
- **Only dependency**: `flask` (install: `pip install flask`)

## Run
```bash
cd plane_distance_web
python app.py          # dev server at http://localhost:5000
```

## File map
```
app.py              Flask routes + input validation (3 POST endpoints)
calculator.py       Pure math — no I/O, no Flask imports
templates/
  index.html        Full frontend: tabs, dark-theme CSS, fetch-based JS
```

## API
All endpoints: `POST /api/<mode>`, JSON in/out.

| Endpoint | Required JSON fields |
|---|---|
| `/api/parameterform` | `p1, p2, p3, point` — each `[x,y,z]` |
| `/api/koordinatenform` | `a, b, c, d` (floats) + `point` `[x,y,z]` |
| `/api/normaleform` | `normal [x,y,z]`, `plane_point [x,y,z]`, `point [x,y,z]` |

Response shape:
```json
{
  "status": "ok" | "on_plane" | "degenerate" | "error",
  "distance": 4.58,
  "intersection": [1.0, 2.0, 3.0],
  "normal_vector": [0, 0, 1],
  "koordinatenform": "z = 0"
}
```
On error: HTTP 400 + `{"status":"error","message":"..."}`.

## calculator.py conventions
- All public functions return a `dict` — never raise, never print.
- Internal helpers are prefixed `_` (not part of the API contract).
- Vectors and points are plain `list[float]` of length 3.
- Edge cases: zero normal → `"error"`, point on plane (dist < 1e-10) → `"on_plane"`.
- Use `math.sqrt` for distance — do **not** use `math.exp(0.5 * math.log(...))`.

## Frontend conventions
- All state is local to the page — no localStorage, no frameworks.
- `val(id)` reads + validates a number input; throws `Error` with a human message on bad input.
- Result rendering is fully in `showResult(panelId, data)` — keep all display logic there.
- CSS custom properties (`:root`) drive the color theme — edit there first for visual changes.

## Testing
No test runner configured. Run ad-hoc math checks directly:
```bash
python -c "import calculator; print(calculator.calculate_koordinatenform(0,0,1,0,[0,0,3]))"
```

## Deployment target
Production: Nginx + Gunicorn (not Flask dev server).
- Keep Flask app stateless — no in-process state between requests.
- All secrets/config go in environment variables, not hardcoded.
- Gunicorn entry point: `gunicorn app:app` (the `if __name__ == '__main__'` block is dev-only).

## Planned features (design for, don't implement yet)
- **2D visualization**: render the plane + point + foot of perpendicular in-browser.
  Likely canvas-based or a lightweight lib (e.g. Plotly.js or Three.js). Keep it optional/lazy-loaded.
  The API already returns `intersection` and `normal_vector` — sufficient data for rendering.
- **Multilingual UI**: target at minimum German + English (Chinese optional).
  Don't hardcode display strings into HTML — use a JS `i18n` map from the start when adding new strings.

## Public-facing quality bar
This app is intended for end users, not just local use:
- Error messages must be human-readable (no raw Python tracebacks to the client).
- Input edge cases (empty fields, non-numeric, collinear points) must all show clear UI feedback.
- app.py already catches `ValueError`/`TypeError` and returns HTTP 400 — maintain this pattern.
- When adding features, test the full browser flow, not just the API.
