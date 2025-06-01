from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
import json
from typing import Annotated, Literal, Optional, Dict

app = FastAPI()

class Data(BaseModel):
    name1: Annotated[str, Field(..., description = "Text 1 as name 1", example = "Reliance Retail Private Limited")]
    name2: Annotated[str, Field(..., description = "Text 2 as name 2", example = "Reliance Retail Pvt. Ltf.")]


def similarity_check(text1: str, text2: str):
    

@app.post("/process")
def process_names(data: Data):

    name1 = data.name1
    name2 = data.name2
    print(f'{name1} ... {name2}')