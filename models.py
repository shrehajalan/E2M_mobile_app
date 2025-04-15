from sqlalchemy import Boolean, Integer, String, Column, Float, Date, LargeBinary, PrimaryKeyConstraint,ForeignKey,Enum
from sqlalchemy.orm import declarative_base
#from database import Base,Base2,Base3

Base = declarative_base()
Base2 = declarative_base()
Base3 = declarative_base()


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
    uniqueCode = Column(String(4), unique=True, nullable=False)

#SELLER RELATED TABLE

class SellerPartyListModel(Base2):
    __tablename__ = "seller_party_list"

    sellerId = Column(Integer, primary_key=True,autoincrement=True,nullable=False, index=True,name="sellerid")
    sellerName = Column(String(50),nullable=False,name="PARTY_NAME")
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

class BuyerPartyListModel(Base2):
    __tablename__ = "buyer_party_list"

    buyerId = Column(Integer, primary_key=True,autoincrement=True,nullable=False, index=True,name="buyerid")
    buyerName = Column(String(50),nullable=False,name="PARTY_NAME")
    address = Column(String(50),name="Address",nullable=False)
    city =Column(String(50),name="city",nullable=False) 
    state = Column(String(50),name="State",nullable=False) 
    gst = Column(String(50),name="Gst num",nullable=False)
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

#TRANSACTION TABLE

class TransactionBuyerModel(Base2):
    __tablename__ = "transaction_buyer"
    
    invoice = Column(String(255),primary_key=True,name="Invoice no",index=True,nullable=False)
    buyerId = Column(Integer,name="buyerid",nullable=False)
    paymentStatus = Column(String(255),name="Payment_status",nullable=False)  
    amount = Column(Float,name="Amount",nullable=False)
    amountPaid = Column(Float,name="Amount_paid",nullable=False)
    dateBill =  Column(Date,name="Date_bill",nullable=False)

class TransactionSellerModel(Base2):
    __tablename__ = "transaction_seller"
    
    invoice = Column(String(255),primary_key=True,name="Invoice no",index=True,nullable=False)
    sellerId = Column(Integer,name="sellerid",nullable=False)
    paymentStatus = Column(String(255),name="Payment_status",nullable=False)  
    amount = Column(Float,name="Amount",nullable=False)
    amountPaid = Column(Float,name="Amount_paid",nullable=False)
    dateBill =  Column(Date,name="Date_bill",nullable=False)

#RESOURCE(LIKE EMPLOYEE) RELATED TABLE(ADMIN)

class EmployeeRegistrationModel(Base3):
    __tablename__ = "employee_registration"

    employeeId = Column(Integer, primary_key=True, autoincrement=True,index=True,nullable=False)
    name = Column(String(30), nullable=False)
    dateOfBirth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False) 
    mobileNum = Column(String(15), unique=True, nullable=False)  
    mailId = Column(String(15), unique=True, nullable=False)  
    address = Column(String(100), nullable=False)  
    zip = Column(String(10), nullable=False) 
    state = Column(String(20), nullable=False)
    proofType = Column(String(20), nullable=False)
    proofNumber = Column(String(20), unique=True, nullable=False) 
    photo = Column(String(1000), nullable=True)  # Base64-encoded string for photo
    bankName = Column(String(50), nullable=False)
    accountNumber = Column(String(30), unique=True, nullable=False)  
    ifscCode = Column(String(20), nullable=False)  
    upiId = Column(String(30), unique=True, nullable=True)  
    password= Column(String(30), nullable=True) 
    role = Column(String(10), nullable=True) 
    empReportingLatitude  = Column(Float, nullable=True) 
    empReportingLongitude = Column(Float, nullable=True) 

class EmployeeJobDetailsModel(Base3):
    __tablename__ = "employ_job_details"

    employeeId = Column(Integer, primary_key=True,autoincrement=True,index=True,nullable=False)
    designation  = Column(String(30), nullable=False)
    department  = Column(String(30), nullable=False)
    joinDate   = Column(Date, nullable=False)
    salary  = Column(Float, nullable=False)
    leavesPerMonth = Column(Integer,nullable=False, default=0)
    totalAdvance = Column(Float, nullable=False, default = 0.0)
    leavesCarriedForward = Column(Integer,nullable=False, default=0)

class EmployeeOtpModel(Base3):
    __tablename__ = "employee_otp"

    employeeId = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    otp = Column(String(6), nullable=False)

class EmployeeSalaryPaymentModel(Base3):
    __tablename__ = "employee_salary_payments"

    empPaymentId = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    employeeId = Column(Integer, ForeignKey("employee_registration.employeeId", ondelete="CASCADE"), nullable=False)
    salaryMonth = Column(String(20),nullable=False)
    salaryYear = Column(String(20),nullable=False)
    paymentDate = Column(Date, nullable=False) 
    paymentMode = Column(String(20),Enum("Cash", "Bank Transfer", "Cheque", name="paymentMode"), nullable=False)
    description =  Column(String(100),nullable=True, default="")
    amountPaid  = Column(Float, nullable=False)

class EmployeeExtraPaymentModel(Base3):
    __tablename__ = "employee_extra_payments"

    empExtraPaymentId = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    employeeId = Column(Integer,ForeignKey("employee_registration.employeeId",ondelete="CASCADE"), nullable=False)
    paymentDate = Column(Date, nullable=False) 
    paymentType = Column(String(20),Enum("Bonus", "Advance Given", "Advance Returned", name="paymentType"), nullable=False)  
    amount = Column(Float, nullable=False)
    description =  Column(String(100),nullable=True, default="")
    paymentMode = Column(String(20),Enum("Cash","Bank Transfer","Cheque","UPI","Advance Returned with Adjustment in Salary", name="paymentMode"), nullable=False)

class ExpenseModel(Base3):
    __tablename__ = "expense_data"

    expenseId = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    expenseDate = Column(Date, nullable=False) 
    expenseType = Column(String(20),Enum("Logistics", "Rents", "Miscelleneous", name="expenseType"), nullable=False)   
    paymentMode = Column(String(20),Enum("Cash","Net Banking","Cheque","UPI",name="paymentMode"), nullable=False)
    description = Column(String(100),nullable=True, default="")
    amount = Column(Float, nullable=False)
    
class EmployeeAttendanceModel(Base3):
    __tablename__ = "employee_attendance"

    attendanceId = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    employeeId = Column(Integer,ForeignKey("employee_registration.employeeId",ondelete="CASCADE"), nullable=False)
    attendanceDate = Column(Date, nullable=False) 
    curLatitude = Column(Float, nullable=False)
    curLongitude = Column(Float, nullable=False)
    empPresentStatus  =  Column(Integer, nullable=False, default=0)



