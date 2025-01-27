from sqlalchemy.orm import Session
from schema_data import ClientDataSearchQuery
from models import TransactionBuyerModel,TransactionSellerModel,BuyerPartyListModel,SellerPartyListModel
from sqlalchemy import func


async def search_query_invoice_func(post : ClientDataSearchQuery, db2 : Session):
    records_per_page = 20
    post = post.dict()
    sType = post['sType']
    searchWord  = post["searchWord"]
    pageNum   = int(post["pageNum"])

    try:
        if sType == "sale":
    
            baseQuery = db2.query(TransactionSellerModel).filter(TransactionSellerModel.invoice == searchWord)      
            baseQuery = baseQuery.join(SellerPartyListModel, TransactionSellerModel.sellerId == SellerPartyListModel.sellerId)
            baseQuery = baseQuery.with_entities(
            TransactionSellerModel.invoice.label("invoice"),
            TransactionSellerModel.amount.label("amount"),
            TransactionSellerModel.dateBill.label("billDate"),
            SellerPartyListModel.sellerName.label("sellerName")
            )
            records = baseQuery.limit(records_per_page).all()
            if not records:
                 status = 1
                 message = "successful search with 0 matching records"
            else:
                 status = 1
                 message = "successful search"
            return{"status": status,"message":message,"records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "seller_name": row[3]} for row in records],"page_num": -1,"total_pages": 1}
        
        elif sType == "purchase":
            print("1")
            baseQuery = db2.query(TransactionBuyerModel).filter(TransactionBuyerModel.invoice == searchWord)      
            baseQuery = baseQuery.join(BuyerPartyListModel, TransactionBuyerModel.buyerId == BuyerPartyListModel.buyerId)
            baseQuery = baseQuery.with_entities(
            TransactionBuyerModel.invoice.label("invoice"),
            TransactionBuyerModel.amount.label("amount"),
            TransactionBuyerModel.dateBill.label("billDate"),
            BuyerPartyListModel.buyerName.label("buyerName")
            )
            records = baseQuery.limit(records_per_page).all()
            if not records:
                 status = 1
                 message = "successful search with 0 matching records"
            else:
                 status = 1
                 message = "successful search"
            return{"status": status,"message": message,"records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "buyer_name": row[3]} for row in records],"page_num": -1,"total_pages": 1}   
    except Exception as e:
            return({"status": 0,"message":f"Error: {e}","status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""}) 
async def search_query_party_func(post : ClientDataSearchQuery, db2 : Session):
    post = post.dict()
    sType = post['sType']
    searchWord  = post["searchWord"]
    startDate = post['startDate']
    endDate = post['endDate']
    pageNum   = int(post["pageNum"])
    totalPages = int(post['totalPages'])
    records_per_page = 10

    try:

        if sType == "sale":
    
            seller_id = (db2.query(SellerPartyListModel.sellerId)
            .filter( SellerPartyListModel.sellerName==searchWord)).scalar()
            baseQuery = (db2.query(
                TransactionSellerModel.invoice.label("invoice"),
                TransactionSellerModel.amount.label("amount"),
                TransactionSellerModel.dateBill.label("billDate"),
                SellerPartyListModel.sellerName.label("buyerName"))
                .join(SellerPartyListModel, TransactionSellerModel.sellerId == SellerPartyListModel.sellerId)
                .filter(TransactionSellerModel.sellerId == seller_id))
        
            
            if pageNum == -1:
                    total_records = baseQuery.count()
                    records = baseQuery.limit(records_per_page).all()
                    total_pages = (total_records + records_per_page - 1) // records_per_page
                    if not(records):
                        total_pages = -1
                        page_num = -1
                        message = "successful search with 0 matching records"
                    else:
                        page_num = 1 
                        message = "successful search"
                    
                    return{"status": 1,"message":message,"records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "seller_name": row[3]} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    return{"status": 1,"message":"successful search","records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "seller_name": row[3]} for row in records],"page_num": page_num,"total_pages": totalPages}

        elif sType == "purchase":

            buyer_id = (db2.query(BuyerPartyListModel.buyerId)
            .filter( BuyerPartyListModel.buyerName==searchWord).scalar())  
            baseQuery = (db2.query(
                TransactionBuyerModel.invoice.label("invoice"),
                TransactionBuyerModel.amount.label("amount"),
                TransactionBuyerModel.dateBill.label("billDate"),
                BuyerPartyListModel.buyerName.label("buyerName"))
                .join(BuyerPartyListModel, TransactionBuyerModel.buyerId == BuyerPartyListModel.buyerId)
                .filter(TransactionBuyerModel.buyerId == buyer_id))
            
            if pageNum == -1:
                    total_records = baseQuery.count()
                    records = baseQuery.limit(records_per_page).all()
                    total_pages = (total_records + records_per_page - 1) // records_per_page
                    if not(records):
                        total_pages = -1
                        page_num = -1
                        message = "successful search with 0 matching records"
                    else:
                        page_num = 1 
                        message = "successful search"
                    return{"status": 1,"message":message,"records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "buyer_name": row[3]} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    return{"status": 1,"message":"successful search","records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "seller_name": row[3]} for row in records],"page_num": page_num,"total_pages": totalPages}
            
    except Exception as e:
            return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""}) 
