import tkinter as tk
from tkinter import ttk, messagebox
import time
# from backend.backend_db import lade_sortiment, speichere_bestellung
from backend.backend_csv import lade_sortiment, speichere_bestellung

# Lade das Sortiment einmalig
PIZZA_SORTIMENT = lade_sortiment()

class PizzaBestellApp:
    def __init__(self, master):
        self.master = master
        master.title("Pizza Bestellsystem (Tkinter)")

        self.warenkorb = {}
        self.gesamtkosten = 0.0

        # --- GUI Elemente initialisieren ---
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

        # 1. Sortiment (ListBox/Treeview)
        self.sortiment_frame = ttk.LabelFrame(master, text="Verfügbares Sortiment")
        self.sortiment_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.sortiment_frame.columnconfigure(0, weight=1)

        self.sortiment_listbox = self._create_sortiment_listbox(self.sortiment_frame)
        self.sortiment_listbox.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # 2. Warenkorb und Steuerung (Frame)
        self.control_frame = ttk.LabelFrame(master, text="Bestellung")
        self.control_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.rowconfigure(0, weight=1)

        # Warenkorb-Anzeige
        self.warenkorb_listbox = tk.Listbox(self.control_frame, height=5)
        self.warenkorb_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Gesamtbetrag Label
        self.gesamt_label = ttk.Label(self.control_frame, text="Gesamt: 0.00 €")
        self.gesamt_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Buttons
        self.add_button = ttk.Button(self.control_frame, text="Pizza hinzufügen", command=self.add_to_cart)
        self.add_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.order_button = ttk.Button(self.control_frame, text="BESTELLEN", command=self.place_order,
                                       style='Accent.TButton')
        self.order_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Initialen Warenkorb anzeigen
        self.update_cart_display()

    def _create_sortiment_listbox(self, parent_frame):
        """Erstellt und befüllt die Listbox für das Sortiment."""

        # Nutzen Sie eine Listbox, da sie einfacher ist als Treeview
        lb = tk.Listbox(parent_frame, height=len(PIZZA_SORTIMENT) + 1, selectmode=tk.SINGLE)

        if not PIZZA_SORTIMENT:
            lb.insert(tk.END, "FEHLER: Sortiment nicht geladen.")
            return lb

        # Header einfügen
        lb.insert(tk.END, f"{'ID':<4} | {'Name':<20} | {'Preis (€)':>10}")
        lb.itemconfig(0, {'bg': '#eee'})  # Header farblich abheben

        # Sortiment befüllen
        for pizza_id, pizza in sorted(PIZZA_SORTIMENT.items()):
            zeile = f"{pizza_id:<4} | {pizza['Name']:<20} | {pizza['Preis_Euro']:>10.2f}"
            lb.insert(tk.END, zeile)

        return lb

    def add_to_cart(self):
        """Fügt die ausgewählte Pizza zum Warenkorb hinzu."""

        try:
            # Selektierte Zeilennummer holen (Tkinter ist 0-basiert, Header ist 0)
            selected_index = self.sortiment_listbox.curselection()[0]

            # Die eigentlichen Daten beginnen bei Index 1
            if selected_index == 0:
                messagebox.showerror("Auswahlfehler", "Bitte wählen Sie eine gültige Pizza aus.")
                return

            # Holen der ID aus der sortierten Liste
            pizza_ids = sorted(PIZZA_SORTIMENT.keys())
            pizza_id = pizza_ids[selected_index - 1]

            pizza = PIZZA_SORTIMENT[pizza_id]

            self.warenkorb[pizza_id] = self.warenkorb.get(pizza_id, 0) + 1
            self.gesamtkosten += pizza['Preis_Euro']

            self.update_cart_display()

        except IndexError:
            messagebox.showerror("Auswahlfehler", "Bitte wählen Sie eine Pizza aus der Liste.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

    def update_cart_display(self):
        """Aktualisiert die Listbox und das Label des Warenkorbs."""

        self.warenkorb_listbox.delete(0, tk.END)  # Listbox leeren

        if not self.warenkorb:
            self.warenkorb_listbox.insert(tk.END, "Warenkorb ist leer.")
        else:
            for pizza_id, anzahl in self.warenkorb.items():
                pizza = PIZZA_SORTIMENT[pizza_id]
                kosten = anzahl * pizza['Preis_Euro']
                zeile = f"{anzahl}x {pizza['Name']} ({kosten:.2f} €)"
                self.warenkorb_listbox.insert(tk.END, zeile)

        self.gesamt_label.config(text=f"Gesamt: {self.gesamtkosten:.2f} €")

    def place_order(self):
        """Führt die Bestellung durch und speichert sie."""

        if not self.warenkorb:
            messagebox.showwarning("Bestellung leer", "Bitte fügen Sie zuerst Pizzen zum Warenkorb hinzu.")
            return

        # --- Daten für die Logik aufbereiten ---
        details = []
        for p_id, anzahl in self.warenkorb.items():
            name = PIZZA_SORTIMENT[p_id]['Name']
            preis = PIZZA_SORTIMENT[p_id]['Preis_Euro']
            details.append(f"{anzahl}x {name} ({preis:.2f}€)")

        bestelldaten = {
            'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'Gesamtkosten': f"{self.gesamtkosten:.2f}",
            'Details': " | ".join(details)
        }

        # Speichern über die Backend-Funktion
        if speichere_bestellung(bestelldaten):
            messagebox.showinfo("Bestellbestätigung",
                                f"Ihre Bestellung wurde erfolgreich gespeichert!\nGesamtkosten: {self.gesamtkosten:.2f} €")

            # Warenkorb zurücksetzen
            self.warenkorb = {}
            self.gesamtkosten = 0.0
            self.update_cart_display()
        else:
            messagebox.showerror("Fehler beim Speichern",
                                 "Die Bestellung konnte nicht in die CSV-Datei geschrieben werden.")

if __name__ == "__main__":
    if not PIZZA_SORTIMENT:
        messagebox.showerror("Startfehler", "Sortiment konnte nicht geladen werden. Bitte CSV prüfen.")
    else:
        root = tk.Tk()
        root.geometry("400x400")

        # Tkinter-Style für moderne Darstellung (optional)
        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'), foreground='blue')
        app = PizzaBestellApp(root)
        root.mainloop()