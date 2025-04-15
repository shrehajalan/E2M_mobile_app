from sqlalchemy.orm import Session
from schema_data import ClientDataSearchQuery
from models import TransactionBuyerModel,TransactionSellerModel,BuyerPartyListModel,SellerPartyListModel,HistoryHandBillModel,HistorySellCashCustomerModel,HistoryPurchaseModel,HistorySellModel
from models import ProductListModel
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
            return{"status": status,"message":message,"records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "seller_name": row[3]} for row in records],"page_num": 1,"total_pages": 1}
        
        elif sType == "purchase":
            
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
            return{"status": status,"message": message,"records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "buyer_name": row[3]} for row in records],"page_num": 1,"total_pages": 1}   
    except Exception as e:
            return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""}) 
async def search_query_party_func(post : ClientDataSearchQuery, db2 : Session):
    post = post.dict()
    sType = post['sType']
    searchWord  = post["searchWord"]
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
                SellerPartyListModel.sellerName.label("sellerName"))
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
                    return{"status": 1,"message":message,"records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "seller_name": row[3]} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    return{"status": 1,"message":"successful search","records":[{"invoice_no": row[0], "amount": row[1], "date_bill": row[2], "seller_name": row[3]} for row in records],"page_num": page_num,"total_pages": totalPages}

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
async def search_query_brand_func(post : ClientDataSearchQuery, db2 : Session):
    post = post.dict()
    sType = post['sType']
    searchWord = post['searchWord']
    try:
         
        if sType == 'sale':

            baseQuery = (db2.query(
                HistorySellModel.prodNum.label('prodNum'),
                func.sum(HistorySellModel.totalPrice).label('totalPrice'),
                func.sum(HistorySellModel.gst).label('gst'))
            .group_by(HistorySellModel.prodNum)
            .subquery())# Turn this into a subquery
            
            final_baseQuery = (db2.query(
                ProductListModel.brand.label('brand'),
                func.sum(baseQuery.c.totalPrice.label('totalPrice')),
                func.sum(baseQuery.c.gst.label('totalGst')))
            .join(ProductListModel, baseQuery.c.prodNum == ProductListModel.prodNum)
            .filter(ProductListModel.brand == searchWord))
            record1_1 = final_baseQuery.all()

            baseQuery = (db2.query(
                HistoryHandBillModel.prodNum.label('prodNum'),
                func.sum(HistoryHandBillModel.totalPrice).label('totalPrice'),
                func.sum(HistoryHandBillModel.gst).label('gst'))
            .group_by(HistoryHandBillModel.prodNum)
            .subquery())# Turn this into a subquery
            
            final_baseQuery = (db2.query(
                ProductListModel.brand.label('brand'),
                func.sum(baseQuery.c.totalPrice.label('totalPrice')),
                func.sum(baseQuery.c.gst.label('totalGst')))
            .join(ProductListModel, baseQuery.c.prodNum == ProductListModel.prodNum)
            .filter(ProductListModel.brand == searchWord))
            record1_2 = final_baseQuery.all()

                    
            baseQuery = (db2.query(
                HistorySellCashCustomerModel.prodNum.label('prodNum'),
                func.sum(HistorySellCashCustomerModel.totalPrice).label('totalPrice'))
            .group_by(HistorySellCashCustomerModel.prodNum)
            .subquery())# Turn this into a subquery
            
            final_baseQuery = (db2.query(
                ProductListModel.brand.label('brand'),
                func.sum(baseQuery.c.totalPrice.label('totalPrice')))
            .join(ProductListModel, baseQuery.c.prodNum == ProductListModel.prodNum)
            .filter(ProductListModel.brand == searchWord))
            
            record2 = final_baseQuery.all()

            total_purchase_amount_on_credit = 0
            total_purchase_amount_on_cash = 0
            if not record1_1[0][0] and not record1_2[0][0] and not record2[0][0]:
                    status = 1
                    message = "successful search with 0 matching records"
            else:
                    status = 1
                    message = "successful search"
                    if record1_1[0][0]:
                            total_purchase_amount_on_credit = int(record1_1[0][1]+record1_1[0][2])
                            if record1_2[0][0]:
                                total_purchase_amount_on_credit = total_purchase_amount_on_credit + int(record1_2[0][1]+record1_2[0][2])
                    if record2[0][0]:
                        for rec in record2:
                            total_purchase_amount_on_cash = int(rec[1])

            return{"status": status,"message": message,"tool-brand":searchWord,"total_sale_amount_on_credit":total_purchase_amount_on_credit,"total_sale_amount_on_cash":total_purchase_amount_on_cash}


        elif sType == 'purchase':
            
            baseQuery = (db2.query(
                    HistoryPurchaseModel.prodNum.label('prodNum'),
                    func.sum(HistoryPurchaseModel.totalPrice).label('totalPrice'),
                    func.sum(HistoryPurchaseModel.gst).label('gst'))
                .group_by(HistoryPurchaseModel.prodNum)
                .subquery())# Turn this into a subquery
                
            final_baseQuery = (db2.query(
                    ProductListModel.brand.label('brand'),
                    func.sum(baseQuery.c.totalPrice.label('totalPrice')),
                    func.sum(baseQuery.c.gst.label('totalGst')))
                .join(ProductListModel, baseQuery.c.prodNum == ProductListModel.prodNum)
                .filter(ProductListModel.brand == searchWord))
            record = final_baseQuery.all()
                
            total_purchase_amount_on_credit = 0
            if not record[0][0]:
                        status = 1
                        message = "successful search with 0 matching records"
            else:
                        status = 1
                        message = "successful search"
                        total_purchase_amount_on_credit = int(record[0][1]+record[0][2])
                
            return{"status": status,"message": message,"tool-brand":searchWord,"total_purchase_amount_on_credit":total_purchase_amount_on_credit,"total_purchase_amount_on_cash":"no cash transaction"}
    
    except Exception as e:
            return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""}) 
    
async def party_list_search_query(post : ClientDataSearchQuery, db2 : Session):
    
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
                    if not(records):#records : [] : signifies false
                        total_pages = -1
                        page_num = -1
                        message = "successful search with 0 matching party"
                    else:
                        page_num = 1 
                        message = "successful search"
                    #if records var is empty ([])..in python It asks: "Is there anything in the list?"...IF NO....the loop body ({"sellerName":row.sellerName}) never runs, so row is never even created or used
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
async def tool_brand_list_search_query(post : ClientDataSearchQuery, db2 : Session):
    print("brand")
    post = post.dict()
    sType = post['sType']
    searchWord = post['searchWord']
    pageNum   = int(post["pageNum"])
    totalPages = int(post['totalPages'])
    records_per_page = 2

    try:
            baseQuery = db2.query(ProductListModel.brand.label("toolBrand")).filter(ProductListModel.brand.contains(searchWord)).group_by(ProductListModel.brand)    
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
                    return{"status": 1,"message": message,"records":[{"tool-brand":row.toolBrand} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    return{"status": 1,"message": message,"records":[{"tool-brand":row.toolBrand} for row in records],"page_num": page_num,"total_pages": total_pages}
            
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""})