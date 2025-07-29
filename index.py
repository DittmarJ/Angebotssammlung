import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Angebot:
    def __init__(self, name, beschreibung, anleitung, ferien):
        self.name = name
        self.beschreibung = beschreibung
        self.anleitung = anleitung
        self.ferien = ferien
        self.erstellt_am = datetime.now().strftime("%d.%m.%Y %H:%M")

class AngebotsManager:
    def __init__(self):
        self.angebote = []
    
    def add_angebot(self, angebot):
        self.angebote.append(angebot)
    
    def get_angebote(self):
        return self.angebote
        # Sortierung nach Erstellungsdatum (neueste zuerst)
        return sorted(self.angebote, key=lambda x: datetime.strptime(x.erstellt_am, "%d.%m.%Y %H:%M"), reverse=True)

class AngebotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Angebotsmanager")
        self.root.geometry("1000x700")
        self.style = ttk.Style()
        self.configure_styles()
        self.manager = AngebotsManager()
        
        self.setup_ui()
    
    def configure_styles(self):
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=5)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        self.style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        self.style.map('TButton', 
                      foreground=[('pressed', 'white'), ('active', 'white')],
                      background=[('pressed', '#0052cc'), ('active', '#0066ff')])
    
    def setup_ui(self):
        # Notebook für Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab für Neueingabe
        self.input_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.input_frame, text="Neues Angebot")
        self.create_input_form()
        
        # Tab für Übersicht
        self.overview_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.overview_frame, text="Angebotsübersicht")
        self.create_overview()
        
        # Starte mit der Übersicht
        self.refresh_overview()
    
    def create_input_form(self):
        # Header
        header = ttk.Label(self.input_frame, text="Neues Angebot erstellen", font=('Segoe UI', 12, 'bold'))
        header.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)
        
        # Formularfelder
        ttk.Label(self.input_frame, text="Angebotsname:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self.input_frame, width=50, font=('Segoe UI', 10))
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(self.input_frame, text="Kurze Beschreibung:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.beschreibung_entry = ttk.Entry(self.input_frame, width=50, font=('Segoe UI', 10))
        self.beschreibung_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(self.input_frame, text="Lange Anleitung:").grid(row=3, column=0, sticky=tk.NW, pady=5)
        self.anleitung_text = tk.Text(self.input_frame, width=50, height=10, wrap=tk.WORD, 
                                    font=('Segoe UI', 10), padx=5, pady=5)
        self.anleitung_text.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Scrollbar für Anleitung
        scrollbar = ttk.Scrollbar(self.input_frame, command=self.anleitung_text.yview)
        scrollbar.grid(row=3, column=2, sticky=tk.NS)
        self.anleitung_text.config(yscrollcommand=scrollbar.set)
        
        ttk.Label(self.input_frame, text="Ferienauswahl:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.ferien_var = tk.StringVar()
        ferien_options = ["Fasnacht", "Ostern", "Pfingsten", "Sommer", "Herbst"]
        self.ferien_combobox = ttk.Combobox(self.input_frame, textvariable=self.ferien_var, 
                                          values=ferien_options, state="readonly",
                                          font=('Segoe UI', 10))
        self.ferien_combobox.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Speichern Button
        save_button = ttk.Button(self.input_frame, text="Angebot speichern", 
                               command=self.save_angebot, style='Accent.TButton')
        save_button.grid(row=5, column=1, padx=10, pady=20, sticky=tk.E)
        
        # Styling für den Accent Button
        self.style.configure('Accent.TButton', foreground='white', background='#0078d7')
    
    def create_overview(self):
        # Header
        header = ttk.Label(self.overview_frame, text="Gespeicherte Angebote", font=('Segoe UI', 12, 'bold'))
        header.pack(anchor=tk.W, pady=(0, 10))
        
        # Treeview für die Angebotsübersicht
        tree_frame = ttk.Frame(self.overview_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Beschreibung", "Ferien", "Erstellt am"), 
                               show="headings", selectmode="browse")
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Spalten konfigurieren
        self.tree.heading("Name", text="Angebotsname", anchor=tk.W)
        self.tree.heading("Beschreibung", text="Beschreibung", anchor=tk.W)
        self.tree.heading("Ferien", text="Ferien", anchor=tk.W)
        self.tree.heading("Erstellt am", text="Erstellt am", anchor=tk.W)
        
        self.tree.column("Name", width=200, anchor=tk.W)
        self.tree.column("Beschreibung", width=300, anchor=tk.W)
        self.tree.column("Ferien", width=100, anchor=tk.W)
        self.tree.column("Erstellt am", width=150, anchor=tk.W)
        
        # Details Frame
        details_frame = ttk.LabelFrame(self.overview_frame, text="Anleitungsdetails", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.anleitung_display = tk.Text(details_frame, height=10, wrap=tk.WORD, 
                                       state=tk.DISABLED, font=('Segoe UI', 10),
                                       padx=5, pady=5)
        self.anleitung_display.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar für Anleitungsdetails
        scrollbar = ttk.Scrollbar(details_frame, command=self.anleitung_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.anleitung_display.config(yscrollcommand=scrollbar.set)
        
        # Auswahl-Ereignis
        self.tree.bind("<<TreeviewSelect>>", self.show_details)
        
        # Aktualisieren Button
        button_frame = ttk.Frame(self.overview_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        refresh_button = ttk.Button(button_frame, text="Liste aktualisieren", 
                                 command=self.refresh_overview)
        refresh_button.pack(side=tk.RIGHT)
    
    def save_angebot(self):
        name = self.name_entry.get().strip()
        beschreibung = self.beschreibung_entry.get().strip()
        anleitung = self.anleitung_text.get("1.0", tk.END).strip()
        ferien = self.ferien_var.get()
        
        if not all([name, beschreibung, anleitung, ferien]):
            messagebox.showwarning("Eingabe unvollständig", "Bitte füllen Sie alle Felder aus!")
            return
        
        # Prüfen ob Angebot mit diesem Namen bereits existiert
        for existing in self.manager.get_angebote():
            if existing.name.lower() == name.lower():
                messagebox.showwarning("Name existiert", 
                                      "Ein Angebot mit diesem Namen existiert bereits!")
                return
        
        angebot = Angebot(name, beschreibung, anleitung, ferien)
        self.manager.add_angebot(angebot)
        
        # Felder zurücksetzen
        self.name_entry.delete(0, tk.END)
        self.beschreibung_entry.delete(0, tk.END)
        self.anleitung_text.delete("1.0", tk.END)
        self.ferien_var.set("")
        
        messagebox.showinfo("Erfolg", "Angebot wurde erfolgreich gespeichert!")
        self.refresh_overview()
        self.notebook.select(1)  # Zur Übersicht wechseln
    
    def refresh_overview(self):
        # Treeview leeren
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Angebote laden (sortiert nach Datum, neueste zuerst)
        angebote = sorted(self.manager.get_angebote(), 
                         key=lambda x: datetime.strptime(x.erstellt_am, "%d.%m.%Y %H:%M"), 
                         reverse=True)
        
        # Angebote einfügen
        for angebot in angebote:
            self.tree.insert("", tk.END, values=(
                angebot.name,
                angebot.beschreibung,
                angebot.ferien,
                angebot.erstellt_am
            ))
    
    def show_details(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        
        item_data = self.tree.item(selected_item)
        angebot_name = item_data['values'][0]
        
        # Passendes Angebot finden
        for angebot in self.manager.get_angebote():
            if angebot.name == angebot_name:
                self.anleitung_display.config(state=tk.NORMAL)
                self.anleitung_display.delete("1.0", tk.END)
                self.anleitung_display.insert("1.0", angebot.anleitung)
                self.anleitung_display.config(state=tk.DISABLED)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = AngebotApp(root)
    root.mainloop()
