from sqlalchemy.orm import Session
from schema_data import ClientDataSearchQueryOnItem
from models import BuyerPartyListModel,SellerPartyListModel,HistoryHandBillModel,HistorySellCashCustomerModel,HistoryPurchaseModel,HistorySellModel
from models import ProductListModel
from sqlalchemy import desc

async def item_search_query_item_func(post : ClientDataSearchQueryOnItem, db2 : Session):
    records_per_page = 20
    post = post.dict()
    searchWord  = post["searchWord"]
    pageNum   = int(post["pageNum"])
    records_per_page = 2
    curBuyPageNum = int(post['curBuyPageNum'])
    curSellPageNum = int(post['curSellPageNum'])
    totalBuyPages = int(post["totalBuyPages"])
    totalCashSellPages = int(post["totalCashSellPages"])
    totalAutoSellPages = int(post["totalAutoSellPages"])
    totalHandSellPages  = int(post["totalHandSellPages"])

    try:
        prodId = db2.query(ProductListModel.prodNum).filter(ProductListModel.productDescription == searchWord).scalar()
        baseQuery = (db2.query(
                              HistoryPurchaseModel.invoiceNo,
                              HistoryPurchaseModel.dateBill,
                              BuyerPartyListModel.buyerName,
                              HistoryPurchaseModel.qty,
                              HistoryPurchaseModel.gst,
                              HistoryPurchaseModel.totalPrice)
                              .join(BuyerPartyListModel,BuyerPartyListModel.buyerId == HistoryPurchaseModel.buyerId)
                              .filter(HistoryPurchaseModel.prodNum == prodId))      
        baseQuery1 = (db2.query(
                              HistorySellModel.invoiceNo,
                              HistorySellModel.dateBill,
                              SellerPartyListModel.sellerName,
                              HistorySellModel.qty,
                              HistorySellModel.gst,
                              HistorySellModel.totalPrice)
                              .join(SellerPartyListModel,SellerPartyListModel.sellerId == HistorySellModel.sellerId)
                              .filter(HistorySellModel.prodNum == prodId))
        baseQuery2 = (db2.query(
                              HistoryHandBillModel.invoiceNo,
                              HistoryHandBillModel.dateBill,
                              SellerPartyListModel.sellerName,
                              HistoryHandBillModel.qty,
                              HistoryHandBillModel.gst,
                              HistoryHandBillModel.totalPrice)
                              .join(BuyerPartyListModel,BuyerPartyListModel.buyerId == HistoryHandBillModel.sellerId)
                              .filter(HistoryHandBillModel.prodNum == prodId))
        baseQuery3 = (db2.query(
                              HistorySellCashCustomerModel.chalanNo,
                              HistorySellCashCustomerModel.dateSell,
                              HistorySellCashCustomerModel.qty,
                              HistorySellCashCustomerModel.totalPrice)
                              .filter(HistorySellCashCustomerModel.prodNum == prodId))
        
        if curBuyPageNum == -1 and curSellPageNum == -1:
                    total_records = baseQuery.count()
                    total_records1 = baseQuery1.count()
                    total_records2 = baseQuery2.count()
                    total_records3 = baseQuery3.count()

                    records = baseQuery.limit(records_per_page).all()
                    total_buy_pages = (total_records + records_per_page - 1) // records_per_page

                    records1 = baseQuery1.limit(records_per_page).all()
                    total_autosell_pages = (total_records1 + records_per_page - 1) // records_per_page

                    records2 = baseQuery2.limit(records_per_page).all()
                    total_handsell_pages = (total_records2 + records_per_page - 1) // records_per_page

                    records3 = baseQuery3.limit(records_per_page).all()
                    total_cashsell_pages = (total_records3 + records_per_page - 1) // records_per_page

                    if not(records):
                        totalBuyPages = -1
                        curBuyPageNum = -2
                        records_dic_buy = []
                    else:
                        totalBuyPages = total_buy_pages
                        curBuyPageNum = 1
                        records_dic_buy = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records]
                   
                    if not(records1):
                        curSellPageNum1 = -1
                        records_dic_sell1 = []
                    else:
                        totalAutoSellPages = total_autosell_pages
                        curSellPageNum1 = 1
                        records_dic_sell1 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records1]

                    if not(records2):
                        curSellPageNum2 = -1
                        records_dic_sell2 = []
                    else:
                        totalHandSellPages = total_handsell_pages
                        curSellPageNum2 = 1
                        records_dic_sell2 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records2]

                    if not(records3):
                        curSellPageNum3 = -1
                        records_dic_sell3 = []
                    else:
                        totalCashSellPages = total_cashsell_pages
                        curSellPageNum3 = 1
                        records_dic_sell3 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records3]
                    
                    if curSellPageNum1 == -1 and curSellPageNum2 == -1 and curSellPageNum3 == -1:
                            curSellPageNum = -2
                    else:
                            curSellPageNum = 1
        else:
             if curBuyPageNum != -1 and curBuyPageNum !=-2:
                  if curBuyPageNum <= totalBuyPages:
                       offset = (curBuyPageNum - 1) * records_per_page
                       records = baseQuery.offset(offset).limit(records_per_page).all()
                       records_dic_buy = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records]
                  else:
                       curBuyPageNum = -2
                       records_dic_buy = []
             if curSellPageNum != -1 and curSellPageNum !=-2:
                  if curSellPageNum <= totalAutoSellPages:
                        offset = (curSellPageNum - 1) * records_per_page
                        records1 = baseQuery1.offset(offset).limit(records_per_page).all()
                        records_dic_sell1 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records1]
                        curSellPageNum1 = curSellPageNum                 
                  else:
                       curSellPageNum1 = -1
                       records_dic_sell1 = []

                  if curSellPageNum <= totalHandSellPages:
                        offset = (curSellPageNum - 1) * records_per_page
                        records2 = baseQuery2.offset(offset).limit(records_per_page).all()
                        records_dic_sell2 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records2]
                        curSellPageNum2 = curSellPageNum
                  else:
                       curSellPageNum2 = -1
                       records_dic_sell2 = []

                  if curSellPageNum  <= totalCashSellPages:
                        curSellPageNum3 = curSellPageNum 
                        offset = (curSellPageNum - 1) * records_per_page
                        records3 = baseQuery3.offset(offset).limit(records_per_page).all()
                        records_dic_sell3 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records3]
                        curSellPageNum3 = curSellPageNum
                  else:
                       curSellPageNum3 = -1
                       records_dic_sell3 = []
        if curSellPageNum != -2:
            if curSellPageNum1 == -1 and curSellPageNum2 == -1 and curSellPageNum3 == -1:
                curSellPageNum = -2
    
        if curBuyPageNum == -2:
             records_dic_buy = []

        if curSellPageNum == -2:
            f_records_dic_sell = []
        else:
             f_records_dic_sell = records_dic_sell1 + records_dic_sell2 + records_dic_sell3

        if curSellPageNum == -2 and curBuyPageNum == -2:
            message = "search successful with 0 buy records and with 0 sell records"
        elif curSellPageNum == -2:
            message = "search successful with 0 sell records and non zero buy records"
        elif curBuyPageNum == -2:
            message = "search successful with 0 buy records and with non zero sell records"
        else:
            message = "search successful"         
                
        return {"status": 1,"message": message,"buy_records": records_dic_buy,"sell_records" : f_records_dic_sell,"page_num": pageNum, "curSellPageNum":curSellPageNum,"curBuyPageNum":curBuyPageNum,"totalBuyPages" : totalBuyPages,
                                "totalCashSellPages" :totalCashSellPages,"totalAutoSellPages":totalAutoSellPages,"totalHandSellPages":totalHandSellPages}

    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","buy_records":[],"sell_records":[],"page_num":"","total_pages":"","curSellPageNum":"","curBuyPageNum":"","totalBuyPages" : "",
                    "totalCashSellPages" :"","totalAutoSellPages":"","totalHandSellPages":""})    
