# LTA Track Access Planner

A React and FastAPI control centre for generating, inspecting, assuring, and exporting railway possession plans. The scheduling rules in `scheduler.py` are preserved; the former Streamlit presentation layer has been replaced by a versioned API and a responsive React interface.

## Architecture

```text
frontend/                 React + Vite user interface
  src/components/         Feature-specific dashboard views
  src/hooks/              Planner request state
  src/lib/                API and CSV adapters
backend/
  api/                    FastAPI routes
  services/               Validation, planning, analytics, serialization
  config.py               Required tables and scenario metadata
  models.py               API response contracts
scheduler.py              Existing scheduling domain engine (unchanged)
app.py                    ASGI entry point
legacy/streamlit_app.py   Previous UI retained as a migration reference
tests/                    Service-level regression tests
```

By default, the production browser loads the unchanged Python scheduler through Pyodide and runs it in a Web Worker. The uploaded CSVs never leave the user's device. For larger centrally hosted deployments, the same interface can call `POST /api/v1/plans` on the optional FastAPI service by setting `VITE_API_URL`.

## Run locally

Prerequisites: Python 3.11+ and Node.js 18+.

### 1. API

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload
```

The API runs at `http://127.0.0.1:8000`; interactive documentation is available at `/docs`.

### 2. React app

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The first plan run downloads the browser Python runtime and pandas, then executes the scheduler away from the UI thread. To use the FastAPI service instead, set `VITE_API_URL` to its `/api/v1` URL before starting or building the frontend.

## Input package

Exactly eight CSVs are required. Filenames may include extra text, but each must contain one of these identifiers:

- `01_LINES`
- `02_STATIONS`
- `03_SECTORS`
- `04_LOCATION_SUPPLY`
- `05_BUFFER_LOCATION`
- `06_PARAMETERS`
- `07_PROJECT_DETAILS`
- `08_ACTIVITY_DETAILS`

## Verification

```powershell
pip install -r requirements-dev.txt
pytest
cd frontend
npm run build
```

The service tests cover KPI parity, assurance rules, capacity aggregation, and upload-manifest validation.

## Production deployment

### Netlify frontend

The root [netlify.toml](netlify.toml) configures the `frontend` base directory, Vite build command, `dist` publish directory, Node version, and SPA fallback. The build copies `scheduler.py` into the published bundle and runs it inside a Web Worker, so `https://nebu1ax.netlify.app` does not require a server-side Python runtime.

Pushes to `main` trigger the linked Netlify deployment. After deployment, verify the homepage loads and generate a plan with all eight CSV tables.

### Optional hosted backend

For heavier workloads, deploy the included [Dockerfile](Dockerfile) to a container-capable Python host. Configure the backend origin:

```text
CORS_ORIGINS=https://nebu1ax.netlify.app
```

After deployment, confirm that this endpoint returns `{"status":"ok"}`:

```text
https://your-api-host.example/api/v1/health
```

Then add this optional variable in **Netlify → Project configuration → Environment variables**:

```text
VITE_API_URL=https://your-api-host.example/api/v1
```

When `VITE_API_URL` is absent, the application automatically uses the in-browser engine. When present on Netlify, it must be an HTTPS URL ending in `/api/v1`.
