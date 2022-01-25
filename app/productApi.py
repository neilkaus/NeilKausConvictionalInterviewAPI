# productApi.py
# contains the class that manages the APIs to pull products from and encapsulates the proccess of getting their data

import requests

class productApi:    
    """maintains a list of info about the APIs to pull products from and encapsulates getting data from the product apis"""

    # list of api info to correctly map the attributes of source API data to this APIs standard stored as (newKey,oldKey)
    # list used to allow for easy addition of new product APIs
    productApiInfo = [ 
        {   
            "url" : "https://my-json-server.typicode.com/convictional/engineering-interview-api/products",
            "productKeyChanges" : { 'code' : 'id', 'title' : 'title', 'vendor' : 'vendor',  'bodyHtml' : 'body_html' , 'variants' : 'variants'},
            "variantKeyChanges" : {'id' : 'id' , 'title' : 'title' , 'sku' : 'sku', 'weight': 'weight', 'images' : 'images'},
            "weightKeyChanges" : {'value' : 'weight' , 'unit' : 'weight_unit'},
            "imageKeyChanges" : {'source' : 'src'}
        }
    ]

    @staticmethod
    def getData():
        """"gets data from all stored product APIs and returns it in the correct format"""
        processedProductData = []
        
        for apiInfo in productApi.productApiInfo:
            productData = requests.get(apiInfo["url"]).json()
            
            for singleProduct in productData:
                #take only the necessary attributes with the correct names from the product API
                productDict = dict((newKey, singleProduct[oldKey]) for (newKey, oldKey) in apiInfo["productKeyChanges"].items())
                
                #change variants into correct form
                variantsList = []
                imagesList = []
                for singleVariant in productDict["variants"]:
                    variantDict = {}
                    for (newKey, oldKey) in apiInfo["variantKeyChanges"].items():
                        # correctly add weight
                        if newKey == 'weight':
                            variantDict.update({'weight' :  {
                                                    'value' : singleVariant[apiInfo["weightKeyChanges"]['value']],
                                                    'unit' : singleVariant[apiInfo["weightKeyChanges"]['unit']]
                                                    }})
                        #collect images to be added to product 
                        elif newKey == 'images':
                            for image in singleVariant[apiInfo["variantKeyChanges"]['images']]:
                                if image != None:
                                    imagesList.append(
                                        {
                                            'source' : image[apiInfo["imageKeyChanges"]['source']],
                                            'variantId' : singleVariant[apiInfo["variantKeyChanges"]['id']]
                                        }
                                    )
                        #change to correct key
                        else:
                            variantDict.update({newKey : singleVariant[oldKey]})
                    
                    variantsList.append(variantDict)        
                productDict["variants"] = variantsList
                productDict["images"] = imagesList

                #update inventory_quantity and whether it is available 
                for singleVariant in productDict["variants"]:
                    if singleVariant != None:
                        if "inventory_quantity" in singleVariant:
                            if singleVariant["inventory_quantity"] > 0:
                                singleVariant["available"] = True
                        else:
                            singleVariant["inventory_quantity"] = 0
                            singleVariant["available"] = False
                
                processedProductData.append(productDict)
            
        return processedProductData
