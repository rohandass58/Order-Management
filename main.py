from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sql_app import models
from db import get_db, engine
import sql_app.models as models
import sql_app.schemas as schemas
from sql_app.repositories import ItemRepo, StoreRepo, OrderRepo, CustomerRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Sample FastAPI Application",
    description="Sample FastAPI Application with Swagger and Sqlalchemy",
    version="1.0.0",)

""" 
Creating the APIs POST,GET, PUSH, DELETE, PUT 
"""


models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)

def validation_exception_handler(request, err):
    """ Handling the exception"""
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.post("/items", tags= ["Item"], response_model= schemas.Item, status_code=201)
async def create_item(item_request: schemas.ItemCreate, db:Session= Depends(get_db)):
    """ 
    Handling the post request to send the data over the network
    """
    db_item = ItemRepo.fetch_by_name(db, name= item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exist")
    return await ItemRepo.create(db=db,item= item_request)

@app.get("/items/", tags=["Item"], response_model=List[schemas.Item])
def get_all_items(name:Optional[str] = None, db: Session= Depends(get_db)):
    """ 
    Handling the get  request to display all the itens
    """

    if name:
        items = []
        db_item = ItemRepo.fetch_by_name(db,name)
        items.append(db_item)
        return items
    else:
        return ItemRepo.fetch_all(db)
    
@app.get('items/{item_id}', tags = ["Item"],response_model=List[schemas.Item])
def get_item(item_id:int, db: Session= Depends(get_db)):

    """
    Retrieving the particular item based on the id 
    """
    db_item = ItemRepo.fetch_by_id(db,id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item


@app.delete('/items/{item_id}', tags=["Item"])
async def delete_item(item_id: int,db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db,item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await ItemRepo.delete(db,item_id)
    return "Item deleted successfully!"

@app.put('/items/{item_id}', tags=["Item"],response_model=schemas.Item)
async def update_item(item_id: int,item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an Item stored in the database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.name = update_item_encoded['name']
        db_item.price = update_item_encoded['price']
        db_item.description = update_item_encoded['description']
        db_item.store_id = update_item_encoded['store_id']
        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")
    
    
@app.post('/stores', tags=["Store"],response_model=schemas.Store,status_code=201)
async def create_store(store_request: schemas.StoreCreate, db: Session = Depends(get_db)):
    """
    Create a Store and save it in the database
    """
    db_store = StoreRepo.fetch_by_name(db, name=store_request.name)
    print(db_store)
    if db_store:
        raise HTTPException(status_code=400, detail="Store already exists!")

    return await StoreRepo.create(db=db, store=store_request)

@app.get('/stores', tags=["Store"],response_model=List[schemas.Store])
def get_all_stores(name: Optional[str] = None,db: Session = Depends(get_db)):
    """
    Get all the Stores stored in database
    """
    if name:
        stores =[]
        db_store = StoreRepo.fetch_by_name(db,name)
        print(db_store)
        stores.append(db_store)
        return stores
    else:
        return StoreRepo.fetch_all(db)
    
@app.get('/stores/{store_id}', tags=["Store"],response_model=schemas.Store)
def get_store(store_id: int,db: Session = Depends(get_db)):
    """
    Get the Store with the given ID provided by User stored in database
    """
    db_store = StoreRepo.fetch_by_id(db,store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found with the given ID")
    return db_store

@app.delete('/stores/{store_id}', tags=["Store"])
async def delete_store(store_id: int,db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_store = StoreRepo.fetch_by_id(db,store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found with the given ID")
    await StoreRepo.delete(db,store_id)
    return "Store deleted successfully!"

@app.post("/orders", tags=["Order"], response_model=schemas.Order, status_code=201)
async def create_order(order_request: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create an Order and save it in the database
    """
    db_order = OrderRepo.fetch_by_name(db, name=order_request.name)
    if db_order:
        raise HTTPException(status_code=400, detail="Order already exists!")

    return await OrderRepo.create(db=db, order=order_request)

@app.post("/customers", tags=["Customer"], response_model=schemas.Customer, status_code=201)
async def create_customer(customer_request: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a Customer and save it in the database
    """
    db_customer = CustomerRepo.fetch_by_name(db, name=customer_request.name)
    if db_customer:
        raise HTTPException(status_code=400, detail="Customer already exists!")

    return await CustomerRepo.create(db=db, customer=customer_request)


@app.get("/customers", tags=["Customer"], response_model=List[schemas.Customer])
def get_all_customers(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Customers stored in the database
    """
    if name:
        customers = []
        db_customer = CustomerRepo.fetch_by_name(db, name)
        customers.append(db_customer)
        return customers
    else:
        return CustomerRepo.fetch_all(db)


@app.get("/customers/{customer_id}", tags=["Customer"], response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Get the Customer with the given ID stored in the database
    """
    db_customer = CustomerRepo.fetch_by_id(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found with the given ID")
    return db_customer


@app.delete("/customers/{customer_id}", tags=["Customer"])
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Delete the Customer with the given ID stored in the database
    """
    db_customer = CustomerRepo.fetch_by_id(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found with the given ID")
    await CustomerRepo.delete(db, customer_id)
    return "Customer deleted successfully!"


@app.put("/customers/{customer_id}", tags=["Customer"], response_model=schemas.Customer)
async def update_customer(customer_id: int, customer_request: schemas.Customer, db: Session = Depends(get_db)):
    """
    Update a Customer stored in the database
    """
    db_customer = CustomerRepo.fetch_by_id(db, customer_id)
    if db_customer:
        update_customer_encoded = jsonable_encoder(customer_request)
        db_customer.name = update_customer_encoded["name"]
        db_customer.phoneNumber = update_customer_encoded["phoneNumber"]
        return await CustomerRepo.update(db=db, customer_data=db_customer)
    else:
        raise HTTPException(status_code=400, detail="Customer not found with the given ID")

    

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)