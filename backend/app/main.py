from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import engine, Base
from app.routes import auth, social, post, monitor
from app.services.scheduler import start_scheduler
from app.services.metrics_scheduler import fetch_and_store_metrics

# -------------------------------------------------
# FastAPI app
# -------------------------------------------------
app = FastAPI(title="Social Scheduler AI API")

# -------------------------------------------------
# CORS Middleware (REQUIRED for React + OAuth)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite frontend
        "http://localhost:3000",  # CRA (optional)
    ],
    allow_credentials=True,
    allow_methods=["*"],        # IMPORTANT: allows OPTIONS
    allow_headers=["*"],        # IMPORTANT: allows Authorization
)

# -------------------------------------------------
# Routers
# -------------------------------------------------
app.include_router(auth.router)
app.include_router(social.router)
app.include_router(post.router)
app.include_router(monitor.router)

# -------------------------------------------------
# Database tables
# -------------------------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------------------------
# Root endpoint
# -------------------------------------------------
@app.get("/")
def root():
    return {"message": "Social Scheduler AI API is running"}

# -------------------------------------------------
# Startup events
# -------------------------------------------------
@app.on_event("startup")
def startup_event():
    """
    Runs once when the application starts.
    Starts:
    1. Post scheduler (every 60 seconds)
    2. Metrics scheduler (every 6 hours)
    """

    # 🔁 Scheduler for metrics (followers, analytics)
    metrics_scheduler = BackgroundScheduler()
    metrics_scheduler.add_job(
        fetch_and_store_metrics,
        trigger="interval",
        hours=6,
        id="metrics_scheduler",
        replace_existing=True,
        max_instances=1,
    )
    metrics_scheduler.start()

    # 🔁 Scheduler for scheduled posts (Facebook / Instagram)
    start_scheduler()

    print("✅ Schedulers started successfully")
