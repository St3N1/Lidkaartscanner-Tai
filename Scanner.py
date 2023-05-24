import numpy as np
from pyzbar.pyzbar import decode
from datetime import datetime
import sqlite3
import cv2

cap = cv2.VideoCapture(0)


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


def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        naamVolledig = obj.data.decode("utf-8")[4:]

        index = 1
        for letter in naamVolledig:
            if letter != letter.upper():
                index += 1
            elif letter == letter.upper() and index != 1:
                achternaam = naamVolledig[:index]
                index = 1
        voornaam = naamVolledig[-index:]

        string = f"{str(voornaam)} {str(achternaam)}"
        cv2.putText(image, string, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        open_database()
        aanwezigheid_toevoegen(achternaam, voornaam, date.strftime("%d/%m/%Y"))


def scanner():
    while True:
        ret, frame = cap.read()
        decoder(frame)
        cv2.imshow('Scanner', frame)
        code = cv2.waitKey(10)
        if code == ord('q'):
            break


if __name__ == "__main__":
    scanner()
