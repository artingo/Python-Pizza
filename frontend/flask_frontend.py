import os

from flask import Flask, render_template, redirect, url_for, session
import time
# from backend.backend_csv import lade_sortiment, speichere_bestellung
from backend.backend_db import lade_sortiment, speichere_bestellung

projektverzeichnis = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__, root_path=projektverzeichnis)
# Ein geheimer Schlüssel ist für die Nutzung von Flask-Sessions erforderlich
app.secret_key = 'super_geheimer_schluessel_fuer_session'

# Lade das Sortiment einmalig beim Start der Anwendung
PIZZA_SORTIMENT = lade_sortiment()

# --- HELFERFUNKTIONEN ---
def berechne_warenkorb_details(warenkorb):
    """Berechnet die Gesamtkosten und bereitet die Details für das Template auf."""
    gesamtkosten = 0.0
    details = []

    for pizza_id, anzahl in warenkorb.items():
        pizza = PIZZA_SORTIMENT.get(int(pizza_id))
        if pizza:
            kosten = anzahl * pizza['Preis_Euro']
            gesamtkosten += kosten
            details.append({
                'id': pizza_id,
                'name': pizza['Name'],
                'anzahl': anzahl,
                'kosten': kosten
            })

    return details, gesamtkosten

# --- FLASK ROUTEN ---
@app.route('/', methods=['GET'])
def index():
    """Startseite: Zeigt das Sortiment und den aktuellen Warenkorb an."""
    if not PIZZA_SORTIMENT:
        return "Fehler: Sortiment konnte nicht geladen werden. Bitte CSV prüfen.", 500

    # Warenkorb aus der Session holen (oder leeres Dictionary, falls nicht vorhanden)
    warenkorb = session.get('warenkorb', {})

    # Details berechnen
    warenkorb_details, gesamtkosten = berechne_warenkorb_details(warenkorb)

    return render_template(
        'index.html',
        sortiment=PIZZA_SORTIMENT,
        warenkorb_details=warenkorb_details,
        gesamtkosten=gesamtkosten
    )

@app.route('/add/<int:pizza_id>', methods=['POST'])
def add_to_cart(pizza_id):
    """Fügt die ausgewählte Pizza zum Warenkorb hinzu."""

    if pizza_id not in PIZZA_SORTIMENT:
        return "Pizza nicht gefunden.", 404

    # Session-Warenkorb holen und aktualisieren
    warenkorb = session.get('warenkorb', {})
    warenkorb[str(pizza_id)] = warenkorb.get(str(pizza_id), 0) + 1
    session['warenkorb'] = warenkorb

    return redirect(url_for('index'))

@app.route('/remove/<int:pizza_id>', methods=['POST'])
def remove_from_cart(pizza_id):
    """Entfernt eine Pizza aus dem Warenkorb."""
    warenkorb = session.get('warenkorb', {})
    str_id = str(pizza_id)

    if str_id in warenkorb:
        warenkorb[str_id] -= 1
        if warenkorb[str_id] <= 0:
            del warenkorb[str_id]
        session['warenkorb'] = warenkorb

    return redirect(url_for('index'))

@app.route('/order', methods=['POST'])
def place_order():
    """Schließt die Bestellung ab und speichert sie in der CSV."""

    warenkorb = session.get('warenkorb', {})
    if not warenkorb:
        return redirect(url_for('index'))  # Nichts zu bestellen

    warenkorb_details, gesamtkosten = berechne_warenkorb_details(warenkorb)

    # Details für die Speicherung in der CSV aufbereiten
    csv_details = [f"{item['anzahl']}x {item['name']} ({item['kosten']:.2f}€)"
                   for item in warenkorb_details]

    bestelldaten = {
        'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'Gesamtkosten': f"{gesamtkosten:.2f}",
        'Details': " | ".join(csv_details)
    }

    # Logik-Funktion aufrufen
    if speichere_bestellung(bestelldaten):
        # Warenkorb leeren
        session.pop('warenkorb', None)
        return render_template('bestellung_abgeschlossen.html', gesamtkosten=gesamtkosten)
    else:
        # Fehlerseite oder Meldung anzeigen
        return "Fehler beim Speichern der Bestellung.", 500

if __name__ == '__main__':
    if PIZZA_SORTIMENT:
        print("Flask-Server gestartet. Öffne http://127.0.0.1:5000/")
        app.run(debug=True)
    else:
        print("Kann Server nicht starten: Sortiment ist leer.")