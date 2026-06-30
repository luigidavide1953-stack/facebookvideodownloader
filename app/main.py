from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Facebook Extractor API",
    description="A powerful API to extract video information and download links from Facebook.",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Facebook Extractor API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