async def item_search_query_date_func(post :  ClientDataSearchQueryOnItem, db2 : Session):
    records_per_page = 20
    post = post.dict()
    pageNum   = int(post["pageNum"])
    startDate = post['startDate']
    endDate = post['endDate']
    records_per_page = 2
    curBuyPageNum = int(post['curBuyPageNum'])
    curSellPageNum = int(post['curSellPageNum'])
    totalBuyPages = int(post["totalBuyPages"])
    totalCashSellPages = int(post["totalCashSellPages"])
    totalAutoSellPages = int(post["totalAutoSellPages"])
    totalHandSellPages  = int(post["totalHandSellPages"])

    try:
        baseQuery = (db2.query(
                              HistoryPurchaseModel.invoiceNo,
                              HistoryPurchaseModel.dateBill,
                              BuyerPartyListModel.buyerName,
                              HistoryPurchaseModel.qty,
                              HistoryPurchaseModel.gst,
                              HistoryPurchaseModel.totalPrice)
                              .join(BuyerPartyListModel,BuyerPartyListModel.buyerId == HistoryPurchaseModel.buyerId)
                              .filter(HistoryPurchaseModel.dateBill >= startDate,
            HistoryPurchaseModel.dateBill <= endDate))    

        baseQuery1 = (db2.query(
                              HistorySellModel.invoiceNo,
                              HistorySellModel.dateBill,
                              SellerPartyListModel.sellerName,
                              HistorySellModel.qty,
                              HistorySellModel.gst,
                              HistorySellModel.totalPrice)
                              .join(SellerPartyListModel,SellerPartyListModel.sellerId == HistorySellModel.sellerId)
                              .filter(HistorySellModel.dateBill >= startDate,
            HistorySellModel.dateBill <= endDate))

        baseQuery2 = (db2.query(
                              HistoryHandBillModel.invoiceNo,
                              HistoryHandBillModel.dateBill,
                              SellerPartyListModel.sellerName,
                              HistoryHandBillModel.qty,
                              HistoryHandBillModel.gst,
                              HistoryHandBillModel.totalPrice)
                              .join(BuyerPartyListModel,BuyerPartyListModel.buyerId == HistoryHandBillModel.sellerId)
                              .filter(HistoryHandBillModel.dateBill >= startDate,
            HistoryHandBillModel.dateBill <= endDate))

        baseQuery3 = (db2.query(
                              HistorySellCashCustomerModel.chalanNo,
                              HistorySellCashCustomerModel.dateSell,
                              HistorySellCashCustomerModel.qty,
                              HistorySellCashCustomerModel.totalPrice)
                              .filter(HistorySellCashCustomerModel.dateSell >= startDate,
            HistorySellCashCustomerModel.dateSell <= endDate))
        if curBuyPageNum == -1 and curSellPageNum == -1:
                    total_records = baseQuery.count()
                    total_records1 = baseQuery1.count()
                    total_records2 = baseQuery2.count()
                    total_records3 = baseQuery3.count()

                    records = baseQuery.limit(records_per_page).all()
                    total_buy_pages = (total_records + records_per_page - 1) // records_per_page

                    records1 = baseQuery1.limit(records_per_page).all()
                    total_autosell_pages = (total_records1 + records_per_page - 1) // records_per_page

                    records2 = baseQuery2.limit(records_per_page).all()
                    total_handsell_pages = (total_records2 + records_per_page - 1) // records_per_page

                    records3 = baseQuery3.limit(records_per_page).all()
                    total_cashsell_pages = (total_records3 + records_per_page - 1) // records_per_page
           
                    if not(records):
                        totalBuyPages = -1
                        curBuyPageNum = -2
                        records_dic_buy = []
                    else:
             
                        totalBuyPages = total_buy_pages
                        curBuyPageNum = 1
                        records_dic_buy = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records]
                   
                    if not(records1):
                        curSellPageNum1 = -1
                        records_dic_sell1 = []
                
                    else:
                        totalAutoSellPages = total_autosell_pages
                        curSellPageNum1 = 1
                        records_dic_sell1 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records1]

                    if not(records2):
                        curSellPageNum2 = -1
                        records_dic_sell2 = []
                     
                    else:
                        totalHandSellPages = total_handsell_pages
                        curSellPageNum2 = 1
                        records_dic_sell2 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records2]
                  
                    if not(records3):
                        curSellPageNum3 = -1
                        records_dic_sell3 = []
                   
                    else:
                        totalCashSellPages = total_cashsell_pages
                        curSellPageNum3 = 1
                        records_dic_sell3 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records3]
                      
                    if curSellPageNum1 == -1 and curSellPageNum2 == -1 and curSellPageNum3 == -1:
                            curSellPageNum = -2
                    else:
                            curSellPageNum = 1
       
        else:
             if curBuyPageNum != -1 and curBuyPageNum != -2:
                  if  curBuyPageNum <= totalBuyPages:
                       offset = ( curBuyPageNum - 1) * records_per_page
                       records = baseQuery.offset(offset).limit(records_per_page).all()
                       records_dic_buy = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records]
                  else:
                       curBuyPageNum = -2
                       records_dic_buy = []

             if curSellPageNum != -1 and curSellPageNum != -2:
                  if  curSellPageNum  <= totalAutoSellPages:       
                        offset = (pageNum - 1) * records_per_page
                        records1 = baseQuery1.offset(offset).limit(records_per_page).all()
                        records_dic_sell1 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records1]
                  else:
                       curSellPageNum1 = -1
                       records_dic_sell1 = []

                  if curSellPageNum <= totalHandSellPages:
                        offset = (pageNum - 1) * records_per_page
                        records2 = baseQuery2.offset(offset).limit(records_per_page).all()
                        records_dic_sell2 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records2]
                  else:
                       curSellPageNum2 = -1
                       records_dic_sell2 = []

                  if curSellPageNum <= totalCashSellPages:
                        offset = (curSellPageNum - 1) * records_per_page
                        records3 = baseQuery3.offset(offset).limit(records_per_page).all()
                        records_dic_sell3 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records3]
                  else:
                       curSellPageNum3 = -1
                       records_dic_sell3 = []

        if curSellPageNum != -2:
            if curSellPageNum1 == -1 and curSellPageNum2 == -1 and curSellPageNum3 == -1:
                curSellPageNum = -2
    
        if curBuyPageNum == -2:
             records_dic_buy = []

        if curSellPageNum == -2:
            f_records_dic_sell = []
        else:
             f_records_dic_sell = records_dic_sell1 + records_dic_sell2 + records_dic_sell3

        if curSellPageNum == -2 and curBuyPageNum == -2:
            message = "search successful with 0 buy records and with 0 sell records"
        elif curSellPageNum == -2:
            message = "search successful with 0 sell records and non zero buy records"
        elif curBuyPageNum == -2:
            message = "search successful with 0 buy records and with non zero sell records"
        else:
            message = "search successful"        
                
        return {"status": 1,"message": message,"buy_records": records_dic_buy,"sell_records" : f_records_dic_sell,"page_num": pageNum, "curSellPageNum":curSellPageNum,"curBuyPageNum":curBuyPageNum,"totalBuyPages" : totalBuyPages,
                                "totalCashSellPages" :totalCashSellPages,"totalAutoSellPages":totalAutoSellPages,"totalHandSellPages":totalHandSellPages}

    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","buy_records":[],"sell_records":[],"page_num":"","total_pages":"","curSellPageNum":"","curBuyPageNum":"","totalBuyPages" : "",
                    "totalCashSellPages" :"","totalAutoSellPages":"","totalHandSellPages":""})
