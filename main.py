from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

class Data(BaseModel):
    name1: Annotated[str, Field(..., description = "Text 1 as name 1", example = "Reliance Retail Private Limited")]
    name2: Annotated[str, Field(..., description = "Text 2 as name 2", example = "Reliance Retail Pvt. Ltf.")]


def similarity_check(text1: str, text2: str):
    len_text1 = len(text1)
    len_text2 = len(text2)
    total_len = len_text1 + len_text2
    
    text1_set = set(text1)
    text2_set = set(text2)
    common_chars = len(text1_set.intersection(text2_set))
    similarity_perc = (2 * common_chars / total_len) * 100

    return round(similarity_perc,2)



@app.post("/process")
def process_names(data: Data):

    name1 = data.name1
    name2 = data.name2

    res = similarity_check(name1.lower(), name2.lower())
    print(f'{name1} ... {name2}.... {res}')

    return JSONResponse(status_code = 200, content = {
        "Similarity": res
    })