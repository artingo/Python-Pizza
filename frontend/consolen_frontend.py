import time
from backend.backend_csv import lade_sortiment, speichere_bestellung
# from backend.backend_db import lade_sortiment, speichere_bestellung

# Lade das Sortiment einmalig zu Beginn
PIZZA_SORTIMENT = lade_sortiment()

def zeige_sortiment(sortiment):
    """Zeigt das verfügbare Pizza-Sortiment in der Konsole an."""
    if not sortiment:
        print("Das Sortiment konnte nicht geladen werden.")
        return

    print("\n" + "=" * 40)
    print("🍕 PIZZA-SORTIMENT 🍕")
    print("=" * 40)
    print(f"{'ID':<4} | {'Name':<15} | {'Preis (€)':>10}")
    print("-" * 40)

    # Iteriere über die sortierten IDs
    for pizza_id, pizza in sorted(sortiment.items()):
        print(f"{pizza_id:<4} | {pizza['Name']:<15} | {pizza['Preis_Euro']:>10.2f}")
    print("=" * 40)

def bestellung_durchfuehren(sortiment):
    """Führt den interaktiven Bestellprozess durch."""

    warenkorb = {}
    gesamtkosten = 0.0

    while True:
        # Menü anzeigen
        zeige_sortiment(sortiment)
        print("Warenkorb: {} Artikel | Gesamt: {:.2f} €".format(
            sum(warenkorb.values()), gesamtkosten))
        print("\nGeben Sie die ID der Pizza ein, die Sie hinzufügen möchten.")
        auswahl = input("Oder 'B' für Bestellung abschließen, 'X' zum Abbrechen: ").strip().upper()

        if auswahl == 'X':
            print("Bestellung abgebrochen.")
            return

        if auswahl == 'B':
            if not warenkorb:
                print("Ihr Warenkorb ist leer!")
                continue
            break  # Bestellung abschließen

        try:
            pizza_id = int(auswahl)
            if pizza_id in sortiment:
                pizza = sortiment[pizza_id]

                # Pizza zum Warenkorb hinzufügen
                warenkorb[pizza_id] = warenkorb.get(pizza_id, 0) + 1
                gesamtkosten += pizza['Preis_Euro']
                print(f"'{pizza['Name']}' wurde hinzugefügt.")
            else:
                print("Ungültige ID. Bitte erneut versuchen.")
        except ValueError:
            print("Ungültige Eingabe.")

    # --- ABSCHLUSS ---
    details = []
    # Erstelle lesbare Details für die Speicherung
    for p_id, anzahl in warenkorb.items():
        name = sortiment[p_id]['Name']
        preis = sortiment[p_id]['Preis_Euro']
        details.append(f"{anzahl}x {name} ({preis:.2f}€)")

    bestelldaten = {
        'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'Gesamtkosten': f"{gesamtkosten:.2f}",
        # Füge die Details zu einem String zusammen
        'Details': " | ".join(details)
    }

    if speichere_bestellung(bestelldaten):
        print("\n========================================")
        print(f"🎉 BESTELLUNG ABGESCHLOSSEN 🎉")
        print(f"Ihre Gesamtkosten: {gesamtkosten:.2f} €")
        print("Die Bestellung wurde gespeichert.")
        print("========================================")
    else:
        print("\nEin Fehler ist beim Speichern aufgetreten.")

if __name__ == "__main__":
    if not PIZZA_SORTIMENT:
        print("System kann nicht gestartet werden. Bitte die Datei 'pizza_sortiment.csv' prüfen.")
    else:
        bestellung_durchfuehren(PIZZA_SORTIMENT)