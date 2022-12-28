from io import StringIO

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import base64
from starlette.responses import FileResponse, Response

from app.rewind import make_rewind

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("../files/form.html", 'r') as form:
        form_d = form.read()
    return form_d


@app.post("/rewind")
def rewind(name, file: UploadFile = File(...)):
    text = file.file.read().decode('utf-8')
    # read file wiht pandas
    df = pd.read_csv(StringIO(text), sep=',', parse_dates=True)
    return Response(content=make_rewind(df, name), media_type="text/html")


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000)