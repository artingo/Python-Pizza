# backend_csv.py
import csv
import os

# --- KONSTANTEN ---
CSV_SORTIMENT = "../resources/pizza_sortiment.csv"
CSV_BESTELLUNG = "../resources/bestellungen.csv"
DELIMITER = ';'

# --- BACKEND-FUNKTIONEN ---
def lade_sortiment():
    """Liest das Pizza-Sortiment aus der CSV-Datei in eine Liste von Dictionaries ein."""
    sortiment = {}
    try:
        with open(CSV_SORTIMENT, mode='r', encoding='utf-8', newline='') as datei:
            # DictReader ist ideal für CSV mit Header
            csv_leser = csv.DictReader(datei, delimiter=DELIMITER)
            for zeile in csv_leser:
                # Preise als Float speichern, ID als Integer für einfachen Zugriff
                pizza_id = int(zeile['ID'])
                zeile['Preis_Euro'] = float(zeile['Preis_Euro'])
                sortiment[pizza_id] = zeile
        return sortiment
    except FileNotFoundError:
        print(f"Fehler: Sortimentsdatei '{CSV_SORTIMENT}' nicht gefunden.")
        return {}
    except ValueError:
        print("Fehler: Konnte Preisdaten in der CSV nicht korrekt konvertieren.")
        return {}

def speichere_bestellung(bestelldaten):
    """Fügt eine abgeschlossene Bestellung zur Bestelldaten-CSV hinzu."""

    # 1. Prüfen, ob die Datei existiert, um den Header zu schreiben
    datei_existiert = os.path.exists(CSV_BESTELLUNG)

    # 2. Schreibe-Modus 'a' (append)
    try:
        with open(CSV_BESTELLUNG, mode='a', encoding='utf-8', newline='') as datei:
            # Definiere die Spaltennamen für die Bestelldatei
            fieldnames = ['Timestamp', 'Gesamtkosten', 'Details']
            csv_schreiber = csv.DictWriter(datei, fieldnames=fieldnames, delimiter=DELIMITER)

            # Schreibe den Header nur, wenn die Datei neu erstellt wird
            if not datei_existiert:
                csv_schreiber.writeheader()

            csv_schreiber.writerow(bestelldaten)

        return True
    except Exception as e:
        print(f"Fehler beim Speichern der Bestellung: {e}")
        return False