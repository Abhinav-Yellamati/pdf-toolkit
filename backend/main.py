from app.main import app


if __name__ == "__main__":
    import os

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8001")),
        reload=os.getenv("RELOAD", "0") == "1",
    )
