import sqlite3
import csv

# --- KONSTANTEN ---
DB_NAME = '../resources/pizza_orders.db'
CSV_SORTIMENT = '../resources/pizza_sortiment.csv'
DELIMITER = ';'

# --- BACKEND-FUNKTIONEN ---
def setup_database():
    """Erstellt die Datenbank und befüllt das Sortiment aus der CSV, falls die Tabelle leer ist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Tabelle für das Sortiment erstellen
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS sortiment
                   (
                       ID
                       INTEGER
                       PRIMARY
                       KEY,
                       Name
                       TEXT
                       NOT
                       NULL,
                       Belaege
                       TEXT,
                       Preis_Euro
                       REAL
                       NOT
                       NULL
                   )
                   """)

    # 2. Tabelle für die Bestellungen erstellen
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS bestellungen
                   (
                       ID
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       Timestamp
                       TEXT
                       NOT
                       NULL,
                       Gesamtkosten
                       REAL
                       NOT
                       NULL,
                       Details
                       TEXT
                   )
                   """)

    # 3. Sortiment aus CSV laden, falls die Sortimentstabelle leer ist
    cursor.execute("SELECT COUNT(*) FROM sortiment")
    if cursor.fetchone()[0] == 0:
        print("Datenbank: Sortiment wird aus CSV geladen...")
        _load_sortiment_from_csv(conn)

    conn.commit()
    conn.close()

def _load_sortiment_from_csv(conn):
    """Interne Funktion zum Befüllen der Sortimentstabelle aus der CSV."""
    cursor = conn.cursor()
    try:
        with open(CSV_SORTIMENT, mode='r', encoding='utf-8', newline='') as datei:
            csv_leser = csv.DictReader(datei, delimiter=DELIMITER)

            for zeile in csv_leser:
                # Daten in die Datenbank einfügen
                cursor.execute("""
                               INSERT INTO sortiment (ID, Name, Belaege, Preis_Euro)
                               VALUES (?, ?, ?, ?)
                               """, (
                                   int(zeile['ID']),
                                   zeile['Name'],
                                   zeile['Beläge'],
                                   float(zeile['Preis_Euro'])
                               ))
        print("Datenbank: Sortiment erfolgreich befüllt.")
    except FileNotFoundError:
        print(f"Fehler: Sortimentsdatei '{CSV_SORTIMENT}' nicht gefunden. DB bleibt leer.")
    except Exception as e:
        print(f"Fehler beim Laden der CSV in die DB: {e}")

# --- API-Funktionen für die Logik-Schicht ---
def get_sortiment():
    """Gibt das gesamte Sortiment als Dictionary {ID: Pizza-Daten} zurück."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Alle Pizzas abrufen
    cursor.execute("SELECT ID, Name, Belaege, Preis_Euro FROM sortiment ORDER BY ID")

    sortiment = {}
    for row in cursor.fetchall():
        pizza_id, name, belaege, preis = row
        sortiment[pizza_id] = {
            'ID': pizza_id,
            'Name': name,
            'Beläge': belaege,
            'Preis_Euro': preis
        }

    conn.close()
    return sortiment

def insert_bestellung(bestelldaten):
    """Fügt eine neue Bestellung in die 'bestellungen'-Tabelle ein."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Konvertiere Gesamtkosten zu Float vor dem Speichern
        gesamtkosten = float(bestelldaten['Gesamtkosten'])

        cursor.execute("""
                       INSERT INTO bestellungen (Timestamp, Gesamtkosten, Details)
                       VALUES (?, ?, ?)
                       """, (
                           bestelldaten['Timestamp'],
                           gesamtkosten,
                           bestelldaten['Details']
                       ))

        conn.commit()
        return True
    except Exception as e:
        print(f"Fehler beim Speichern der Bestellung in SQLite: {e}")
        return False
    finally:
        conn.close()

# Datenbank-Setup beim Start des Backends ausführen (nur falls direkt ausgeführt)
if __name__ == "__main__":
    setup_database()
    sortiment = get_sortiment()
    print(sortiment)
    print("Datenbank-Setup abgeschlossen.")