**Aktualisiert auf Deutsch:**

# Konsolen-Pizza-Bestellsystem

Dies ist eine einfache Konsolenanwendung in Python, die grundlegende Prinzipien der Systemintegration demonstriert. Der Fokus liegt dabei auf dem Lesen von Daten aus einer CSV-Datei (für die Speisekarte) und dem Zurückschreiben von Bestelldaten in eine separate CSV-Datei.

Das Projekt ist in ein Frontend (Konsolen-Benutzeroberfläche) und ein Backend (Datenverarbeitung) unterteilt.  



## 🚀 Funktionen

  * **Menü aus CSV laden:** Liest die Pizza-Auswahl und Preise aus der Datei `pizza_sortiment.csv`.
  * **Interaktive Konsolenbestellung:** Ermöglicht Benutzern, Artikel anhand ihrer ID auszuwählen und den Warenkorb zu überprüfen.
  * **Bestellspeicherung (Persistenz):** Speichert abgeschlossene Bestellungen, einschließlich Zeitstempel, Gesamtkosten und Artikeldetails, in der Datei `bestellungen.csv`.
  * **Klare Aufgabentrennung (Separation of Concerns):** Die Logik ist aufgeteilt in ein Frontend (`consolen_frontend.py`), das die Benutzeroberfläche darstellt, und ein Backend (`backend_csv.py`), das die Datenverarbeitung übernimmt.

## 📁 Projektstruktur

```
.
├── consolen_frontend.py  # Benutzeroberfläche und Hauptanwendungslogik
├── backend_csv.py        # Funktionen zum Lesen/Schreiben von CSV-Daten
└── resources/
    ├── pizza_sortiment.csv  # Eingabedatei für die Pizza-Speisekarte
    └── bestellungen.csv     # Ausgabedatei für alle gespeicherten Bestellungen
```

## 🛠️ Anforderungen

  * Python 3.x

## 🏁 Erste Schritte

1.  **Klonen Sie das Repository** (falls zutreffend) oder stellen Sie sicher, dass Sie alle Projektdateien haben.

2.  **Stellen Sie sicher, dass der Ordner `resources` existiert** und die Datei `pizza_sortiment.csv` mit den korrekten Headern (`ID`, `Name`, `Preis_Euro`, etc.) enthält.

3.  **Führen Sie die Hauptanwendungsdatei aus:**

    ```bash
    python consolen_frontend.py
    ```

## 💡 Funktionsweise

### `consolen_frontend.py`

Diese Datei verwaltet die Benutzerinteraktion:

  * Sie ruft `lade_sortiment()` vom Backend einmalig beim Start auf.
  * `zeige_sortiment(sortiment)` zeigt die Speisekarte (ID, Name, Preis) an.
  * `bestellung_durchfuehren(sortiment)` ist die zentrale Schleife:
      * Sie fordert den Benutzer zur Eingabe einer Pizza-ID auf, oder 'B' zum Abschließen, oder 'X' zum Abbrechen.
      * Sie verwaltet das Dictionary `warenkorb` und berechnet die `gesamtkosten`.
      * Nach Abschluss der Bestellung werden die Daten formatiert und die Funktion `speichere_bestellung()` aus dem Backend aufgerufen.

### `backend_csv.py`

Diese Datei kümmert sich um die Dateivorgänge:

  * **`lade_sortiment()`:**
      * Liest das Menü aus `pizza_sortiment.csv`.
      * Verwendet `csv.DictReader`, um Zeilen in Dictionaries umzuwandeln.
      * Konvertiert `ID` zu `int` und `Preis_Euro` zu `float`.
      * Gibt das Menü als Dictionary zurück, wobei die Pizza-ID der Schlüssel ist.
  * **`speichere_bestellung(bestelldaten)`:**
      * Fügt die Bestelldaten an die Datei `bestellungen.csv` an.
      * Schreibt automatisch den CSV-Header (`Timestamp`, `Gesamtkosten`, `Details`), falls die Datei noch nicht existiert.
      * Als Trennzeichen wird das **Semikolon (`;`)** verwendet.