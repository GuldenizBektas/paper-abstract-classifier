from helpers.relabeler import relabel
from helpers import install_nltk
import joblib
import json
import pandas as pd
from fastapi import FastAPI
from fastapi import Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn


app = FastAPI()


class InputDoc(BaseModel):
  text  : str


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post('/predict')
def predict(doc : str = Body(...)):
    """
    Data cleaning part added for api usage only.
    Webapp requires these steps inside it's code file.
    """
    
    model  = joblib.load("models/svc_best_model_stemmed.joblib")
    result = model.predict([doc])
    label  = relabel(result[0])

    return {"text": doc, "label":label}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)