async def search_query_date_func(post : ClientDataSearchQuery, db2 : Session):
    post = post.dict()
    sType = post['sType']
    startDate = post['startDate']
    endDate = post['endDate']
    pageNum   = int(post["pageNum"])
    totalPages = int(post['totalPages'])
    records_per_page = 2

    try: 
          
        if sType == "sale":
    
            baseQuery = db2.query(TransactionSellerModel).filter( TransactionSellerModel.dateBill >= startDate,
            TransactionSellerModel.dateBill <= endDate)     
            baseQuery = baseQuery.join(SellerPartyListModel, TransactionSellerModel.sellerId == SellerPartyListModel.sellerId)
            baseQuery = baseQuery.with_entities(
            TransactionSellerModel.invoice.label("invoice"),
            TransactionSellerModel.amount.label("amount"),
            TransactionSellerModel.dateBill.label("billDate"),
            SellerPartyListModel.sellerName.label("sellerName"))
            if pageNum == -1:
                    total_records = baseQuery.count()
                    records = baseQuery.limit(records_per_page).all()
                    total_pages = (total_records + records_per_page - 1) // records_per_page
                    if not(records):
                        total_pages = -1
                        page_num = -1
                        message = "successful search with 0 matching records"
                    else:
                        page_num = 1 
                        message = "successful search"
                    return{"status": 1,"message":"successful search","records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "seller_name": row[3]} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    return{"status": 1,"message":"Successful","records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "seller_name": row[3]} for row in records],"page_num": page_num,"total_pages": totalPages}

        elif sType == "purchase":
            baseQuery = db2.query(TransactionBuyerModel).filter(TransactionBuyerModel.dateBill >= startDate,
            TransactionBuyerModel.dateBill <= endDate)      
            baseQuery = baseQuery.join(BuyerPartyListModel, TransactionBuyerModel.buyerId == BuyerPartyListModel.buyerId)
            baseQuery = baseQuery.with_entities(
            TransactionBuyerModel.invoice.label("invoice"),
            TransactionBuyerModel.amount.label("amount"),
            TransactionBuyerModel.dateBill.label("billDate"),
            BuyerPartyListModel.buyerName.label("buyerName")
            )
            if pageNum == -1:
                    total_records = baseQuery.count()
                    records = baseQuery.limit(records_per_page).all()
                    total_pages = (total_records + records_per_page - 1) // records_per_page
                    if not(records):
                        total_pages = -1
                        page_num = -1
                        message = "successful search with 0 matching records"
                    else:
                        page_num = 1
                        message = "successful search"
                    return{"status": 1,"message": message,"records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "buyer_name": row[3]} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    return{"status": 1,"message":"successful search","records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "buyer_name": row[3]} for row in records],"page_num": page_num,"total_pages":totalPages}

    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""})

async def party_list_search_query(post : ClientDataSearchQuery, db2 : Session):
    print("party1")
    post = post.dict()
    sType = post['sType']
    searchWord = post['searchWord']
    pageNum   = int(post["pageNum"])
    totalPages = int(post['totalPages'])
    records_per_page = 2

    try:
        if sType == "sale":
            baseQuery = db2.query(SellerPartyListModel.sellerName.label("sellerName")).filter(SellerPartyListModel.sellerName.contains(searchWord))      
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
                    return{"status": 1,"message": message,"records":[{"sellerName":row.sellerName} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
            
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    return{"status": 1,"message":"successful search","records":[{"sellerName":row.sellerName} for row in records],"page_num": page_num,"total_pages": totalPages}
        elif sType == "purchase":
                baseQuery = db2.query(BuyerPartyListModel.buyerName.label("buyerName")).filter(BuyerPartyListModel.buyerName.contains(searchWord))      
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
                            message= "successful search"
                        return{"status": 1,"message":message,"records":[{"buyerName":row.buyerName} for row in records],"page_num": page_num,"total_pages": total_pages}
                
                else:
                        page_num = pageNum
                        offset = (pageNum - 1) * records_per_page
                        records = baseQuery.offset(offset).limit(records_per_page).all()
                        return{"status": 1,"message":"successful search","records":[{"buyerName":row.buyerName} for row in records],"page_num": page_num,"total_pages": totalPages}
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""})

