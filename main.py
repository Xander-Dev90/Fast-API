from fastapi import FastAPI
from db import create_all_tables
from venv_clean.app.main import app as api_router
from models import Customer, CustomerCreate, Transaction, Invoice, CustomerUpdate

# Crear la aplicación FastAPI
app = FastAPI(lifespan=create_all_tables)

# Incluir el router de la API
app.include_router(api_router)
