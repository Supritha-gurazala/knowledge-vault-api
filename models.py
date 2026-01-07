from pydantic import BaseModel 
from datetime import datetime 

class ItemCreate(BaseModel): 
	title: str 
	content: str 
	type: str
	
class Item(ItemCreate): 
	id: int 
	created_at: datetime