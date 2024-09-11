from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup has begun!")
    yield
    print("Shutdown has begun!")


app = FastAPI(lifespan=lifespan)
