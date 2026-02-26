from pydantic import BaseModel

from sqlmodel import SQLModel, Field


class CustomerBase(SQLModel):
    name: str = Field(index=True)
    description: str | None = Field(index=True)
    email: str = Field(index=True)
    age: int = Field(index=True)

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)



class Transaction(BaseModel):
    id: int
    ammount: int
    description: str


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)