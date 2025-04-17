from models import ClientRegistrationModel,HistoryPurchaseModel
from models import HistorySellCashCustomerModel,HistoryHandBillModel,HistorySellModel,ProductListModel
from fastapi import  HTTPException
from sqlalchemy.orm import Session
from datetime import date,datetime
from sqlalchemy import func,extract,case
from sqlalchemy import desc,union_all
from sqlalchemy import Integer
import calendar


async def MaxclientId(db:Session):
    try:
        result = db.query(ClientRegistrationModel).order_by(ClientRegistrationModel.clientId.desc()).first()
            # Return the highest clientId or 0 if the table is empty
        id = result.clientId if result else 0
        return ({"status": 1,"message":"successfully obtained","id":id})
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}"})

async def dashboardSale(db:Session):
    
    try:
        current_year = datetime.now().year
        current_month = datetime.now().month


        if current_month<4:
            current_year=current_year-1

        year_start_date=date(current_year, 4, 1)
        year_end_date=date(current_year+1, 3, 31)

        quarter = int(current_month/3)
        rem=int(current_month%3)
        if rem>0:
            quarter=quarter+1
      
        quarter_end_month = quarter * 3
        quarter_start_month = quarter_end_month -2
        quarter_month_range = list(range(quarter_start_month,quarter_end_month+1))

        resultautomated = (
        db.query(
            func.extract('YEAR', HistorySellModel.dateBill).label("year"),
            func.extract('MONTH', HistorySellModel.dateBill).label("month"),
            func.sum(HistorySellModel.totalPrice).label("total_price"),
            func.sum(HistorySellModel.gst).label("GST"),
            case(
                (
                    func.extract('MONTH', HistorySellModel.dateBill).in_(quarter_month_range),
                    (func.extract('DAY', HistorySellModel.dateBill) - 1) // 7 + 1
                ),
            else_=None)
        .label("week"),
        func.sum(
            case(
                    (
                        func.extract('MONTH', HistorySellModel.dateBill).in_(quarter_month_range),
                        HistorySellModel.totalPrice
                    ),
                else_=0
            )
        ).label("weekly_totalprice"),
        func.sum(
            case(
                    (
                        func.extract('MONTH', HistorySellModel.dateBill).in_(quarter_month_range),
                        HistorySellModel.gst
                    ),
                else_=0
            )).label("weekly_gst"))
        .filter(HistorySellModel.dateBill >= year_start_date, HistorySellModel.dateBill <=year_end_date)
        .group_by(
            func.extract('YEAR', HistorySellModel.dateBill), 
            func.extract('MONTH', HistorySellModel.dateBill),
            case(
                (
                    func.extract('MONTH', HistorySellModel.dateBill).in_(quarter_month_range),
                    (func.extract('DAY', HistorySellModel.dateBill) - 1) // 7 + 1
                ),
            else_=None
        )
        )
        .order_by(
        func.extract('YEAR', HistorySellModel.dateBill).asc(),
        func.extract('MONTH', HistorySellModel.dateBill).asc(),
        case(
                (
                    func.extract('MONTH', HistorySellModel.dateBill).in_(quarter_month_range),
                    (func.extract('DAY', HistorySellModel.dateBill) - 1) // 7 + 1
                ),
            else_=None
        ).asc()
        )
        .all())

        resultautomated_day= (
        db.query(
            func.extract('DAY', HistorySellModel.dateBill).label('day'),  # Extracting the day number
            func.sum(HistorySellModel.totalPrice).label('total_price'),  # Summing total price
            func.sum(HistorySellModel.gst).label('GST')  # Summing GST
        )
        .filter(
            func.extract('YEAR', HistorySellModel.dateBill) == datetime.now().year,
            func.extract('MONTH', HistorySellModel.dateBill) == datetime.now().month
        )
        .group_by(
            func.extract('DAY', HistorySellModel.dateBill)
        )
        .order_by(
            func.extract('DAY', HistorySellModel.dateBill).asc()
        )
        .all())

        print(resultautomated) 
        print(resultautomated_day)
    
        resulthand = (
        db.query(
            func.extract('YEAR', HistoryHandBillModel.dateBill).label("year"),
            func.extract('MONTH', HistoryHandBillModel.dateBill).label("month"),
            func.sum(HistoryHandBillModel.totalPrice).label("total_price"),
            func.sum(HistoryHandBillModel.gst).label("GST"),
            case(
                (
                    func.extract('MONTH', HistoryHandBillModel.dateBill).in_(quarter_month_range),
                    (func.extract('DAY', HistoryHandBillModel.dateBill) - 1) // 7 + 1
                ),
            else_=None)
        .label("week"),
        func.sum(
            case(
                    (
                        func.extract('MONTH', HistoryHandBillModel.dateBill).in_(quarter_month_range),
                        HistoryHandBillModel.totalPrice
                    ),
                else_=0
            )
        ).label("weekly_totalprice"),
        func.sum(
            case(
                    (
                        func.extract('MONTH', HistoryHandBillModel.dateBill).in_(quarter_month_range),
                        HistoryHandBillModel.gst
                    ),
                else_=0
            )
        ).label("weekly_gst")
        )
        .filter(HistoryHandBillModel.dateBill >= year_start_date, HistoryHandBillModel.dateBill <=year_end_date)
        .group_by(func.extract('YEAR', HistoryHandBillModel.dateBill), 
                  func.extract('MONTH', HistoryHandBillModel.dateBill),
                  case(
                (
                    func.extract('MONTH', HistoryHandBillModel.dateBill).in_(quarter_month_range),
                    (func.extract('DAY', HistoryHandBillModel.dateBill) - 1) // 7 + 1
                ),
            else_=None
        ))
        .order_by(
        func.extract('YEAR', HistoryHandBillModel.dateBill).asc(),
        func.extract('MONTH', HistoryHandBillModel.dateBill).asc(),
        case(
                (
                    func.extract('MONTH', HistoryHandBillModel.dateBill).in_(quarter_month_range),
                    (func.extract('DAY', HistoryHandBillModel.dateBill) - 1) // 7 + 1
                ),
            else_=None
        ).asc()
    )
        .all())
        resulthand_day= (
        db.query(
            func.extract('DAY', HistoryHandBillModel.dateBill).label('day'),  # Extracting the day number
            func.sum(HistoryHandBillModel.totalPrice).label('total_price'),  # Summing total price
            func.sum(HistoryHandBillModel.gst).label('GST')  # Summing GST
        )
        .filter(
            func.extract('YEAR', HistoryHandBillModel.dateBill) == current_year,
            func.extract('MONTH', HistoryHandBillModel.dateBill) == current_month
        )
        .group_by(
            func.extract('DAY', HistoryHandBillModel.dateBill)
        )
        .order_by(
            func.extract('DAY', HistoryHandBillModel.dateBill).asc()
        )
        .all())
        
        
        print(resulthand)

        resultcash = (
        db.query(
            func.extract('YEAR', HistorySellCashCustomerModel.dateSell).label("year"),
            func.extract('MONTH', HistorySellCashCustomerModel.dateSell).label("month"),
            func.sum(HistorySellCashCustomerModel.totalPrice).label("total_price"),
            case(
                (
                    func.extract('MONTH', HistorySellCashCustomerModel.dateSell).in_(quarter_month_range),
                    (func.extract('DAY', HistorySellCashCustomerModel.dateSell) - 1) // 7 + 1
                ),
            else_=None)
        .label("week"),
            func.sum(
            case(
                    (
                        func.extract('MONTH', HistorySellCashCustomerModel.dateSell).in_(quarter_month_range),
                        HistoryHandBillModel.totalPrice
                    ),
                else_=0
            )
        ).label("weekprice"))
        .filter(HistorySellCashCustomerModel.dateSell >= year_start_date, HistorySellCashCustomerModel.dateSell <=year_end_date)
        .group_by(func.extract('YEAR', HistorySellCashCustomerModel.dateSell), 
                  func.extract('MONTH', HistorySellCashCustomerModel.dateSell),
                  case(
                (
                    func.extract('MONTH', HistorySellCashCustomerModel.dateSell).in_(quarter_month_range),
                    (func.extract('DAY', HistorySellCashCustomerModel.dateSell) - 1) // 7 + 1
                ),
            else_=None
        ))
        .order_by(
        func.extract('YEAR', HistorySellCashCustomerModel.dateSell).asc(),
        func.extract('MONTH', HistorySellCashCustomerModel.dateSell).asc(),
        case(
                (
                    func.extract('MONTH', HistorySellCashCustomerModel.dateSell).in_(quarter_month_range),
                    (func.extract('DAY', HistorySellCashCustomerModel.dateSell) - 1) // 7 + 1
                ),
            else_=None
        ).asc())
        .all())
        resultcash_day= (
        db.query(
            func.extract('DAY', HistorySellCashCustomerModel.dateSell).label('day'),  # Extracting the day number
            func.sum(HistorySellCashCustomerModel.totalPrice).label('total_price')  # Summing total price
        )
        .filter(
            func.extract('YEAR', HistorySellCashCustomerModel.dateSell) == datetime.now().year,
            func.extract('MONTH', HistorySellCashCustomerModel.dateSell) == datetime.now().month
        )
        .group_by(
            func.extract('DAY', HistorySellCashCustomerModel.dateSell)
        )
        .order_by(
            func.extract('DAY', HistorySellCashCustomerModel.dateSell).asc()
        )
        .all())

        annually_total=0.0
        monthly_total=0.0
        quarterly_total=0.0
        days_in_month = calendar.monthrange(current_year, current_month)[1]
        curr_month_day_wise = [0.0] * days_in_month
        curr_quarter_week_wise = [0.0] * 12
        curr_year_month_wise = [0.0] * 12

        
        if resultautomated:
            for i in resultautomated:
                month=i[1]
                gst=i[3]
                total=i[2]
                total_gst = total+gst
                if current_month == month:
                    monthly_total = monthly_total + total_gst
                if month >= quarter_start_month and  month <= quarter_end_month:
                    quarterly_total = quarterly_total + total_gst
                    if month == quarter_month_range[0]:
                        index = i[4]-1
                    elif month == quarter_month_range[1]:
                        index = 4 + i[4]-1
                    elif month == quarter_month_range[2]:
                        index = 8 + i[4]-1
                    curr_quarter_week_wise[index] = curr_quarter_week_wise[index] + total + gst 
                annually_total=annually_total+total_gst
                curr_year_month_wise[i[1]-1] = curr_year_month_wise[i[1]-1] + total_gst
        
        if resultautomated_day:
            for i in resultautomated_day:
                day = i[0]-1
                total = i[1]
                gst = i[2]
                curr_month_day_wise[day] = total + gst
        
        if resulthand:
            for i in resulthand:
                month=i[1]
                gst=i[3]
                total=i[2]
                total_gst = total+gst
                if current_month == month:
                    monthly_total = monthly_total + total_gst
                if month>=quarter_start_month and  month<=quarter_end_month:
                    quarterly_total=quarterly_total+total_gst
                    if month == current_month:
                        index = i[4]-1
                    elif month == current_month+1:
                        index = 4 + i[4]-1
                    elif month == current_month+2:
                        index = 8 + i[4]-1
                    curr_quarter_week_wise[index] = curr_quarter_week_wise[index] + total + gst 
                annualy_total=annualy_total+total_gst
                curr_year_month_wise[i[1]-1] = curr_year_month_wise[i[1]-1] + total_gst
        
        if resulthand_day:
            for i in resulthand_day:
                day = i[0]-1
                total = i[1]
                gst = i[2]
                curr_month_day_wise[day] = curr_month_day_wise[day] + total + gst
        
        if resultcash:
            for i in resultcash:
                month=i[1]
                total=i[2]
                if current_month == month:
                     monthly_total = monthly_total + total
                if month>=quarter_start_month and  month<=quarter_end_month:
                    quarterly_total=quarterly_total+total
                    if month == quarter_month_range[0]:
                        index = i[4]-1
                    elif month == quarter_month_range[1]:
                        index = 4 + i[4]-1
                    elif month == quarter_month_range[2]:
                        index = 8 + i[4]-1
                    curr_quarter_week_wise[index] = curr_quarter_week_wise[index] + total
                annually_total=annually_total+total
                curr_year_month_wise[i[1]-1] = curr_year_month_wise[i[1]-1] + total

        if resultcash_day:
            for i in resultcash_day:
                day = i[0]-1
                total = i[1]
                gst = i[2]
                curr_month_day_wise[day] = curr_month_day_wise[day] + total + gst
            

        
        #TOP 5 ITEMS BASED ON UNITS SOLD
        subquery1 = (
        db.query(
            HistorySellCashCustomerModel.prodNum.label("product_number"),  # Group by product number
            func.sum(HistorySellCashCustomerModel.qty).label("total_volume"),
            func.count().label("record_count")  # Sum of total price for each product
        )
        .filter(
            HistorySellCashCustomerModel.dateSell >= year_start_date, 
            HistorySellCashCustomerModel.dateSell <= year_end_date
        )
        .group_by(HistorySellCashCustomerModel.prodNum)  # Group by prod_num
        #.order_by(desc(func.sum(HistorySellCashCustomerModel.qty)),desc(func.count()))  # Order by total sales in descending order
        .order_by(desc(func.count()))
        .limit(5)  # Get top 5 items
        .subquery())

        print("top_products_by_cash")
        print(subquery1)

        subquery2 = (
        db.query(
            HistorySellModel.prodNum.label("product_number"),  # Group by product number
            func.sum(HistorySellModel.qty).label("total_volume"),
            func.count().label("record_count")  # Sum of total price for each product
        )
        .filter(
            HistorySellModel.dateBill >= year_start_date, 
            HistorySellModel.dateBill <= year_end_date
        )
        .group_by(HistorySellModel.prodNum)  # Group by prod_num
        #.order_by(desc(func.sum(HistorySellModel.qty)),desc(func.count()))  # Order by total sales in descending order
        .order_by(desc(func.count()))
        .limit(5)  # Get top 5 items
        .all())
        subquery2_dic= {record.product_number: record.record_count for record in subquery2}

        subquery3 = (
        db.query(
            HistoryHandBillModel.prodNum.label("product_number"),  # Group by product number
            func.sum(HistoryHandBillModel.qty).label("total_volume"),
            func.count().label("record_count")  # Sum of total price for each product
        )
        .filter(
            HistoryHandBillModel.dateBill >= year_start_date, 
            HistoryHandBillModel.dateBill <= year_end_date
        )
        .group_by(HistoryHandBillModel.prodNum)  # Group by prod_num
        #.order_by(desc(func.sum(HistoryHandBillModel.qty)),desc(func.count()))  # Order by total sales in descending order
        .order_by(desc(func.count()))
        .limit(5)  # Get top 5 items
        .all())
        subquery3_dic= {record.product_number: record.record_count  for record in subquery3}

        top_5_products_dic = subquery2_dic.copy()
        for key, value in subquery3_dic.items():
            if key in top_5_products_dic:
                top_5_products_dic[key] = max(value, top_5_products_dic.get(key))
            else:
                top_5_products_dic[key] = subquery3_dic[key]
        
        top_5_products_dic = dict(sorted(top_5_products_dic.items(),key = lambda item:item[1],reverse=True)[:5])
        top_5_products_key = list(top_5_products_dic.keys())

  
        filtered_products_cash = (
        db.query(
            ProductListModel.prodNum.label("Product Number"),
            ProductListModel.productDescription.label("Product Name"),
            #subquery1.c.total_volume.label("Total Volume"),
            subquery1.c.record_count.label("Record Count")
        )
        .join(subquery1, ProductListModel.prodNum == subquery1.c.product_number)  # Join condition
        .all())

        filtered_products_credit = (
            db.query(
                 ProductListModel.prodNum.label("Product Number"),
                 ProductListModel.productDescription.label("Product Name"))
            .filter(
                ProductListModel.prodNum.in_(top_5_products_key))
            .all())

        filtered_products_cash_list = [
        {
            "product_number": item[0],
            "product_name": item[1],
            #"total_volume": float(item[2]),  # Convert Decimal to float
            "record_count": item[3]
        }for item in filtered_products_cash]

        filtered_products_credit_list = [
        {
            "product_number": item[0],
            "product_name": item[1],
            #"total_volume": float(item[2]),  # Convert Decimal to float
            "record_count": top_5_products_dic[item[0]]
        }for item in filtered_products_credit]
        
        current_year_calc = datetime.now().year
        monthly_total = int(monthly_total)
        quarterly_total = int(quarterly_total)
        annually_total = int(annually_total)
        curr_month_day_wise = [int(x) for x in curr_month_day_wise]
        curr_quarter_week_wise = [int(x) for x in curr_quarter_week_wise]
        curr_year_month_wise = [int(x) for x in curr_year_month_wise]
        current_month_name = calendar.month_name[current_month]+" "+str(current_year_calc)
        current_quarter_name = calendar.month_name[quarter_start_month]+" "+str(current_year_calc)+" - "+calendar.month_name[quarter_end_month]+" "+str(current_year_calc)
    
        current_year_name  = ("April"+" "+str(current_year_calc -1)+" - "+"March"+" "+str(current_year_calc) 
                              if current_month in [1,2,3]
                              else "April"+str(current_year_calc)+" - "+"March"+str(current_year_calc+1))
        
        curr_year_month_wise = curr_year_month_wise[3:]+curr_year_month_wise[0:3]
        
        start_date = datetime.strptime(f"1/{quarter_start_month}/{datetime.now().year}", "%d/%m/%Y")
        end_date = datetime.now() 
        days_difference = (end_date - start_date).days
        curr_week_num = (days_difference // 7)+1
        curr_day_num =  datetime.now().day

        return {"status":1,"message":"done successfully",
                "curr_day_num":curr_day_num,
                "curr_week_num":curr_week_num, 
                "name":[current_month_name,current_quarter_name,current_year_name],
                "value":[monthly_total,quarterly_total,annually_total],
                "graph":[curr_month_day_wise, curr_quarter_week_wise, curr_year_month_wise],
                "top_products_by_credit":filtered_products_credit_list,
                "top_products_by_cash":filtered_products_cash_list}
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}"})