async def item_search_query_item_party_func(post : ClientDataSearchQueryOnItem, db2 : Session):
    records_per_page = 20
    post = post.dict()
    pageNum   = int(post["pageNum"])
    itemName = post["searchWord"]
    partyName  = post["searchWord2"]
    records_per_page = 2
    curBuyPageNum = int(post['curBuyPageNum'])
    curSellPageNum = int(post['curSellPageNum'])
    totalBuyPages = int(post["totalBuyPages"])
    totalCashSellPages = int(post["totalCashSellPages"])
    totalAutoSellPages = int(post["totalAutoSellPages"])
    totalHandSellPages  = int(post["totalHandSellPages"])

    try:
        prodId = db2.query(ProductListModel.prodNum).filter(ProductListModel.productDescription == itemName).scalar()
        baseQuery1 = (db2.query(
                              HistorySellModel.invoiceNo,
                              HistorySellModel.dateBill,
                              SellerPartyListModel.sellerName,
                              HistorySellModel.qty,
                              HistorySellModel.gst,
                              HistorySellModel.totalPrice)
                              .join(SellerPartyListModel,SellerPartyListModel.sellerId == HistorySellModel.sellerId)
                              .filter(HistorySellModel.prodNum == prodId)
                              .filter(SellerPartyListModel.sellerName == partyName)
                              .order_by(desc(HistorySellModel.dateBill)))  
        
        baseQuery2 = (db2.query(
                              HistoryHandBillModel.invoiceNo,
                              HistoryHandBillModel.dateBill,
                              SellerPartyListModel.sellerName,
                              HistoryHandBillModel.qty,
                              HistoryHandBillModel.gst,
                              HistoryHandBillModel.totalPrice)
                              .join(SellerPartyListModel,SellerPartyListModel.sellerId == HistoryHandBillModel.sellerId)
                              .filter(HistoryHandBillModel.prodNum == prodId)
                              .filter(BuyerPartyListModel.buyerName == partyName)
                              .order_by(desc(HistoryHandBillModel.dateBill)))  
 
        baseQuery3 = (db2.query(
                              HistorySellCashCustomerModel.chalanNo,
                              HistorySellCashCustomerModel.dateSell,
                              HistorySellCashCustomerModel.qty,
                              HistorySellCashCustomerModel.totalPrice)
                              .filter(HistoryPurchaseModel.prodNum == prodId)
                              .filter(SellerPartyListModel.sellerName == partyName)
                              .order_by(desc(HistorySellCashCustomerModel.dateSell)))
        if curSellPageNum == -1:
                    
                    total_records1 = baseQuery1.count()
                    total_records2 = baseQuery2.count()
                    total_records3 = baseQuery3.count()

                    records1 = baseQuery1.limit(records_per_page).all()
                    total_autosell_pages = (total_records1 + records_per_page - 1) // records_per_page

                    records2 = baseQuery2.limit(records_per_page).all()
                    total_handsell_pages = (total_records2 + records_per_page - 1) // records_per_page

                    records3 = baseQuery3.limit(records_per_page).all()
                    total_cashsell_pages = (total_records3 + records_per_page - 1) // records_per_page
                   
                    if not(records1):
                        curSellPageNum1 = -1
                        records_dic_sell1 = []
                    else:
                        totalAutoSellPages = total_autosell_pages
                        curSellPageNum1 = 1
                        records_dic_sell1 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records1]

                    if not(records2):
                        curSellPageNum2 = -1
                        records_dic_sell2 = []
                    else:
                        totalHandSellPages = total_handsell_pages
                        curSellPageNum2 = 1
                        records_dic_sell2 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records2]

                    if not(records3):
                        curSellPageNum3 = -1
                        records_dic_sell3 = []
                    else:
                        totalCashSellPages = total_cashsell_pages
                        curSellPageNum3 = 1
                        records_dic_sell3 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records3]

                    if curSellPageNum1 == -1 and curSellPageNum2 == -1 and curSellPageNum3 == -1:
                        curSellPageNum = -2
                    else: 
                         curSellPageNum = 1  
       
        else:
             if curSellPageNum != -1 and curSellPageNum != -2:
                  if curSellPageNum <= totalAutoSellPages:
                        curSellPageNum1 = curSellPageNum
                        offset = (curSellPageNum- 1) * records_per_page
                        records1 = baseQuery1.offset(offset).limit(records_per_page).all()
                        records_dic_sell1 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records1]
                  else:
                       curSellPageNum1 = -1
                       records_dic_sell1 = []

                  if curSellPageNum <= totalHandSellPages:
                        curSellPageNum2 = curSellPageNum
                        offset = (pageNum - 1) * records_per_page
                        records2 = baseQuery2.offset(offset).limit(records_per_page).all()
                        records_dic_sell2 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records2]
                  else:
                       curSellPageNum2 = -1
                       records_dic_sell2 = []

                  if curSellPageNum <= totalCashSellPages:
                        curSellPageNum3 = curSellPageNum
                        offset = (curSellPageNum - 1) * records_per_page
                        records3 = baseQuery3.offset(offset).limit(records_per_page).all()
                        records_dic_sell3 = [{"invoice_no":record[0],"bill_date":record[1],"buyer_name":record[2],"quantity":record[3],"total_price after_gst":record[4]+record[5]}for record in records3]
                  else:
                       curSellPageNum3 = -1
                       records_dic_sell3 = []

        if curSellPageNum == -2:
            f_records_dic_sell = []
        else:
            if curSellPageNum1 == -1 and curSellPageNum2 == -1 and curSellPageNum3 == -1:
                curSellPageNum = -2
                f_records_dic_sell = []
            else:
                f_records_dic_sell = records_dic_sell1 + records_dic_sell2 + records_dic_sell3

        if curSellPageNum == -2:
            message = "search successful with 0 sell records"
        else:
            message = "search successful"         
                
        return {"status": 1,"message": message,"buy_records": [],"sell_records" : f_records_dic_sell,"page_num": pageNum, "curSellPageNum":curSellPageNum,"curBuyPageNum":"","totalBuyPages" : "",
                                "totalCashSellPages" :totalCashSellPages,"totalAutoSellPages":totalAutoSellPages,"totalHandSellPages":totalHandSellPages}

    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","buy_records":[],"sell_records":[],"page_num":"","total_pages":"","curSellPageNum":"","curBuyPageNum":"","totalBuyPages" : "",
                    "totalCashSellPages" :"","totalAutoSellPages":"","totalHandSellPages":""})

