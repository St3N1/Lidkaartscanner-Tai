from fastapi import FastAPI, HTTPException
import sqlite3
import os

app = FastAPI()


@app.get("/aanwezigheidlijst/{jaar}")
def aanwezigheidlijst_weergeven(jaar: int):
    if os.path.exists(f"Aanwezigheidlijst_{jaar}.db"):  
        conn = sqlite3.connect(f"Aanwezigheidlijst_{jaar}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Aanwezigheden")
        leden = cursor.fetchall()
    else:
        raise HTTPException(404, "Geen Aanwezigheidlijst gevonden.")

    if not leden:
        raise HTTPException(404, "Geen leden gevonden.")
    return leden


# @app.get("/aanwezigheidlijst/{jaar}/{maand}")
# def aanwezigheidlijst_weergeven(jaar: int, maand: int = None):
#     if os.path.exists(f"Aanwezigheidlijst_{jaar}.db"):
#         conn = sqlite3.connect(f"Aanwezigheidlijst_{jaar}.db")
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT * FROM Aanwezigheden WHERE strftime('%m', datum) = ?", (maand,))
#         leden = cursor.fetchall()
#     else:
#         raise HTTPException(404, "Geen Aanwezigheidlijst gevonden.")
    
#     if not leden:
#         raise HTTPException(404, "Geen leden gevonden.")
#     return leden
