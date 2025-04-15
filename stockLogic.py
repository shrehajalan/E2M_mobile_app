from sqlalchemy.orm import Session
from schema_data import ClientDataStockDetail
from models import ProductListModel
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce

async def total_stock_query(post : ClientDataStockDetail, db2 : Session):
    type = post['type']
    value = post['value']
    try:
         
        if type == 'itemName':
            record = db2.query(ProductListModel.stock,(ProductListModel.stock * ProductListModel.mrp).label("total_item_value")).filter(ProductListModel.productDescription == value).first()
            if not record:
                return({"status":0, "message":"no matching records", "values":{'type': type, 'value': value, "stock_in_numbers" : "", "total_stock_value" : ""}})
            return({"status":1, "message":"successful match", "values":{'type': type, 'value': value, "stock_in_numbers": int(record[0]), "total_stock_value":int(record[1])}})

        if type == "brand":
            stock_value = db2.query(coalesce(func.sum(ProductListModel.stock), -1).label("total_stock")).filter(ProductListModel.brand == value).scalar()
            if stock_value == -1:
                return({"status":0, "message":"no matching records", "values":{'type': type, 'value': value, "stock_in_numbers" : "", "total_stock_value" : ""}})
            return({"status":1, "message":"successful match","values": {'type': type, 'value':value, "stock_in_numbers":"", "total_stock_value":int(stock_value)}})
   
    except Exception as e:
        return({"status" : 0,"message" : f"Error: {e}","values": None})   
async def item_list_stock_query(post : ClientDataStockDetail, db2 : Session):

    searchWord = post['value']
    pageNum   = int(post["pageNum"])
    totalPages = int(post['totalPages'])
    records_per_page = 2
    try:
            baseQuery = db2.query(ProductListModel.productDescription.label("itemName")).filter(ProductListModel.productDescription.contains(searchWord)).group_by(ProductListModel.productDescription)    
            if pageNum == -1:  
                    total_records = baseQuery.count()
                    records = baseQuery.limit(records_per_page).all()
                    total_pages = (total_records + records_per_page - 1) // records_per_page
                    if not(records):
                        total_pages = -1
                        page_num = -1
                        message = "successful search with 0 matching party"
                    else:
                        page_num = 1 
                        message = "successful search"
                    return{"status": 1,"message": message,"records":[{"item_name":row.itemName} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    message = "successful search"
                    return{"status": 1,"message": message,"records":[{"item_name":row.itemName} for row in records],"page_num": page_num,"total_pages": totalPages}
            
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""})
async def brand_list_stock_query(post : ClientDataStockDetail, db2 : Session):
    searchWord = post['value']
    pageNum   = int(post["pageNum"])
    totalPages = int(post['totalPages'])
    records_per_page = 2
    try:
            baseQuery = db2.query(ProductListModel.brand.label("brand")).filter(ProductListModel.brand.contains(searchWord)).group_by(ProductListModel.brand)    
            if pageNum == -1:  
                    total_records = baseQuery.count()
                    records = baseQuery.limit(records_per_page).all()
                    total_pages = (total_records + records_per_page - 1) // records_per_page
                    if not(records):
                        total_pages = -1
                        page_num = -1
                        message = "successful search with 0 matching party"
                    else:
                        page_num = 1 
                        message = "successful search"
                    return{"status": 1,"message": message,"records":[{"brand":row.brand} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    message = "successful search"
                    return{"status": 1,"message": message,"records":[{"brand":row.brand} for row in records],"page_num": page_num,"total_pages": totalPages}
            
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""})        