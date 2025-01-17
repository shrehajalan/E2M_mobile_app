from sqlalchemy import Boolean, Integer, String, Column, Float, Date, LargeBinary, PrimaryKeyConstraint
from database import Base,Base2

class ClientRegistrationModel(Base):
    __tablename__ = "ClientRegistration"

    clientId = Column(Integer, primary_key=True, index=True)
    userName= Column(String(50))
    emailId = Column(String(50))
    mobileNumber = Column(String(20))
    firmName = Column(String(50))
    location =Column(String(50))
    state=Column(String(50))
    country=Column(String(50))
    password=Column(String(100))
    status=Column(Integer)
    role=Column(String(10))

    
#SELLER RELATED TABLE
class SellerPartyListModel(Base):
    __tablename__ = "seller_party_list"

    sellerId = Column(Integer, primary_key=True,nullable=False, index=True,name="sellerid")
    partyName = Column(String(50),nullable=False,name="PARTY_NAME")
    address = Column(String(50),name="Address",nullable=False)
    city =Column(String(50),name="city",nullable=False) 
    state = Column(String(50),name="State",nullable=False) 
    gst = Column(String(50),name="Gst",nullable=False)
    seller_phone_num = Column(String(50),name="Seller phone num",nullable=False) 
    gmail  = Column(String(50),name="gmail",nullable=False) 
    debitAmt =Column(Float,name="DEBIT_amt",nullable=False) 
    creditAmt =Column(Float,name="CREDIT_amt",nullable=False)

class HistorySellModel(Base2):
    __tablename__ = "history_sell"

    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    invoiceNo = Column(String(255), index=True, name="Invoice no",nullable=False) 
    chalanNo = Column(Integer,name="chalan_no",nullable=False) 
    dateBill = Column(Date,name="Date_bill",nullable=False)
    sellerId = Column(Integer,name="sellerid",nullable=False)
    prodNum = Column(Integer,name="prod num",nullable=False)
    qty = Column(Integer,name="qty",nullable=False)
    unitPrice = Column(Float,name="unit_price",nullable=False)
    gst = Column(Float,name="GST",nullable=False)
    totalPrice = Column(Float,name="Total_price",nullable=False)


class HistoryHandBillModel(Base2):
    __tablename__ = "history_sell_handbill"

    invoiceNo = Column(String(255), name="Invoice no",nullable=False)  
    dateBill = Column(Date,name="Date_bill",nullable=False)
    sellerId = Column(Integer,name="sellerid",nullable=False)
    prodNum = Column(Integer,name="prod num",nullable=False)
    qty = Column(Integer,name="qty",nullable=False)
    unitPrice = Column(Float,name="unit_price",nullable=False)
    gst = Column(Float,name="GST",nullable=False)
    totalPrice = Column(Float,name="Total_price",nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("Invoice no", "prod num", name="pk_invoice_prod"),
    )

class HistorySellCashCustomerModel(Base2):
    __tablename__ = "history_sell_cash_customer"

    dateSell= Column(Date,name="Date_sell",nullable=False)
    prodNum = Column(Integer,name="prod num",nullable=False)
    qty = Column(Integer,name="qty",nullable=False)
    unitPrice = Column(Float,name="unit_price",nullable=False)
    totalPrice = Column(Float,name="Total_price",nullable=False) 
    chalanNo = Column(Integer, primary_key=True, name="chalan_no",nullable=False,index=True) 

class SellerSpecialRateModel(Base2):
    __tablename__ = "seller_special_rate"

    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False,index=True)
    sellerId= Column(Integer,name="sellerid",nullable=False,index=True)
    prodNum = Column(Integer, name="prod num",nullable=False) 
    rate = Column(Float,name="Rate",nullable=False)


#BUYER RELATED TABLES

class BuyerPartyListModel(Base):
    __tablename__ = "buyer_party_list"

    buyerId = Column(Integer, primary_key=True,nullable=False, index=True,name="buyerid")
    partyName = Column(String(50),nullable=False,name="PARTY_NAME")
    address = Column(String(50),name="Address",nullable=False)
    city =Column(String(50),name="city",nullable=False) 
    state = Column(String(50),name="State",nullable=False) 
    gst = Column(String(50),name="Gst",nullable=False)
    buyerPhone_num = Column(String(50),name="Buyer phone num",nullable=False) 
    gmail  = Column(String(50),name="gmail",nullable=False) 
    borrowedAmt =Column(Float,name="borrowed_amt",nullable=False) 
    paidAmt =Column(Float,name="Paid_amt",nullable=False)

class HistoryPurchaseModel(Base2):
    __tablename__ = "history_buy"

    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    invoiceNo = Column(String(255), index=True, name="Invoice no",nullable=False)  # Assuming not a primary key based on the provided structure
    dateBill = Column(Date,name="Date_bill",nullable=False)
    buyerId = Column(Integer,name="buyerid",nullable=False)
    prodNum = Column(Integer,name="prod num",nullable=False)
    qty = Column(Integer,name="qty",nullable=False)
    unitPrice = Column(Float,name="unit_price",nullable=False)
    gst = Column(Float,name="GST",nullable=False)
    totalPrice = Column(Float,name="Total_price",nullable=False)
    recNo = Column(Integer, primary_key=True, index=True, name="rec no",nullable=False)

class BuyerSpecialRateModel(Base2):
    __tablename__ = "buyer_special_rate"

    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False,index=True)
    buyerId= Column(Integer,name="buyerid",nullable=False,index=True)
    prodNum = Column(Integer, name="prod num",nullable=False) 
    rate = Column(Float,name="Rate",nullable=False)

#GST TABLE

class GstModel(Base2):
    __tablename__ = "gst"

    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False,index=True)
    date= Column(Date,name="date",nullable=False)
    invoiceNo = Column(String(255), index=True, name="invoice num",nullable=False) 
    type = Column(String(255),name="type",nullable=False)
    gstNum = Column(String(255),name="gst num",nullable=False)
    cgst = Column(Float,name="cgst",nullable=False) 
    sgst = Column(Float,name="sgst",nullable=False)
    igst = Column(Float,name="igst",nullable=False)

#PRODUCT LIST TABLE

class ProductListModel(Base2):
    __tablename__ = "product_list"

    prodNum = Column(Integer, primary_key=True, autoincrement=True,name="prod num",index=True,nullable=False)
    brand = Column(String(255), name="Brand",nullable=False)  # Assuming not a primary key based on the provided structure
    productDescription = Column(Date,name="product Description",nullable=False)
    imageData = Column(LargeBinary,name="ImageData",nullable=False)
    hsnCode = Column(String(255),name="HSN Code",nullable=False)
    gst = Column(Integer,name="GST",nullable=False)
    mrp = Column(Float,name="MRP",nullable=False)
    stock = Column(Float,name="Stock",nullable=False)
    perUnit =  Column(String(255),name="per_unit",nullable=False)
    qrCode=  Column(String(255),name="QR_code",nullable=False)











