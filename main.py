from fastapi import FastAPI                  # http://localhost:8000/application-form
from app.routes import user_input_form

app = FastAPI()

app.include_router(user_input_form.router)
