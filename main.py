from fastapi import FastAPI
from database import engine, Base
from user.api import router as auth_router
from product.api import router as product_router


app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/status/", response_model=dict)
async def status():
    # check if the database is connected
    try:
        engine.connect()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(product_router, tags=["Products"])