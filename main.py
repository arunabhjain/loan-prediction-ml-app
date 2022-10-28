from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class request_body(BaseModel):
    gender:object
    married:object
    depend:object
    edu:object
    selfemp:object
    app:int
    coapp:float
    loan:float
    loanterm:float
    credit:float
    prop:object

#Train Model
df=pd.read_csv(r"loan_data.csv")
del df['Loan_ID']
X=df.drop("Loan_Status", axis=1)
y=df['Loan_Status']
X.Gender.fillna('Male', inplace=True)
X.Married.fillna('Yes', inplace=True)
X.Dependents.fillna('0', inplace=True)
X.Self_Employed.fillna('No', inplace=True)
X.LoanAmount.fillna(np.mean(X.LoanAmount), inplace=True)
X.Loan_Amount_Term.fillna(np.mean(X.Loan_Amount_Term), inplace=True)
X.Credit_History.fillna(1.0, inplace=True)
X=pd.get_dummies(X)
rfc=RandomForestClassifier()
rfc.fit(X, y)


def predict_output(gender, married, depend, edu, selfemp, app, coapp, loan, loanterm, credit,prop):
    value=[[gender, married, depend,edu, selfemp, app, coapp, loan, loanterm, credit, prop]]
    newdf=pd.DataFrame(value, columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
       'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
       'Loan_Amount_Term', 'Credit_History', 'Property_Area'])
    newdf=pd.get_dummies(newdf)
    missing_cols=set(X.columns)-set(newdf.columns)
    for i in missing_cols:
        newdf[i]=0
    newdf=newdf[X.columns]
    new_prediction=rfc.predict(newdf)
    if(new_prediction[0]=='Y'):
        return "Y"
    else:
        return "N"

    
@app.post("/")
async def predict_loan(result : request_body):   
    return {
        "result": predict_output(data.gender, data.married, data.depend, data.edu, data.selfemp, data.app, data.coapp, data.loan, data.loanterm, data.credit, data.prop)
    }
