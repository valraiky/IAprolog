# 🔍 Système d'Enquête Policière - Prolog & Python

## 📖 Table des Matières
- [Introduction](#-introduction)
- [Architecture du Projet](#-architecture-du-projet)
- [Fonctionnement de Prolog](#-fonctionnement-de-prolog)
- [Structure des Données](#-structure-des-données)
- [Règles Métier](#-règles-métier)
- [Interface Graphique](#-interface-graphique)
- [Installation et Utilisation](#-installation-et-utilisation)
- [Exemples d'Utilisation](#-exemples-dutilisation)
- [Structure des Fichiers](#-structure-des-fichiers)

## 🎯 Introduction

Ce projet est un système expert d'enquête policière développé en **Prolog** avec une interface graphique **Python/Tkinter**. Il permet de déterminer la culpabilité de suspects basée sur des preuves et des règles logiques.

## 🏗️ Architecture du Projet

### 🔄 Interaction Prolog-Python
```
Python Tkinter Interface → Appel → Prolog Engine → Résultat → Affichage Python
```

### 📋 Composants
- **Moteur Logique** : Prolog (règles métier)
- **Interface Utilisateur** : Python Tkinter
- **Base de Faits** : Enregistrée en Prolog
- **Système d'Inférence** : Moteur Prolog intégré

## 🧠 Fonctionnement de Prolog

### ⚡ Qu'est-ce que Prolog ?
Prolog (**PRO**grammation **LOG**ique) est un langage de programmation logique basé sur :
- **Faits** : Données de base (`has_motive(mary, assassinat).`)
- **Règles** : Logique déductive (`is_guilty/2`)
- **Requêtes** : Questions posées au système (`?- is_guilty(mary, assassinat).`)

### 🎯 Comment Prolog fonctionne dans ce projet

#### 1. Base de Faits
```prolog
% Suspects et crimes
suspect(john).
suspect(mary).
crime_type(assassinat).

% Preuves
has_motive(mary, assassinat).
was_near_crime_scene(mary, assassinat).
```

#### 2. Règles de Culpabilité
```prolog
is_guilty(Suspect, assassinat) :-
    has_motive(Suspect, assassinat),
    was_near_crime_scene(Suspect, assassinat),
    has_fingerprint_on_weapon(Suspect, assassinat).
```

#### 3. Inférence Automatique
Quand vous demandez `is_guilty(mary, assassinat)`, Prolog :
1. ✅ Vérifie si Mary a un motif
2. ✅ Vérifie si Mary était sur les lieux  
3. ✅ Vérifie si Mary a des empreintes sur l'arme
4. ✅ Retourne `true` si toutes les conditions sont remplies

## 📊 Structure des Données

### 🧾 Types de Crimes
```prolog
crime_type(assassinat).
crime_type(vol).
crime_type(escroquerie).
```

### 👥 Suspects
```prolog
suspect(john).
suspect(mary).
suspect(alice).
suspect(bruno).
suspect(sophie).
```

### 🔍 Preuves Disponibles
| Preuve | Description |
|--------|-------------|
| `has_motive/2` | Le suspect a un motif |
| `was_near_crime_scene/2` | Présent sur les lieux |
| `has_fingerprint_on_weapon/2` | Empreintes sur l'arme |
| `has_bank_transaction/2` | Transaction bancaire suspecte |
| `owns_fake_identity/2` | Possède une fausse identité |

## ⚖️ Règles Métier

### 🗡️ Crime d'Assassinat
```prolog
is_guilty(Suspect, assassinat) :-
    has_motive(Suspect, assassinat),           % Motif
    was_near_crime_scene(Suspect, assassinat), % Présence sur lieux
    has_fingerprint_on_weapon(Suspect, assassinat). % Empreintes
```

### 💳 Crime d'Escroquerie  
```prolog
is_guilty(Suspect, escroquerie) :-
    has_motive(Suspect, escroquerie)           % Motif
    ; has_bank_transaction(Suspect, escroquerie) % Transaction
    ; owns_fake_identity(Suspect, escroquerie). % Fausse identité
```

### 🎒 Crime de Vol
```prolog
is_guilty(Suspect, vol) :-
    has_motive(Suspect, vol),
    was_near_crime_scene(Suspect, vol), 
    has_fingerprint_on_weapon(Suspect, vol).
```

## 🖥️ Interface Graphique

### 🎨 Fonctionnalités de l'Interface
- **Menus déroulants** pour sélection des suspects et crimes
- **Boutons interactifs** pour vérification et démonstration
- **Affichage coloré** des résultats (✅ Coupable / ❌ Non coupable)
- **Zone de défilement** pour les preuves détaillées
- **Gestion d'erreurs** complète

### 🔄 Communication Prolog-Python
```python
# Dans l'interface Python
resultat = executer_prolog("python_verifier(mary, assassinat)")

# Prolog retourne un format structuré :
# "RESULTAT:coupable\nPREUVES:motif, presence_lieux, empreintes_arme"
```

## 🚀 Installation et Utilisation

### 📦 Prérequis
```bash
# Installation de SWI-Prolog
# Ubuntu/Debian
sudo apt-get install swi-prolog

# macOS
brew install swi-prolog

# Windows: Télécharger depuis https://www.swi-prolog.org
```

### 🏃‍♂️ Lancement du Projet
```bash
# 1. Téléchargez tous les fichiers dans le même dossier
# 2. Lancez l'interface graphique
python interface_tkinter_prolog.py

# 3. Ou testez en ligne de commande Prolog
swipl -s enquete_prolog_tkinter.pl
?- python_verifier(mary, assassinat).
```

## 🧪 Exemples d'Utilisation

### 🔍 Cas d'Assassinat
**Suspect**: Mary  
**Crime**: Assassinat  
**Résultat**: ✅ Coupable  
**Preuves**: Motif, Présence sur lieux, Empreintes sur arme

### 💳 Cas d'Escroquerie  
**Suspect**: Alice  
**Crime**: Escroquerie  
**Résultat**: ✅ Coupable  
**Preuves**: Motif, Transaction bancaire

### ❌ Cas de Non-Culpabilité
**Suspect**: Bruno  
**Crime**: Assassinat  
**Résultat**: ❌ Non coupable  
**Preuves**: Aucune preuve trouvée

### 🎯 Démonstration Complète
Cliquez sur **"Lancer Démo"** pour exécuter tous les tests automatiquement :
- Mary + Assassinat = Coupable
- Bruno + Assassinat = Non coupable  
- Alice + Escroquerie = Coupable
- John + Vol = Coupable

## 📁 Structure des Fichiers

```
enquete_policiere/
├── enquete_prolog_tkinter.pl    # Moteur Prolog principal
├── interface_tkinter_prolog.py  # Interface graphique Python
├── database.py                  # Base de données (version Python alternative)
├── rules.py                     # Règles métier (version Python alternative)
├── gui_app.py                   # Interface Python standalone
└── test.py                      # Tests unitaires
```

## 🎓 Concepts Prolog Expliqués

### 🔍 Unification
Prolog trouve automatiquement les valeurs qui satisfont les contraintes :
```prolog
% Trouve tous les coupables d'assassinat
?- findall(S, is_guilty(S, assassinat), Coupables).
Coupables = [mary].
```

### ⚡ Backtracking
Prolog explore automatiquement toutes les possibilités :
```prolog
% Est-ce que Alice est coupable d'un crime ?
?- is_guilty(alice, Crime).
Crime = escroquerie.
```

### 🧠 Programmation Déclarative
On décrit **CE QU'ON VEUT** plutôt que **COMMENT LE FAIRE** :
```prolog
% Déclaratif : "Un suspect est coupable d'escroquerie s'il a un motif OU une transaction suspecte"
is_guilty(S, escroquerie) :- has_motive(S, escroquerie); has_bank_transaction(S, escroquerie).
```

## 💡 Points Forts du Projet

### ✅ Avantages de l'Approche Prolog
- **Logique pure** : Code concis et expressif
- **Inférence automatique** : Pas besoin de boucles ou conditions complexes
- **Extensibilité** : Ajout facile de nouvelles règles
- **Déclaratif** : Focus sur la logique métier plutôt que l'implémentation

### 🎯 Applications Réelles
Ce projet démontre comment Prolog peut être utilisé pour :
- Systèmes experts de diagnostic
- Moteurs de règles métier
- Analyse de preuves et d'évidences
- Systèmes de recommandation basés sur des règles

## 🔮 Extensions Possibles

### 🚀 Améliorations Futures
```prolog
% Ajout de nouvelles preuves
has_dna_evidence(Suspect, Crime).
has_confession(Suspect, Crime).

% Règles plus complexes
is_guilty(Suspect, Crime) :-
    strong_evidence(Suspect, Crime),
    not has_alibi(Suspect, Crime).

% Système de scoring
culpability_score(Suspect, Crime, Score) :-
    findall(1, has_evidence(Suspect, Crime), Evidences),
    length(Evidences, Score).
```

## 📚 Ressources Apprentissage Prolog

### 🎓 Pour Approfondir
- [SWI-Prolog Documentation](https://www.swi-prolog.org/)
- [Learn Prolog Now!](http://www.learnprolognow.org/)
- [Prolog Programming for Artificial Intelligence](https://www.amazon.com/Prolog-Programming-Artificial-Intelligence-International/dp/0321417461)

### 🔧 Outils Recommandés
- **SWI-Prolog** : Environnement de développement
- **Visual Studio Code** avec extension Prolog
- **PySwip** : Bibliothèque Python pour intégration Prolog

---

---

**💡 Conseil** : Ce projet montre la puissance de la programmation logique pour les systèmes experts. Prolog excelle dans les domaines où la logique et les règles métier sont complexes !