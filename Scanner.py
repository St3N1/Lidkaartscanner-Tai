import sqlite3
from datetime import datetime
import cv2
from zxingcpp import read_barcodes


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
                    Achternaam TEXT NOT NULL,
                    Voornaam TEXT NOT NULL,
                    Datum DATE NOT NULL, UNIQUE(Achternaam, Voornaam, Datum));''')


def scanner():
    cap = cv2.VideoCapture("http://192.168.1.178:4000/video")
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = read_barcodes(gray)

        gegevens = ""
        for code in barcodes:
            gegevens = code.text
                
        if gegevens != "":
            voornaam = ""
            achternaam = ""
            switch = False
            for i, letter in enumerate(gegevens):
                if switch:
                    voornaam += letter
                else:
                    achternaam += letter

                if gegevens[i] == gegevens[i].upper() and gegevens[i-1] != " " and i != 0 and gegevens[i] != " ":
                    switch = True

            voornaam = achternaam[len(achternaam)-1:] + voornaam
            achternaam = achternaam[:len(achternaam)-1]

            if achternaam != "A":
                open_database()
                aanwezigheid_toevoegen(achternaam, voornaam, date.strftime("%d/%m/%Y"))

        cv2.imshow("Barcode Scanner", frame)

        code = cv2.waitKey(10)
        if code == ord('q'):
            break


if __name__ == "__main__":
    scanner()
