from fastapi import FastAPI     # http://localhost:8000/application-form
from app.routes import form

app = FastAPI()

app.include_router(form.router)
