import tkinter as tk
from tkinter import ttk
from datetime import datetime

from pymodbus.client import ModbusTcpClient


# Parametres Modbus


periode_lecture = 500

client = ModbusTcpClient("172.20.10.3", port=5020)


# Correspondance des couleurs


noms_couleurs = { 0: "Aucune", 1: "Rouge", 2: "Vert",
    3: "Jaune", 4: "Bleu"}

couleurs_affichage = { 0: "#B0B0B0", 1: "#D62828",
2: "#2A9D4B",3: "#E3B505", 4: "#246BCE"}


# Creation de la fenetre


fenetre = tk.Tk()

fenetre.title("Interface avec modbus")
fenetre.geometry("550x500")
fenetre.resizable(False, False)

style = ttk.Style()

style.configure("SousTitre.TLabel", font=("Arial", 12, "bold"))

style.configure("Valeur.TLabel", font=("Arial", 12))



# Zone de connexion

cadre_connexion = ttk.LabelFrame(fenetre, text="Communication")

cadre_connexion.pack(fill="x", padx=25, pady=10)


ligne_connexion = ttk.Frame(cadre_connexion)

ligne_connexion.pack(fill="x", padx= 15, pady =12)


voyant_connexion = tk.Canvas(ligne_connexion, width = 24, height=24)

voyant_connexion.pack(side="left", padx=(0, 10))



cercle_connexion = voyant_connexion.create_oval(3, 3, 21, 21, fill="red")


connexion = ttk.Label(ligne_connexion, text="Connexion : Deconnecte",
style="SousTitre.TLabel")

connexion.pack(side="left")



# Zone des informations cube

cadre_cube = ttk.LabelFrame(fenetre, text="informations du cube")

cadre_cube.pack( fill="both", expand=True, padx=25, pady=10)


presence = ttk.Label(cadre_cube, text="Piece presente : Non", style="Valeur.TLabel")

presence.grid(row=0, column=0, columnspan=2, sticky="w",
padx=20, pady=(18, 10))


etiquette_couleur = ttk.Label(cadre_cube, text="Couleur :",
style="Valeur.TLabel")


etiquette_couleur.grid( row=1, column=0, sticky="w",padx=(20,5), pady=10)



couleur = ttk.Label(cadre_cube, text="---",style="Valeur.TLabel")

couleur.grid(row=1, column=1, sticky="w", padx=5, pady=10)


indicateur_couleur = tk.Canvas(cadre_cube, width=34, height=34,
highlightthickness=1, highlightbackground="#808080" )


indicateur_couleur.grid(row=1, column=2, padx=15,pady=10)

rectangle_couleur = indicateur_couleur.create_rectangle(4,4, 30, 30,
    fill="#B0B0B0", outline="")


position_x = ttk.Label(cadre_cube, text="Position X : ---",
style="Valeur.TLabel")

position_x.grid(row=2, column=0, columnspan=2, sticky="w",padx=20,pady=10)


position_y = ttk.Label(cadre_cube, text="Position Y : ---", style="Valeur.TLabel")

position_y.grid(row=3,column=0, columnspan=2, sticky="w", padx=20,pady=10)


orientation = ttk.Label(cadre_cube, text="Orientation : ---", style="Valeur.TLabel")

orientation.grid(row=4, column=0, columnspan=2, sticky="w", padx=20, pady=10)



# Derniere mise a jour


cadre_mise_a_jour = ttk.Frame(fenetre)

cadre_mise_a_jour.pack(fill="x", padx=25,pady=(5, 15))

derniere_mise_a_jour = ttk.Label(cadre_mise_a_jour, 
text="Derniere mise a jour : ---", font=("Arial", 10))

derniere_mise_a_jour.pack(side="left")



# Fonctions d'affichage


def afficher_connexion(connecte):
    if connecte:
        connexion.config(text="Connexion : Connecte")
        voyant_connexion.itemconfig( cercle_connexion, fill="#2A9D4B")
        
    else:
        connexion.config(text="Connexion : Deconnecte")
        voyant_connexion.itemconfig( cercle_connexion , fill="#D62828")


def vider_informations():
    presence.config(text="Piece presente : Non")
    couleur.config(text="---")

    indicateur_couleur.itemconfig( rectangle_couleur,fill=couleurs_affichage[0])

    position_x.config(text="Position x : ---")
    position_y.config(text="Position y : ---")
    orientation.config(text="orientation : ---")


def afficher_erreur():
    presence.config(text="Piece presente : Erreur")
    
    couleur.config(text="Erreur")
    indicateur_couleur.itemconfig(rectangle_couleur,fill="#B0B0B0")

    position_x.config(text="Position X : Erreur")
    position_y.config(text="Position Y : Erreur")
    orientation.config(text="Orientation : Erreur")



# Lecture Modbus

def lire_modbus():
    try:
        if not client.connected: 
             client.connect()

        if not client.connected:
        
            afficher_connexion(False)
            vider_informations()

            fenetre.after( periode_lecture, lire_modbus)
            
            return

        afficher_connexion(True)

        reponse_coil = client.read_coils(address=0 ,count=1)

        if reponse_coil.isError():
            afficher_erreur()

        else:
            piece_presente = reponse_coil.bits[0]

            if piece_presente:
                presence.config( text="Piece presente : Oui")

                reponse_registres = (client.read_holding_registers(address=0,
                        count=4))

                if reponse_registres.isError():
                    afficher_erreur()

                else:
                    x = reponse_registres.registers[0]
                    y = reponse_registres.registers[1]
                    angle = reponse_registres.registers[2]
                    code_couleur = reponse_registres.registers[3]

                    nom_couleur = noms_couleurs.get(code_couleur,"Inconnue")

                    couleur.config( text=nom_couleur)

                    indicateur_couleur.itemconfig(rectangle_couleur,
                        fill=couleurs_affichage.get(code_couleur,"#B0B0B0"))

                    position_x.config(text=f"Position X : {x} px")
                    position_y.config(text=f"Position Y : {y} px")
                    orientation.config(text=f"Orientation : {angle} degres")

            else:
                vider_informations()

        heure = datetime.now().strftime("%H:%M:%S")

        derniere_mise_a_jour.config(text=f"Derniere mise a jour : {heure}")

    except Exception as erreur:
        afficher_connexion(False)
        afficher_erreur()
        client.close()

        print("Erreur Modbus :", erreur)

    fenetre.after(periode_lecture , lire_modbus)


# Fermeture propre


def fermer_interface():
    client.close()
    fenetre.destroy()


fenetre.protocol("WM_DELETE_WINDOW", fermer_interface)


# Demarrage

lire_modbus()

fenetre.mainloop()
