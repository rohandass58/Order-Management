from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

class ItemBase(BaseModel):
    name : str
    price: float
    description: Optional[str] =  None

#value of optional_str variable will be either any string or None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True

class StoreBase(BaseModel):
    name: str

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    customer_id: int
    product_ids: List[int]
    total_price: float
    quantity: int
    created_at: datetime
    updated_at: datetime

class OrderCreate(BaseModel):
    name: str
    customer_id: int
    product_id: int
    quantity: int

class CustomerBase(BaseModel):
    name: str
    phoneNumber: int


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True







