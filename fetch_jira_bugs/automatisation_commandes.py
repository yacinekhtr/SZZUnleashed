# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 21:07:53 2023

@author: CYTech Student
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv  
import os
import subprocess

Projet = pd.read_csv('h:\Downloads\Projects.csv', header = 0)
K = Projet.copy()
K['URL '].replace('https://github.com/', ' ').replace('/', ' ')
Projet.head()

parent_folder = 'D:\projet_tests'
url_list = Projet['URL '].tolist()
commit_list = Projet['Commit '].tolist()

def test(url_list):
    
# Parcourir chaque ligne du DataFrame
    for index, row in Projet.iterrows():
# Extraire le premier mot de l'URL GitHub
        url = row['URL ']
        first_word = url.split('/')[3:5]  # Assumant que l'URL suit le format "https://github.com/premier-mot/..."
        last_words_list = [url.split('/')[-1] for url in url_list]
        result = [[word, word] for word in last_words_list]
    # Chemin complet du dossier à créer
        folder_path = os.path.join(parent_folder, '_'.join(first_word))
        print(folder_path)
        folder_exists = os.path.exists(folder_path)
        print(folder_exists)
        i = 0
    #for i in range(len(url_list)):
        while  i <= len(url_list):
        
            if folder_exists == True:
                print("Le fichier existe déja")
                url_list.pop(i)
                
                #i+=1
                #url_list[i]
                test(url_list)
            elif folder_exists == False:
                folder_path = os.path.join(parent_folder, result[i][0] + "_" + result[i][1])
        
                # # Créer un répertoire avec le chemin complet
                os.makedirs(folder_path, exist_ok=True)
                
                # #  afficher le nom du dossier créé
                print(f"Dossier créé : {folder_path}")
                
                
                ###Automatisation des commandes présentes dans Docker.md
                
                commande_1 = "docker build -t szz ."
                subprocess.run(["bash", "-c", commande_1], shell=True)
                commande_2 = "docker run -it -e GITHUB_TOKEN=$GITHUB_TOKEN --name szz_con szz ash"
                subprocess.run(["bash", "-c", commande_2], shell=True)
                commande_3 = "https://github.com/"+ result[i][0]+"/" + result[i][1] +".git"
                subprocess.run(["bash", "-c", commande_3], shell=True)
                commande_4 = "cd /root/fetch_jira_bugs"
                subprocess.run(["bash", "-c", commande_4], shell=True)
                commande_5 = "python3 fetch_github.py"+ " " + result[i][0]+ " "+ result[i][1]
                subprocess.run(["bash", "-c", commande_5], shell=True)
                commande_6 = "python3 git_log_to_array.py --repo-path"+ " "+ "../"+result[i][1]+ " "+ "--from-commit"+ " "+ commit_list[i]
                subprocess.run(["bash", "-c", commande_6], shell=True)
                commande_7 = 'python3 find_bug_fixes.py --gitlog ./gitlog.json --issue-list ./issues --gitlog-pattern "[Cc]loses #{nbr}\D|#{nbr}\D|[Ff]ixes #{nbr}\D"'
                subprocess.run(["bash", "-c", commande_7], shell=True)
                commande_8 = "cd /root/szz"
                subprocess.run(["bash", "-c", commande_8], shell=True)
                commande_9 = "java -jar ./build/libs/szz_find_bug_introducers-0.1.jar -i ../fetch_jira_bugs/issue_list.json -r" + " "+ "../"+ result[i][1]
                subprocess.run(["bash", "-c", commande_9], shell=True)
                commande_10 = 'docker cp -a szz_con:/root/szz/results "D:/Données"'
                subprocess.run(["bash", "-c", commande_10], shell=True)