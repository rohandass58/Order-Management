from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base



class Item(Base):


    """
    Creating the Item class to store the details of the Item 
    it includes id, name, price, store_id

    
    """
    __tablename__="items"

    id = Column(Integer, primary_key= True, index = True)
    name = Column(String(80), nullable= False, unique= True, index = True)
    price= Column(Float(precision=2), nullable =  False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable= False)

    def __repr__(self):
        return 'ItemModel(name = %s, price=%s,store_id=%s)' %(self.name, self.price, self.id)

class Store(Base):

    """
    Creating the Store class to store  the details of the Store
    It stores the name, items along with the id
    the items column have the relationship with the column store_id 
    
    """
    __tablename__ = "stores"

    id =  Column(Integer, primary_key=True, index = True)
    name = Column(String(80), nullable= False,unique = True)
     #primary_join  is used for the one to many relationship
    items =  relationship("Item", primary_join="Store.id == Item.store_id", cascade="all, delete-orphan")

    def __repr__(self):
        return 'Store(name = %s)' %(self.name)



