from fastapi import FastAPI
from app.api.user_routes import router as user_router
from app.api.carRoutes import router as car_router
from app.core.database import Base, engine

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# include routes
app.include_router(user_router)
app.include_router(car_router)