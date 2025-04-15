from pydantic import BaseModel, Field
from datetime import date

class ClientRegistration(BaseModel):
    userName : str
    emailId  : str
    mobileNumber : str
    firmName : str
    location  : str
    password  : str
    state : str
    country : str

class ClientLogin(BaseModel):
    mobileNumber : str
    password     : str

class ClientDataDashboard(BaseModel):
    clientId : str

class ClientDataSearchQuery(BaseModel):
   clientId : str
   sType : str
   typeFilter  : str
   searchWord : str
   startDate : str
   endDate : str
   pageNum  : str
   totalPages : str
   flag : str

class ClientDataSearchQueryOnItem(BaseModel):
   clientId : str
   sType : str
   typeFilter  : str
   typeFilter2  : str
   searchWord : str
   searchWord2 : str
   startDate : str
   endDate : str
   pageNum  : str
   curBuyPageNum : str
   curSellPageNum : str
   totalBuyPages: str
   totalCashSellPages : str
   totalAutoSellPages : str
   totalHandSellPages : str
   flag : str
   totalPages:str

class ClientDataInvoiceDetail(BaseModel):
    clientId : str
    invoice:str
    type:str

class ClientDataStockDetail(BaseModel):
    clientId : str
    type : str
    value : str
    pageNum : str
    totalPages : str
    flag : str

class EmployeeRegistration(BaseModel):
    clientId : str
    name : str
    dateOfBirth : str
    gender : str
    mobileNum : str
    mailId : str
    address : str
    zip : str
    state : str
    proofType : str
    proofNumber  : str
    photo : str# base64-encoded string if required
    bankName : str
    accountNumber : str
    ifscCode : str
    upiId : str
    designation : str
    department : str
    joinDate : str
    salary : str
    empReportingLatitude  : str
    empReportingLongitude  : str

class EmployeeLogin(BaseModel):
    empId : str
    password :str

class SetEmpPasswordDetails(BaseModel):
    empId : str
    otp : str
    newPassword : str
    flag : str
    clientId : str
    employeeNum : str
    
class EmployeeListFromName(BaseModel):
    clientId : str
    empName : str
    pageNum : str
    totalPages : str

class EmployeeSalaryEntryDetail(BaseModel):
     clientId : str
     empName : str
     employeeNum : str
     salaryMonth : str
     salaryYear : str
     paymentDate : str
     paymentMode : str
     description : str
     amountPaid : str
     flag : str
     availableLeaves : str
     leavesTaken : str
     nextMonthLeavesCarriedForward : str

class EmployeeExtraPaymentDetail(BaseModel):
            clientId : str
            empName : str
            employeeNum : str
            paymentDate : date
            paymentType : str
            paymentMode : str
            description : str
            amount : str

class ExpenseDetail(BaseModel):
    clientId : str
    expenseDate : date
    expenseType : str
    paymentMode : str
    description : str
    amount : str

class EmployeeAttendanceDetail(BaseModel):
    clientId : str
    employeeNum : str
    attendanceDate : date
    curLatitude : str
    curLongitude : str
    empPresentStatus : str
