import uvicorn

from settings import settings_obj

if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        log_level="info",
        host=settings_obj.SERVER_HOST,
        port=settings_obj.SERVER_PORT,
        reload=True,
    )
