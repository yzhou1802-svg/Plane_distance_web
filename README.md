# Plane–Point Distance Calculator

A web app that computes the perpendicular distance from a point to a plane in 3D space.

## Features

- **Parameterform** — define the plane by three points lying on it
- **Koordinatenform** — define the plane as ax + by + cz = d
- **Normaleform** — define the plane by a normal vector and a point on the plane

All three modes return the exact distance, the foot of the perpendicular, the normal vector,
and the plane equation in Koordinatenform.

## Tech stack

- **Backend**: Python 3 + Flask, REST JSON API
- **Frontend**: Vanilla HTML/CSS/JavaScript, single-page, no build step required
- **Production server**: Gunicorn

## Local development

```bash
git clone <repo-url>
cd plane_distance_web

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

## Deployment

The app is deployed on [Render](https://render.com) as a Python web service.
Render runs the app using Gunicorn — no Procfile or Docker configuration is required.

Start command used on Render:
```
gunicorn app:app
```

## License

MIT — see [LICENSE](LICENSE).
