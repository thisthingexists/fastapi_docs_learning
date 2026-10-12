from fastapi import FastAPI
from enum import Enum
import asyncio
app = FastAPI()

class ModelName(str,Enum): # we use enum to predefine options a user can enter in url bar or any input field
    # otherwise it would return error
    alexnet = "alexnet"
    lenet = "lenet"
    resnet = "resnet"

@app.get("/")
async def root():
    return {"Message":"Hello bhosdiwalon"}

@app.get("/item/{item_id}")
async def get_item(item_id: int):
    return {"item":item_id}

@app.get("/model/{model_name}")
async def get_model(model_name : ModelName):
    if model_name.value == ModelName.alexnet:
        return {"Model name is":ModelName.alexnet}
    if model_name is ModelName.resnet:
        return f"Model name is {ModelName.resnet}"
    if model_name is ModelName.lenet:
        return {"Model Name":model_name.value,"NEWS":"Modi MAdarXhod hai"}


@app.get("/file/{file_path:path}") #here path is used to make a url which includes slashes ////
async def get_file(file_path:str):
    return {"The path is":file_path}


