from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import routes


description = """
--------------
This is a demo for testing purpose only

All the CRUD operations are being performed for each functionality.
Please refer below listed routes/endpointer for better understanding on how are routes working.

**Note**: Feel free to ask any question regarding below routes.

Thanks :)
"""

app = FastAPI(
    title="FastAPI Demo",
    description=description,
    summary="FastAPI Demo for Learning",
    version="1.0.0",
    contact={
        "name": "Umang Bhadja",
        "url": "http://localhost:8000",
        "email": "umang@simprosys.com"
    }
)

origins = [
    "http://localhost:3000",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


app.include_router(routes.product_router, prefix="", tags=["products"])

