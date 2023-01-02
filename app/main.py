from io import StringIO

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import csv
import pandas_lite as pd
from starlette.responses import Response

from app.rewind import make_rewind
from app.utils import try_parse_date

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("files/form.html", 'r') as form:
        form_d = form.read()
    return form_d


@app.post("/rewind")
def rewind(name, file: UploadFile = File(...)):
    text = file.file.read().decode('utf-8')
    reader = csv.DictReader(StringIO(text), delimiter=',')

    data = {}

    # Iterate over the rows of the file
    for row in reader:
        if try_parse_date(row["Date"]).year != 2022:
            continue
        # Iterate over the keys and values in the row
        for key, value in row.items():
            # Initialize the array for the key if it doesn't exist
            if key not in data:
                data[key] = []
            # Add the value to the array
            data[key].append(value)

    df = pd.DataFrame(data)

    return Response(content=make_rewind(df, name), media_type="text/html")


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000)