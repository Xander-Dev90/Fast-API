from sqlmodel import select as sql_select

from fastapi import APIRouter, HTTPException, status
from ..models import Customer, CustomerCreate, Transaction, Invoice, CustomerUpdate
from ..db import SessionDep



router = APIRouter()

@router.get("/customers", response_model=list[Customer])
async def list_customers(session: SessionDep):
    customers = session.exec(sql_select(Customer)).all()
    return customers

@router.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_db

@router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer_data: CustomerCreate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer_data.model_dump().items():
        setattr(customer_db, key, value)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db 

@router.delete("/customers/{customer_id}", response_model=Customer)
async def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return customer

@router.patch("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep
):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer_data.model_dump(exclude_unset=True).items():
        setattr(customer, key, value)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer
