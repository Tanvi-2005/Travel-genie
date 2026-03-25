# 🌍 Travel Genie AI — Personalized Trip Planning Assistant

An AI-powered travel planner combining **Google Gemini AI**, **Machine Learning model comparison**, and a premium React dashboard.

---

## 🏗️ Project Structure

```
travel guide/
├── backend/
│   ├── main.py                  # FastAPI server (all API routes)
│   ├── database.py              # SQLAlchemy models (SQLite)
│   ├── schemas.py               # Pydantic request/response validation
│   ├── gemini_service.py        # Google Gemini AI integration
│   ├── ml_model_comparison.py   # 6 ML model training & evaluation
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # 🔑 API keys (add your Gemini key here)
│   └── start_backend.bat        # One-click backend launcher
└── frontend/
    ├── src/
    │   ├── App.jsx              # Main React application (4 pages)
    │   ├── index.css            # Premium design system
    │   └── main.jsx             # React entry point
    ├── index.html               # HTML shell
    ├── vite.config.js           # Vite config + API proxy
    ├── package.json
    └── start_frontend.bat       # One-click frontend launcher
```

---

## 🚀 Quick Start

### Step 1 — Add Your Gemini API Key

Edit `backend/.env`:
```
GEMINI_API_KEY=your_actual_key_here
```
> Get your free key at: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
> The app works **without** the key too — it will generate a basic itinerary as a fallback.

### Step 2 — Start the Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
Or double-click **`backend/start_backend.bat`**

Backend will start at: **http://localhost:8000**  
API Docs (Swagger): **http://localhost:8000/docs**

### Step 3 — Start the Frontend

```bash
cd frontend
npm install
npm run dev
```
Or double-click **`frontend/start_frontend.bat`**

Frontend will open at: **http://localhost:5173**

---

## 🤖 Machine Learning Features

On startup, the backend automatically:

1. **Generates** a synthetic travel dataset (2,000 records, 6 features)
2. **Trains** 6 ML models simultaneously:
   - Logistic Regression
   - Decision Tree
   - Random Forest
   - Gradient Boosting
   - SVM (RBF Kernel)
   - K-Nearest Neighbors
3. **Evaluates** each with: Accuracy, Precision, Recall, F1-Score
4. **Selects** the best model automatically for recommendations
5. **Stores** all results in SQLite database

### Dataset Features
| Feature | Description |
|---|---|
| `age` | Traveler age (18–70) |
| `budget` | Trip budget in USD ($500–$15,000) |
| `duration` | Trip length in days (1–30) |
| `group_size` | Number of travelers (1–8) |
| `travel_style` | 0=Adventure, 1=Relaxation, 2=Cultural, 3=Family |
| `preferred_climate` | 0=Tropical, 1=Temperate, 2=Cold, 3=Desert |

### Target: Destination Category
`beach` | `mountain` | `city` | `countryside` | `island`

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/plan-trip` | Plan a trip (ML + Gemini AI) |
| `GET` | `/api/trips` | Get all trip history |
| `GET` | `/api/trips/{id}` | Get specific trip |
| `DELETE` | `/api/trips/{id}` | Delete a trip |
| `GET` | `/api/ml/comparison` | Get ML model results |
| `POST` | `/api/ml/retrain` | Retrain all models |
| `GET` | `/api/dataset/stats` | Dataset statistics |

---

## 🖥️ Frontend Pages

| Page | Route | Description |
|---|---|---|
| 🏠 Home | `/` | Hero section + feature overview |
| 🗺️ Plan Trip | `/plan` | Trip form → ML prediction → Gemini itinerary |
| 📊 AI Results | `/results` | Model cards, bar charts, dataset info |
| 📋 History | `/history` | All saved trips with view/delete |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + Vanilla CSS |
| Backend | FastAPI + Python 3.10+ |
| Database | SQLite + SQLAlchemy |
| AI | Google Gemini AI (`gemini-pro`) |
| ML | scikit-learn (6 models) |
| ML Data | NumPy + Pandas (synthetic) |