async def itemName_list_search_query(post : ClientDataSearchQueryOnItem, db2 : Session):
    post = post.dict()
    searchWord = post['searchWord']
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
                    return{"status": 1,"message": message,"records":[{"item-name":row.itemName} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    message = "successful search"
                    return{"status": 1,"message": message,"records":[{"item-name":row.itemName} for row in records],"page_num": page_num,"total_pages": totalPages}
            
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""})    
async def sellerParty_list_search_query(post : ClientDataSearchQueryOnItem, db2 : Session):
    
    post = post.dict()
    searchWord = post['searchWord2']
    pageNum   = int(post["pageNum"])
    totalPages = int(post['totalPages'])
    records_per_page = 2

    try:
            baseQuery = db2.query(SellerPartyListModel.sellerName.label("partyName")).filter(SellerPartyListModel.sellerName.contains(searchWord)).group_by(SellerPartyListModel.sellerName)    
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
                    return{"status": 1,"message": message,"records":[{"party-name":row.partyName} for row in records],"page_num": page_num,"total_pages": total_pages}
            
            else:
                    page_num = pageNum
                    offset = (pageNum - 1) * records_per_page
                    records = baseQuery.offset(offset).limit(records_per_page).all()
                    message = "successful search"
                    return{"status": 1,"message": message,"records":[{"party-name":row.partyName} for row in records],"page_num": page_num,"total_pages": totalPages}
            
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}","records":[],"page_num":"","total_pages":""})