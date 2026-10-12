from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name: str
    description :str| None = None
    price: float 
    tax : float | None = None


database = {}

number_of_ids = 1
def generate_id():
    global number_of_ids
    uid = number_of_ids
    number_of_ids +=1
    return uid


@app.get("/")
async def home():
    return {"message":"Store API Running"}


@app.post("/products/")
async def create_product(product: Product):
    uid = generate_id()
    database[uid] = product
    result= {"id": uid,**product.model_dump()}
    if product.tax is not None:
        result["price_with_tax"] = product.price+product.tax
    return result

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    if product_id not in database:
        return {"error":"product not found"}
    product = database[product_id]
    return {"id":product_id,**product.model_dump()}

@app.put("/products/{product_id}")
async def update_product(product_id: int,product: Product ):
    if product_id not in database:
        return {"error":"product not found"}
    database[product_id] = product
    return {"id":product_id,**product.model_dump()}


@app.get("/products/")
async def get_all_product(q:str|None= None,skip:int=0,limit: int = 10):
    result = []
    for pid,product in database.items():
        item = {"id":pid,**product.model_dump()}
        if q is not None:
            if q not in item["name"].lower():
                continue
        result.append(item)
    return result[skip:skip+limit]

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    if product_id not in database:
        return {"error":"product not found"}
    del database[product_id]
    return {"Message":"Product deleted successfully"}