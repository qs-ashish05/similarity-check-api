from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

class Data(BaseModel):
    name1: Annotated[str, Field(..., description = "Text 1 as name 1", example = "Reliance Retail Private Limited")]
    name2: Annotated[str, Field(..., description = "Text 2 as name 2", example = "Reliance Retail Pvt. Ltf.")]


def levenshtein_distance(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    # Initialize a matrix of size (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming empty string to the other
    for i in range(m + 1):
        dp[i][0] = i  # Deletion
    for j in range(n + 1):
        dp[0][j] = j  # Insertion

    # Compute distances
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0  # No operation needed
            else:
                cost = 1  # Substitution
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Deletion
                dp[i][j - 1] + 1,      # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )
    return dp[m][n]

def similarity_percentage(s1: str, s2: str) -> float:
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 100.0  # Both strings are empty
    similarity = (1 - distance / max_len) * 100
    return round(similarity, 2)



@app.post("/process")
def process_names(data: Data):

    name1 = data.name1
    name2 = data.name2

    res = similarity_percentage(name1.lower(), name2.lower())
    print(f'{name1} ... {name2}.... {res}')

    return JSONResponse(status_code = 200, content = {
        "Similarity": res
    })