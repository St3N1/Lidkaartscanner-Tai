from flask import Flask, jsonify, redirect
import sqlite3
import os

app = Flask(__name__)


@app.route("/")
def main():
    return redirect("/aanwezigheidlijst/<jaar>")

@app.route("/aanwezigheidlijst/<jaar>")
def aanwezigheidlijst_weergeven(jaar: int):
    if os.path.exists(f"Aanwezigheidlijst_{jaar}.db"):
        conn = sqlite3.connect(f"Aanwezigheidlijst_{jaar}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Aanwezigheden")
        leden = cursor.fetchall()
    else:
        return jsonify("Geen aanwezigheidlijst gevonden."), 404

    if not leden:
        return jsonify("Geen leden gevonden."), 404
    return jsonify(leden), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
