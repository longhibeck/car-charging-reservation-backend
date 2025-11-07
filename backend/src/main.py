from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api.router import router as api_router
from database import create_tables

app = FastAPI(
    title="Car Charging Reservation System - API",
    description="API Backend for Car Charging System",
    version="0.1.0",
)

create_tables()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.include_router(api_router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
