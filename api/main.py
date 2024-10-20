from fastapi import FastAPI

from routers import items
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(items.router)

@app.get("/")
def read_root():
    return {"Alumnes API"}
