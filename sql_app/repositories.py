
from sqlalchemy.orm import Session

from . import models, schemas

class ItemRepo:
    """
    Asynchronous functions to perform various CRUD operations on items.
    """

    async def create(db: Session, item: schemas.ItemCreate):
        db_item = models.Item(name=item.name, price=item.price, description=item.description, store_id=item.store_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def fetch_by_id(db: Session, item_id):
        return db.query(models.Item).filter(models.Item.id == item_id).first()

    def fetch_by_name(db: Session, name):
        return db.query(models.Item).filter(models.Item.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Item).offset(skip).limit(limit).all()

    async def delete(db: Session, item_id):
        db_item = db.query(models.Item).filter_by(id=item_id).first()
        db.delete(db_item)
        db.commit()

    async def update(db: Session, item_data):
        updated_item = db.merge(item_data)
        db.commit()
        return updated_item


class StoreRepo:
    """
    Similarly defining the functions to perform the CRUD operations

    """
    async def create(db:Session,store: schemas.StoreCreate):
        db_store = models.Store(name = store.name)
        db.add(db_store)
        db.commit()
        db.refresh(db_store)
        return db_store
    
    def fetch_by_id(db: Session, _id: int):
        return db.query(models.Store).filter(models.Store.id == _id).first()
    def fetch_by_name(db:Session, name:str):
        return db.query(models.Store).filter(models.Store.name == name).first()
    def fetch_all(db:Session, skip: int = 0, limit: int =100):
        return db.query(models.Store).offset(skip).limit(limit).all()
    
    async def delete(db: Session,_id:int):
        db_store= db.query(models.Store).filter_by(id = _id).first()
        db.delete(db_store)
        db.commit()
        
    async def update(db: Session,store_data):
        db.merge(store_data)
        db.commit()
    
class OrderRepo:


    def fetch_all(db:Session, order: schemas.OrderCreate):
        return db.query(models.Order).all()

    def fetch_by_id(db:Session, id: int):
        return db.query(models.Order).filter_by(id=id).first()

    def create(db:Session, order: schemas.OrderCreate): 
        db_order = models.Order(name =  order.name, customer_id=order.customer_id, product_id=order.product_id, quantity=order.quantity)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order


    def delete(self, id: int) -> None:
        order = self.session.query(models.Order).filter_by(id=id).first()
        if order is not None:
            self.session.delete(order)
            self.session.commit()

class CustomerRepo:
    """
    Functions to perform CRUD operations on customers.
    """

    def create(db: Session, customer: schemas.CustomerCreate):
        db_customer = models.Customer(name=customer.name, phoneNumber=customer.phoneNumber)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer

    def fetch_by_id(db: Session, customer_id: int):
        return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

    def fetch_by_name(db: Session, name: str):
        return db.query(models.Customer).filter(models.Customer.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Customer).offset(skip).limit(limit).all()

    def delete(db: Session, customer_id: int):
        db_customer = db.query(models.Customer).filter_by(id=customer_id).first()
        db.delete(db_customer)
        db.commit()

    def update(db: Session, customer_data):
        db.merge(customer_data)
        db.commit()
