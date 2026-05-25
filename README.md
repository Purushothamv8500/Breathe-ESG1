# ESG Data Ingestion & Review System

Enterprise carbon/emissions data ingestion, normalization, and analyst review for **SAP**, **utility electricity**, and **corporate travel** sources.

## Stack

- **Backend:** Django 4.2 + Django REST Framework (SQLite)
- **Frontend:** React 18 + Vite + Tailwind CSS + Axios + Recharts
- **Multi-tenant:** `X-Client-Id` header on every API call

## Quick start

### Backend (required — start this first)

```powershell
# From project root (easiest):
.\start-backend.ps1

# Or manually:
cd backend
.\venv\Scripts\python manage.py runserver 8001
```

API base: `http://127.0.0.1:8001/api/` (port **8001** — avoid conflict with other apps on 8000)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

UI: `http://127.0.0.1:5173` (proxies `/api` → Django on **8001**)

**Important:** Start the backend before the frontend. If you see "Backend not connected", run `.\start-backend.ps1` then hard-refresh the browser.

### Frontend with a deployed backend

If the Django API is already hosted (Render, Railway, Azure, etc.):

1. Copy `frontend/.env.production.example` → `frontend/.env.production`
2. Set `VITE_API_BASE_URL` to your live API root, e.g. `https://your-api.example.com/api`
3. Build and deploy:

```bash
cd frontend
npm run build
```

Deploy `frontend/dist/` (Vercel, Netlify, Cloudflare Pages). On the host, set **`VITE_API_BASE_URL`** in build settings (baked in at build time).

Verify the API:

```bash
curl -H "X-Client-Id: acme" https://your-api.example.com/api/dashboard/
```

### Frontend pages

- **Dashboard** — KPI cards, source/status charts, data quality panel
- **Records** — filterable data grid + right-side detail drawer (raw vs normalized)
- **Pending Reviews** — card-based work queue with quick approve/reject

### Default tenants

| client_id | Name |
|-----------|------|
| `acme` | Acme Corp |
| `globex` | Globex Industries |

Use the client dropdown in the UI or header: `X-Client-Id: acme`

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/ingest/sap/` | Upload SAP CSV/JSON |
| POST | `/api/ingest/utility/` | Upload utility CSV/JSON |
| POST | `/api/ingest/travel/` | Upload travel CSV/JSON |
| GET | `/api/records/` | List normalized records (filters: `source`, `status`, `scope`) |
| GET | `/api/records/{id}/` | Record detail (raw + normalized) |
| POST | `/api/records/{id}/approve/` | Approve record |
| POST | `/api/records/{id}/reject/` | Reject record |
| GET | `/api/dashboard/` | Summary stats |

### Ingest example (curl)

```bash
curl -X POST http://127.0.0.1:8000/api/ingest/sap/ \
  -H "X-Client-Id: acme" \
  -F "file=@../samples/sap_fuel_procurement.csv"
```

## Project structure

```
backend/
  config/          # Django settings & URLs
  tenants/         # Tenant model
  records/         # Raw + normalized models, review API
  ingestion/       # Parsers, normalizers, ingest views
  scripts/seed.py  # Sample data loader
frontend/src/      # React analyst UI
samples/           # Example CSV files for all 3 sources
```

## Documentation

- [MODEL.md](MODEL.md) — data model & traceability
- [DECISIONS.md](DECISIONS.md) — assumptions
- [TRADEOFFS.md](TRADEOFFS.md) — scope limits
- [SOURCES.md](SOURCES.md) — real-world format assumptions

## Admin

```bash
python manage.py createsuperuser
```

Open `http://127.0.0.1:8000/admin/`
