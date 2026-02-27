import zoneinfo
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from models import Customer,CustomerCreate ,Transaction, Invoice, CustomerUpdate
from db import SessionDep, create_all_tables
from sqlmodel import select



app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"message": "Hola, Persancho!"}


country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}


@app.post("/customers", response_model=Customer)

async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer(**customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers/{customer_id}", response_model=Customer, status_code = status.HTTP_201_CREATED)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
             )
    customer_data_dict = customer_db.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@app.delete("/customers/{customer_id}", response_model=Customer)
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    return customer_db


@app.put("/customers_update/{id}")
async def update_customer(id: int, customerUpdate: CustomerUpdate, session: SessionDep):  
    customer = session.get(Customer, id)    
    if not customer:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    else:
        data = customerUpdate.model_dump()
         
        for key, value in data.items():  
                      setattr(customer, key, value)        
                      session.commit()
                      session.refresh(customer) 
                      return customer
        

@app.get("/customers", response_model=list[Customer])
async def list_customers(session: SessionDep):
    customers = session.exec(select(Customer)).all()
    return customers

@app.post("/transactions")
async def create_transation(transaction_data: Transaction, session: SessionDep):
    return transaction_data


@app.post("/invoices", response_model=Invoice)
async def create_invoice(invoice_data: Invoice):
    breakpoint()
    return invoice_data