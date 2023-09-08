# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 14:37:34 2023

@author: CYTech Student
"""

import sys
import os
import subprocess
import csv 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re


# Variable racine
racine = r"h:/SZZUnleashed/"
vm_path = r"C:/Users/CYTech Student/Documents/Pharo/vms/100-x64/Pharo.exe"
Pharo_path = r"C:/Users/CYTech Student/Documents/Pharo/images/m10_szz/m10_szz.image"
local_root = r"H:/SZZUnleashed"
command_pharo_ro = f"SZZImporter findFilesChangedByBugfixesFrom: '{local_root}/sortie/results/DOSSIER_NAME/annotations.json' to: 'YOUR_CSV_VARIABLE_HERE'"






# Chemin du fichier Projects.csv
projects_csv_path = rf'{local_root}\entree\Projects.csv'

# Récupération du token GitHub à partir des variables d'environnement
github_token = os.environ.get("GITHUB_TOKEN")

if github_token is None:
    print("GITHUB_TOKEN is not set in the environment", file=sys.stderr)
    raise SystemExit(1)
else:
    print("GITHUB_TOKEN =", github_token)

# Commande Docker avec la variable racine
docker_command = f"docker run -e GITHUB_TOKEN={github_token} -v {racine}entree:/input -v {racine}sortie:/output szz"

# Exécution de la commande Docker avec affichage en temps réel
process = subprocess.Popen(docker_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# Lecture et affichage de la sortie en temps réel
for line in process.stdout:
    print(line, end='')

# Attente de la fin du processus
process.wait()

# Affichage du code de retour du processus
print("Return code:", process.returncode)


# Lecture du fichier Projects.csv pour obtenir github_repo
with open(projects_csv_path, newline="") as csvfile:
    for row in csv.reader(csvfile):
        if len(row) >= 2:
            url, Commit = row
            url_parts = url.split('/')
            if len(url_parts) >= 5:
                github_owner, github_repo = url_parts[3:5]
                print(f"URL: {url}, Commit: {Commit}")
                print(f"GitHub Owner: {github_owner}, GitHub Repo: {github_repo}")
                
                
                result_root_pharo = f"{local_root}/sortie/results/{github_owner}__{github_repo}"
                correlation_output_file =  os.path.join(result_root_pharo, "correlation.csv")
                if os.path.exists(correlation_output_file):
                    print("skiping correlation")
                else: 
                    # Construction du chemin du fichier CSV basé sur github_repo
                #csv_path = rf'{result_root}\modele_{github_repo}.csv'
                

                # Chemin d'accès du dossier de sortie
                #output_folder = "{local_root}/sortie/results/{github_owner}__{github_repo}"

                # Création du chemin csv_path avec os.path.join
                    csv_filename = f"modele_{github_repo}.csv"
                    csv_path = f"{result_root_pharo}/{csv_filename}"

                    print("CSV Path:", csv_path)

                
                # Remplacement du chemin du fichier CSV dans la commande
                    command_pharo = command_pharo_ro.replace('YOUR_CSV_VARIABLE_HERE', csv_path).replace('DOSSIER_NAME', f"{github_owner}__{github_repo}")

                # Création de la commande complète
                    command = fr'"{vm_path}" --headless "{Pharo_path}" eval "{command_pharo}"'

                # Exécution de la commande dans le terminal Windows ou PowerShell
                    print("modèle Pharo en cours...")
                    print("exécution de la commande pharo suivante",command)
                    subprocess.run(command, shell=True)
        #     else:
        #         print("Invalid URL format:", url)
        # else:
        #     print("Invalid row format:", row)
            
# with open(projects_csv_path, newline="") as csvfile:
#     for row in csv.reader(csvfile):
#         if len(row) >= 2:
#             url, Commit = row
#             url_parts = url.split('/')
#             if len(url_parts) >= 5:
#                 github_owner, github_repo = url_parts[3:5]
#                 print(f"URL: {url}, Commit: {Commit}")
#                 print(f"GitHub Owner: {github_owner}, GitHub Repo: {github_repo}")          
             
                
                 
                # Variable pour le chemin du fichier CSV
                #csv_path = rf'{local_root}/sortie/results/{github_owner}__{github_repo}/modele_{github_repo}.csv'
                
                # Vérifier si le fichier csv_path existe
                #if  os.path.isfile(csv_path):
                #    print(f"Le fichier {csv_path} n'existe pas.")
                #    continue  # Passer au traitement du fichier suivant
                
                    #Essayer d'ouvrir le fichier csv_path
                    try:
                        modele = pd.DataFrame(pd.read_csv(csv_path))
                    except FileNotFoundError:
                        print(f"Le fichier {csv_path} n'existe pas.")
                        continue  # Passer au traitement du fichier suivant
    
            
                    #modele = pd.DataFrame(pd.read_csv("H:\modele_darkreader.csv"))
                    #modele = pd.DataFrame(pd.read_csv(csv_path))
            
                    modele['Files'] = modele['Files'].str.replace('#', '')
                    files_list = modele['Files'].to_list()
                    commit_list = modele['Commit ID'].to_list()
                    
                    # Concaténer tous les éléments en une seule chaîne
                    all_files_text = ' '.join(files_list)
                    
                    # Utiliser une expression régulière pour extraire les noms de fichiers
                    file_names = re.findall(r"'(.*?)'", all_files_text)
                    
                    # Utiliser un ensemble pour stocker les noms de fichiers uniques
                    unique_file_names = set(file_names)
                    
                    # Convertir l'ensemble en liste pour obtenir les noms de fichiers uniques
                    final_file_names = list(unique_file_names)
                    
                    print(final_file_names)
                    
                    print(commit_list)
                    
                    occurrences = [file_names.count(file) for file in final_file_names]
                    
                    print(occurrences)
                    z = 0
                    for y in range(len(occurrences)):
                        z += occurrences[y]
                    print(z)
                    
                    
                    file_paths_with_h = [f"{local_root}/sortie/git/{github_repo}/" + file_name for file_name in final_file_names] ### à modifier pour que ça puisse marcher pour n'import quel dépôt 
            
                    # Créer un DataFrame avec les noms de fichiers et leurs occurrences
                    data = pd.DataFrame({"File": final_file_names, "Occurrences": occurrences, "File_Path": file_paths_with_h})
            
                    # Ajouter une colonne pour la position de chaque fichier dans final_file_names
                    data["Position"] = data["File"].apply(lambda x: final_file_names.index(x))
            
            
            
            
            
                    # Fonction pour compter les lignes de code dans un fichier
                    def count_lines(file_path):
                        try:
                            with open(file_path, "r", encoding="utf-8") as file:
                                lines = file.readlines()
                                return len(lines)
                        except FileNotFoundError:
                            return None
                    
                    # Ajouter une colonne pour le nombre de lignes de code
                    data["Lines of Code"] = data["File_Path"].apply(lambda x: count_lines(x))
            
                    print(data)
                
                    print(file_paths_with_h)
                    
                    correlation_matrix = data[["Occurrences", "Lines of Code"]].corr() #### correlation de Pearson
                    
                    print(correlation_matrix)
            
                    # Accéder à la valeur de corrélation entre "Occurrences" et "Lines of Code"
                    correlation_value = correlation_matrix.loc["Occurrences", "Lines of Code"]
                    
                    print("Correlation between Occurrences and Lines of Code:", correlation_value)
                    
                            # Chemin d'accès du dossier de sortie
                    #output_folder = "{local_root}/sortie/results/{github_owner}__{github_repo}"
                    
                    # Chargement des données du fichier Projects.csv et création de la liste projects_data
                    projects_data = []
                    
            
                    projects_data.append({"url": url, "Commit": Commit, "github_owner": github_owner, "github_repo": github_repo})
                                
                    
                    # Créer une liste pour stocker les données mises à jour
                    updated_data = []
                    
                    # Calculer la corrélation et ajouter le nom du github_repo et la corrélation
                    for project in projects_data:
                        github_repo_name = project["github_repo"]
                        project["correlation"] = correlation_value
                        
                        updated_data.append({"nom": github_repo_name, "url": project["url"], "Commit": project["Commit"], "correlation": correlation_value})
                    
                    # Créer un DataFrame à partir des données mises à jour
                    updated_df = pd.DataFrame(updated_data)
                    
                    # Créer le fichier correlation.csv dans le dossier de sortie
                    output_file = os.path.join(result_root_pharo, "correlation.csv")
                    updated_df.to_csv(output_file, index=False)
                    
                    print("Fichier correlation.csv créé avec succès dans le dossier de sortie.")
            else:
                print("Invalid URL format:", url)
        else:
            print("Invalid row format:", row)
