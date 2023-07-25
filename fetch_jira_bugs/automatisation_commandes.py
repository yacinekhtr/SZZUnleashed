# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 21:07:53 2023

@author: CYTech Student
"""
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
import csv  
import os
import subprocess

parent_folder = '/root/projet_tests'

with open('/input/Projects.csv', newline="") as csvfile:
    
    # Parcourir chaque ligne du DataFrame
    #for index, row in Projet.iterrows():
    for row in csv.reader(csvfile):
        # Each row is a list of values representing the columns
        url, Commit = row
        print(f"URL: {url}, Commit: {Commit}")
        # Extraire le premier mot de l'URL GitHub
        github_owner, github_repo = url.split('/')[3:5]  # Assumant que l'URL suit le format "https://github.com/premier-mot/..."
        # Chemin complet du dossier à créer
        folder_path = os.path.join(parent_folder, '__'.join([github_owner,github_repo]))
        folder_exists = os.path.exists(folder_path)
        
        if folder_exists : 
            print("Le folder " + folder_path + " existe deja")
        else :
            # Créer un répertoire avec le chemin complet
            os.makedirs(folder_path, exist_ok=True)
                
            #  afficher le nom du dossier créé
            print(f"Dossier cree : {folder_path}")    

            ###Automatisation des commandes présentes dans Docker.md
         
            os.chdir(folder_path)
                                                                                         
            url_git = f"https://github.com/{github_owner}/{github_repo}.git"                               
            subprocess.run(["git", "clone", url_git])
                                                                                   
            subprocess.run(["python3", "/root/fetch_jira_bugs/fetch_github.py", github_owner, github_repo])
                                                                                  
            subprocess.run(["python3", "/root/fetch_jira_bugs/git_log_to_array.py", "--repo-path", github_repo, "--from-commit", Commit])
                                 
            subprocess.run(["python3", "/root/fetch_jira_bugs/find_bug_fixes.py", "--gitlog", "./gitlog.json", "--issue-list", "./fetch_issues", "--gitlog-pattern", '"[Cc]loses #{nbr}\D|#{nbr}\D|[Ff]ixes #{nbr}\D"'])
        
            subprocess.run(["java", "-jar", "/root/szz/build/libs/szz_find_bug_introducers-0.1.jar", "-i", "./issue_list.json", "-r", github_repo])

            project_output = os.path.join("/output/", '__'.join([github_owner,github_repo]))
            os.makedirs(project_output, exist_ok=True)
            subprocess.run(["cp", "./results/annotations.json", project_output])
            subprocess.run(["cp", "./results/commits.json", project_output])
            subprocess.run(["cp", "./results/fix_and_introducers_pairs.json", project_output])
