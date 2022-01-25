# main.py
# main file containing app definition and definition of get functions

from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.schemas import inventory, product, error
from app.productApi import productApi

app = FastAPI(
    title="Convictional Interview API",
    openapi_tags= [
        {
            "name" : "product",
            "description" : "Representation of a seller's products"
        },
        {
            "name" : "store",
            "description" : "Representation of a seller's storefront"
        }
    ]
)

@app.get("/products", 
    summary="Get all products",
    description="Returns a list of all products",
    tags=["product"],
    response_model=List[product],
    responses={404 : {"model" : error}})
async def getAllProducts():
    allProducts = productApi.getData()
    
    # if there are no products throw an error
    if allProducts == []:
        return JSONResponse(status_code=404, content={"message" : "Products not found"})
    else:
        return allProducts

@app.get("/products/{productId}", 
    summary="Get product by ID",
    description="Returns a single product",
    tags=["product"],
    response_model=product,
    responses={404 : {"model" : error}, 400 : {"model" : error}})
async def getProductById(productId):
    #check for correct productId form
    try:
        int(productId)
    except:
        return JSONResponse(status_code=400, content={"message" : "Invalid ID supplied"})

    allProducts = productApi.getData()

    # if there are no products throw an error
    if allProducts == []:
        return JSONResponse(status_code=404, content={"message" : "Product not found"})

    #find the right product
    for singleProduct in allProducts:
        if str(singleProduct['code']) == str(productId):
            return singleProduct

    return JSONResponse(status_code=404, content={"message" : "Product not found"})


@app.get("/store/inventory", 
    summary="Returns product inventories",
    description="Returns an array of inventory objects for each variant",
    tags=["store"],
    response_model=List[inventory],
    responses={404 : {"model" : error}})
async def getInventory():
    allProducts = productApi.getData()

    #if there are no products throw an error
    if allProducts == []:
        return JSONResponse(status_code=404, content={"message" : "Products not found"})

    # create list of inventory formatted dicts for all variants
    inventoryList = []
    for singleProduct in allProducts:
        for singleVariant in singleProduct['variants']:
            inventoryList.append({
                'productId' : singleProduct['code'],
                'variantId' : singleVariant['id'],
                'stock' : singleVariant['inventory_quantity']
            })
    
    return inventoryList

