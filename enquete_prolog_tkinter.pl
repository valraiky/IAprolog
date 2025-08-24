% enquete_prolog_tkinter.pl - Version compatible interface Tkinter

% Déclaration des prédicats discontinus
:- discontiguous has_motive/2.
:- discontiguous was_near_crime_scene/2.
:- discontiguous has_fingerprint_on_weapon/2.
:- discontiguous has_bank_transaction/2.
:- discontiguous owns_fake_identity/2.

% Types de crimes
crime_type(assassinat).
crime_type(vol).
crime_type(escroquerie).

% Suspects
suspect(john).
suspect(mary).
suspect(alice).
suspect(bruno).
suspect(sophie).

% Faits de l'enquête
has_motive(john, vol).
was_near_crime_scene(john, vol).
has_fingerprint_on_weapon(john, vol).

has_motive(mary, assassinat).
was_near_crime_scene(mary, assassinat).
has_fingerprint_on_weapon(mary, assassinat).

has_motive(alice, escroquerie).
has_bank_transaction(alice, escroquerie).

has_bank_transaction(bruno, escroquerie).
owns_fake_identity(sophie, escroquerie).

% Règles de culpabilité (inchangées)
is_guilty(Suspect, assassinat) :-
    has_motive(Suspect, assassinat),
    was_near_crime_scene(Suspect, assassinat),
    (has_fingerprint_on_weapon(Suspect, assassinat)
    ; eyewitness_identification(Suspect, assassinat)
    ).

is_guilty(Suspect, escroquerie) :-
    (has_motive(Suspect, escroquerie)
    ; has_bank_transaction(Suspect, escroquerie)
    ; owns_fake_identity(Suspect, escroquerie)
    ).

is_guilty(Suspect, vol) :-
    has_motive(Suspect, vol),
    was_near_crime_scene(Suspect, vol),
    has_fingerprint_on_weapon(Suspect, vol).

% =============================================
% NOUVELLES RÈGLES POUR INTERFACE TKINTER
% =============================================

% Règle pour vérifier la culpabilité et retourner un résultat simple
verifier_culpabilite(Suspect, Crime, Resultat) :-
    (is_guilty(Suspect, Crime) -> Resultat = 'coupable' ; Resultat = 'non_coupable').

% Règle pour obtenir les preuves sous forme de liste
obtenir_preuves(Suspect, Crime, PreuvesListe) :-
    findall(Preuve, (
        (has_motive(Suspect, Crime), Preuve = 'motif');
        (was_near_crime_scene(Suspect, Crime), Preuve = 'presence_lieux');
        (has_fingerprint_on_weapon(Suspect, Crime), Preuve = 'empreintes_arme');
        (has_bank_transaction(Suspect, Crime), Preuve = 'transaction_bancaire');
        (owns_fake_identity(Suspect, Crime), Preuve = 'fausse_identite');
        (eyewitness_identification(Suspect, Crime), Preuve = 'temoin_oculaire')
    ), PreuvesListe).

% Règle pour formater les preuves en texte
formater_preuves(Suspect, Crime, TextePreuves) :-
    obtenir_preuves(Suspect, Crime, PreuvesListe),
    (PreuvesListe = [] -> 
        format(atom(TextePreuves), 'Aucune preuve contre ~w pour ~w', [Suspect, Crime])
    ;
        atomic_list_concat(PreuvesListe, ', ', PreuvesStr),
        format(atom(TextePreuves), 'Preuves contre ~w pour ~w: ~w', [Suspect, Crime, PreuvesStr])
    ).

% Règle pour obtenir tous les coupables
obtenir_tous_coupables(CoupablesListe) :-
    findall((Suspect, Crime), is_guilty(Suspect, Crime), CoupablesListe).

% Règle principale pour l'interface
% Usage: interface_verifier(mary, assassinat, Resultat, Preuves)
interface_verifier(Suspect, Crime, Resultat, Preuves) :-
    verifier_culpabilite(Suspect, Crime, Resultat),
    formater_preuves(Suspect, Crime, Preuves).

% Règle pour exécuter la démo et retourner les résultats
executer_demo(ResultatsDemo) :-
    % Mary assassinat
    verifier_culpabilite(mary, assassinat, Resultat1),
    formater_preuves(mary, assassinat, Preuves1),
    
    % Bruno assassinat  
    verifier_culpabilite(bruno, assassinat, Resultat2),
    formater_preuves(bruno, assassinat, Preuves2),
    
    % Alice escroquerie
    verifier_culpabilite(alice, escroquerie, Resultat3),
    formater_preuves(alice, escroquerie, Preuves3),
    
    % Formatage des résultats
    format(atom(ResultatsDemo), 
           'Mary assassinat: ~w (~w)~nBruno assassinat: ~w (~w)~nAlice escroquerie: ~w (~w)',
           [Resultat1, Preuves1, Resultat2, Preuves2, Resultat3, Preuves3]).

% Règle pour éviter l'erreur
eyewitness_identification(_, _) :- fail.

% =============================================
% POINTS D'ENTRÉE POUR PYTHON
% =============================================

% Point d'entrée pour vérifier la culpabilité
% Usage: python_verifier(mary, assassinat)
python_verifier(Suspect, Crime) :-
    interface_verifier(Suspect, Crime, Resultat, Preuves),
    format('RESULTAT:~w~nPREUVES:~w', [Resultat, Preuves]).

% Point d'entrée pour la démo
% Usage: python_demo
python_demo :-
    executer_demo(Resultats),
    format('DEMO_RESULTATS:~w', [Resultats]).

% Point d'entrée pour les preuves seulement
% Usage: python_preuves(mary, assassinat)
python_preuves(Suspect, Crime) :-
    formater_preuves(Suspect, Crime, Preuves),
    format('PREUVES:~w', [Preuves]).