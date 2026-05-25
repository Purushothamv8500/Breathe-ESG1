# Deploy Breathe ESG (backend + frontend)

## URLs

| App | Host | URL |
|-----|------|-----|
| Backend API | Render | https://breathe-esg1.onrender.com |
| Frontend UI | Vercel (recommended) | Set after deploy — e.g. `https://breathe-esg1.vercel.app` |

---

## 1. Push code to GitHub

```powershell
cd "C:\Users\sanka\OneDrive\Desktop\Breathe ESG1"
git add .
git commit -m "Add Render and Vercel deployment config"
git push origin main
```

(Use your branch name if not `main`.)

---

## 2. Redeploy backend (Render)

1. Open [Render Dashboard](https://dashboard.render.com) → service **breathe-esg1**
2. **Settings** → confirm:
   - **Root Directory:** `backend`
   - **Build Command:** `./build.sh` (or `pip install -r requirements.txt && python manage.py migrate`)
   - **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
3. **Environment** variables:

   | Key | Value |
   |-----|--------|
   | `DEBUG` | `false` |
   | `SECRET_KEY` | (generate a random string) |
   | `ALLOWED_HOSTS` | `breathe-esg1.onrender.com,.onrender.com` |
   | `FRONTEND_URL` | Your Vercel URL after step 3 (no trailing slash) |

4. Click **Manual Deploy** → **Deploy latest commit**

Verify: https://breathe-esg1.onrender.com/api/dashboard/ with header `X-Client-Id: acme`

---

## 3. Deploy frontend (Vercel)

1. Go to [vercel.com](https://vercel.com) → **Add New Project** → import `Purushothamv8500/Breathe-ESG1`
2. **Root Directory:** `frontend`
3. **Environment Variables** (Production):

   | Name | Value |
   |------|--------|
   | `VITE_API_BASE_URL` | `https://breathe-esg1.onrender.com/api` |

4. Deploy

5. Copy your Vercel URL (e.g. `https://breathe-esg1.vercel.app`)

6. Back on **Render** → set `FRONTEND_URL` = that URL → redeploy backend once

Open the Vercel URL — the dashboard should load and call the Render API.

---

## Alternative: Netlify (frontend)

- Base directory: `frontend`
- Build: `npm run build`
- Publish: `dist`
- Env: `VITE_API_BASE_URL=https://breathe-esg1.onrender.com/api`
- Add `public/_redirects` (already in repo) for SPA routing

---

## Local production build test

```powershell
cd frontend
npm run build
npm run preview
```

Uses `frontend/.env.production` → Render API.