async def dashboardPurchase(db:Session):
    
    try:
        current_year = datetime.now().year
        current_month = datetime.now().month

        if current_month<4:
            current_year=current_year-1
        year_start_date=date(current_year, 4, 1)
        year_end_date=date(current_year+1, 3, 31)

        quarter = int(current_month/3)
        rem=int(current_month%3)
        if rem>0:
            quarter=quarter+1
      
        quarter_end_month = quarter * 3
        quarter_start_month = quarter_end_month -2
        quarter_month_range = list(range(quarter_start_month,quarter_end_month+1))

        resultautomated = (
        db.query(
            func.extract('YEAR', HistoryPurchaseModel.dateBill).label("year"),
            func.extract('MONTH', HistoryPurchaseModel.dateBill).label("month"),
            func.sum(HistoryPurchaseModel.totalPrice).label("total_price"),
            func.sum(HistoryPurchaseModel.gst).label("GST"),
            case(
                (
                    func.extract('MONTH', HistoryPurchaseModel.dateBill).in_(quarter_month_range),
                    (func.extract('DAY', HistoryPurchaseModel.dateBill) - 1) // 7 + 1
                ),
                else_=None
                ).label("week"),
        func.sum(
            case(
                    (
                        func.extract('MONTH', HistoryPurchaseModel.dateBill).in_(quarter_month_range),
                        HistoryPurchaseModel.totalPrice
                    ),
                else_=0
                )
        ).label("weekly_totalprice"),
        func.sum(
            case(
                    (
                        func.extract('MONTH', HistoryPurchaseModel.dateBill).in_(quarter_month_range),
                        HistoryPurchaseModel.gst
                    ),
                else_=0
            )
        ).label("weekly_gst"))
        .filter(HistoryPurchaseModel.dateBill >= year_start_date, HistoryPurchaseModel.dateBill <=year_end_date)
        .group_by(func.extract('YEAR', HistoryPurchaseModel.dateBill),
                  func.extract('MONTH', HistoryPurchaseModel.dateBill),
                  case(
                    (func.extract('MONTH', HistoryPurchaseModel.dateBill).in_(quarter_month_range),
                    (func.extract('DAY', HistoryPurchaseModel.dateBill) - 1) // 7 + 1),
                    else_=None
                    ))
        .order_by(
        func.extract('YEAR', HistoryPurchaseModel.dateBill).asc(),
        func.extract('MONTH', HistoryPurchaseModel.dateBill).asc(),
        case(
                (
                    func.extract('MONTH', HistoryPurchaseModel.dateBill).in_(quarter_month_range),
                    (func.extract('DAY', HistoryPurchaseModel.dateBill) - 1) // 7 + 1
                ),
            else_=None
        ).asc())
        .all())

        resultautomated_day= (
        db.query(
            func.extract('DAY', HistoryPurchaseModel.dateBill).label('day'),  # Extracting the day number
            func.sum(HistoryPurchaseModel.totalPrice).label('total_price'),  # Summing total price
            func.sum(HistoryPurchaseModel.gst).label('GST')  # Summing GST
        )
        .filter(
            func.extract('YEAR', HistoryPurchaseModel.dateBill) == datetime.now().year,
            func.extract('MONTH', HistoryPurchaseModel.dateBill) == datetime.now().month
        )
        .group_by(
            func.extract('DAY', HistoryPurchaseModel.dateBill)
        )
        .order_by(
            func.extract('DAY', HistoryPurchaseModel.dateBill).asc()
        )
        .all())
        
        annually_total=0.0
        monthly_total=0.0
        quarterly_total=0.0
        days_in_month = calendar.monthrange(current_year, current_month)[1]
        curr_month_day_wise = [0.0] * days_in_month
        curr_quarter_week_wise = [0.0] * 12
        curr_year_month_wise = [0.0] * 12

        if resultautomated:
            for i in resultautomated:
                month=i[1]
                gst=i[2]
                total=i[3]
                total_gst = total + gst
                if current_month == month:
                    monthly_total = monthly_total + total_gst
                if month >= quarter_start_month and  month <= quarter_end_month:
                    quarterly_total = quarterly_total + total_gst
                    if month == quarter_month_range[0]:
                        index = i[4]-1
                    elif month == quarter_month_range[1]:
                        index = 4 + i[4]-1
                    elif month == quarter_month_range[2]:
                        index = 8 + i[4]-1
                    curr_quarter_week_wise[index] = curr_quarter_week_wise[index] + total_gst 
                annually_total=annually_total+total_gst
                curr_year_month_wise[i[1]-1] = curr_year_month_wise[i[1]-1] + total_gst
            
        if resultautomated_day:
            for i in resultautomated_day:
                day = i[0]-1
                total = i[1]
                gst = i[2]
                curr_month_day_wise[day] = total + gst

        monthly_total = int(monthly_total)
        quarterly_total = int(quarterly_total)
        annually_total = int(annually_total)
        curr_month_day_wise = [int(x) for x in curr_month_day_wise]
        curr_quarter_week_wise = [int(x) for x in curr_quarter_week_wise]
        curr_year_month_wise = [int(x) for x in curr_year_month_wise]
        curr_year_month_wise = curr_year_month_wise[3:]+curr_year_month_wise[0:3]
        
        return {"status":1,"message":"calculated successfully","value":[monthly_total,quarterly_total,annually_total],"graph":[curr_month_day_wise, curr_quarter_week_wise,curr_year_month_wise]}
    except Exception as e:
        return({"status": 0,"message":f"Error: {e}"})
