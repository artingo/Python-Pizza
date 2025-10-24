# backend_db.py
from . import db_connection as db

# Beim ersten Import die Datenbank einrichten (Tabellen erstellen und befüllen)
# db.setup_database()

def lade_sortiment():
    """Ruft das Sortiment aus der SQLite-Datenbank ab."""
    return db.get_sortiment()

def speichere_bestellung(bestelldaten):
    """Speichert die Bestellung in der SQLite-Datenbank."""
    return db.insert_bestellung(bestelldaten)