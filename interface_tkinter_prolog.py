# interface_tkinter_prolog.py - Interface pour la nouvelle version Prolog

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os

class PrologInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Système d'Enquête Policière Prolog")
        self.root.geometry("800x600")
        
        self.prolog_file = "enquete_prolog_tkinter.pl"
        self.setup_gui()
        
    def setup_gui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titre
        title_label = tk.Label(main_frame, text="🔍 SYSTÈME D'ENQUÊTE POLICIÈRE", 
                              font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Sélection
        ttk.Label(main_frame, text="Suspect:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.suspect_var = tk.StringVar()
        suspects = ['john', 'mary', 'alice', 'bruno', 'sophie']
        self.suspect_combo = ttk.Combobox(main_frame, textvariable=self.suspect_var, values=suspects, width=15)
        self.suspect_combo.grid(row=1, column=1, pady=5)
        self.suspect_combo.set('mary')
        
        ttk.Label(main_frame, text="Crime:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.crime_var = tk.StringVar()
        crimes = ['assassinat', 'vol', 'escroquerie']
        self.crime_combo = ttk.Combobox(main_frame, textvariable=self.crime_var, values=crimes, width=15)
        self.crime_combo.grid(row=2, column=1, pady=5)
        self.crime_combo.set('assassinat')
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="Vérifier Culpabilité", command=self.verifier_culpabilite).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Afficher Preuves", command=self.afficher_preuves).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Lancer Démo", command=self.lancer_demo).pack(side=tk.LEFT, padx=5)
        
        # Résultat
        result_frame = ttk.LabelFrame(main_frame, text="Résultats", padding="10")
        result_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=15, width=70, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.result_text.insert(tk.END, "💡 Interface connectée à Prolog\n\n")
    
    def executer_prolog(self, requete):
        """Exécute une requête Prolog et retourne le résultat"""
        try:
            # Crée un script temporaire
            with open('temp_run.pl', 'w', encoding='utf-8') as f:
                f.write(f":- consult('{self.prolog_file}').\n")
                f.write(f"start :- {requete}, halt.\n")
                f.write(":- start.\n")
            
            # Exécute Prolog
            result = subprocess.run(
                ['swipl', '-q', '-s', 'temp_run.pl'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if os.path.exists('temp_run.pl'):
                os.remove('temp_run.pl')
                
            return result.stdout.strip()
            
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def parser_resultat(self, output):
        """Parse le résultat formaté de Prolog"""
        if "RESULTAT:" in output and "PREUVES:" in output:
            lines = output.split('\n')
            resultat = lines[0].replace('RESULTAT:', '').strip()
            preuves = lines[1].replace('PREUVES:', '').strip()
            return resultat, preuves
        return None, output
    
    def verifier_culpabilite(self):
        suspect = self.suspect_var.get().strip()
        crime = self.crime_var.get().strip()
        
        if not suspect or not crime:
            messagebox.showerror("Erreur", "Sélectionnez un suspect et un crime")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Vérification de {suspect} pour {crime}...\n")
        
        resultat = self.executer_prolog(f"python_verifier({suspect}, {crime})")
        verdict, preuves = self.parser_resultat(resultat)
        
        if verdict:
            if verdict == 'coupable':
                message = f"✅ {suspect.capitalize()} est COUPABLE de {crime}"
                couleur = "red"
            else:
                message = f"❌ {suspect.capitalize()} est NON COUPABLE de {crime}"
                couleur = "green"
            
            self.result_text.insert(tk.END, f"{message}\n\n")
            self.result_text.insert(tk.END, f"Preuves: {preuves}\n")
            
            # Colorier le résultat
            self.result_text.tag_configure("verdict", foreground=couleur, font=("Arial", 12, "bold"))
            self.result_text.tag_add("verdict", "2.0", "2.end")
        else:
            self.result_text.insert(tk.END, f"Résultat: {resultat}\n")
    
    def afficher_preuves(self):
        suspect = self.suspect_var.get().strip()
        crime = self.crime_var.get().strip()
        
        if not suspect or not crime:
            messagebox.showerror("Erreur", "Sélectionnez un suspect et un crime")
            return
        
        self.result_text.delete(1.0, tk.END)
        
        resultat = self.executer_prolog(f"python_preuves({suspect}, {crime})")
        preuves = resultat.replace('PREUVES:', '').strip()
        
        self.result_text.insert(tk.END, f"🔍 Preuves contre {suspect} pour {crime}:\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        self.result_text.insert(tk.END, f"{preuves}\n")
    
    def lancer_demo(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "🎯 Lancement de la démo...\n")
        
        resultat = self.executer_prolog("python_demo")
        demo_result = resultat.replace('DEMO_RESULTATS:', '').strip()
        
        self.result_text.insert(tk.END, "Résultats de la démo:\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        self.result_text.insert(tk.END, f"{demo_result}\n")

def main():
    root = tk.Tk()
    app = PrologInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()