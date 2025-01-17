from pydantic import BaseModel

class AmountCalc(BaseModel):
    type : str
    period : str


class ClientRegistration(BaseModel):
    userName : str
    emailId  : str
    mobileNumber : str
    firmName : str
    location  : str
    password  : str
    state:str
    country:str


class ClientLogin(BaseModel):
    mobileNumber : str
    password     : str

class ClientDataDashboard(BaseModel):
    userId : str
    token  : str

class ClientDataSearchQuery(BaseModel):
    searchWord : str
    pageNum  : str


