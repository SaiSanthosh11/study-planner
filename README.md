# AI Study Planner

A production-ready AI-powered study planner for B.Tech students.

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env with your MongoDB URL, JWT secret, and OpenAI key

uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env: VITE_API_URL=http://localhost:8000

npm run dev
```

Open http://localhost:5173

---

## Environment Variables

### Backend `.env`
| Variable | Description |
|---|---|
| `MONGODB_URL` | MongoDB Atlas connection string |
| `JWT_SECRET` | Random secret string (min 32 chars) |
| `OPENAI_API_KEY` | OpenAI API key (optional — falls back to rule-based) |

### Frontend `.env`
| Variable | Description |
|---|---|
| `VITE_API_URL` | Backend URL |

---

## Deployment

### Backend → Render
1. Push `backend/` to GitHub
2. New Web Service on Render → connect repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard

### Frontend → Vercel
1. Push `frontend/` to GitHub
2. Import project on Vercel
3. Framework: Vite
4. Add `VITE_API_URL` pointing to your Render backend URL

### Database → MongoDB Atlas
1. Create free cluster at mongodb.com/atlas
2. Create database user
3. Whitelist `0.0.0.0/0` for Render/Vercel access
4. Copy connection string to `MONGODB_URL`

---

## API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Register user |
| POST | `/auth/login` | No | Login |
| GET/POST | `/subjects` | Yes | Manage subjects |
| GET/POST | `/marks` | Yes | Manage marks |
| GET | `/marks/analysis` | Yes | Performance analysis |
| POST | `/planner/generate-plan` | Yes | Generate study plan |
| GET | `/planner/current-plan` | Yes | Get active plan |
| POST | `/planner/reschedule` | Yes | Reschedule missed tasks |
| POST | `/progress/update-progress` | Yes | Mark task complete |
| GET | `/progress/progress` | Yes | Get analytics |

---

## AI Fallback

The system works fully without an OpenAI key using the built-in rule-based planner:
- Weak subjects (< 50%) get 3x time allocation
- Moderate subjects get 2x
- Revision sessions every 3rd day
- Missed tasks auto-redistributed to future days
