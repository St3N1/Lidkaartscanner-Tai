import sqlite3
from datetime import datetime
import cv2
from zxingcpp import read_barcodes
import numpy as np
from pyzbar.pyzbar import decode
import time

def aanwezigheid_toevoegen(achternaam, voornaam, datum):
    try:
        cursor.execute(
            "INSERT INTO Aanwezigheden (Achternaam, Voornaam, Datum) VALUES (?, ?, ?)", (achternaam, voornaam, datum))
    except sqlite3.IntegrityError:
        print("Lid staat er in.")
    DATABASE.commit()


def open_database():
    global date
    global FILENAME
    global DATABASE
    global cursor

    date = datetime.now()
    FILENAME = f'Aanwezigheidlijst_{date.strftime("%Y")}.db'
    DATABASE = sqlite3.connect(FILENAME)
    cursor = DATABASE.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Aanwezigheden
                    (Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Voornaam TEXT NOT NULL,
                    Achternaam TEXT NOT NULL,
                    Datum DATE NOT NULL, UNIQUE(Voornaam, Achternaam, Datum));''')


def decoder(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = read_barcodes(gray)
    barcode = decode(gray)

    gegevens = ""
    for code in barcodes:
        gegevens = code.text

    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

        if gegevens != "":
            voornaam = ""
            achternaam = ""
            switch = False
            for i, letter in enumerate(gegevens):
                if i > 3:
                    if letter == "_":
                        switch = True
                    elif switch:
                        voornaam += letter
                    else:
                        achternaam += letter

            if achternaam[0] != "A":
                open_database()
                aanwezigheid_toevoegen(
                    voornaam, achternaam, date.strftime("%d/%m/%Y"))
                cv2.putText(frame, f"{voornaam} {achternaam}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

def scanner():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        decoder(frame)
        
        cv2.imshow("Barcode Scanner", frame)
        
        code = cv2.waitKey(10)
        if code == ord('q'):
            break


if __name__ == "__main__":
    scanner()
