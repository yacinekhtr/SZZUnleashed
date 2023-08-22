# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 21:07:53 2023

@author: CYTech Student
"""


from dotenv import load_dotenv
import csv  
import os
import subprocess
import shutil
import sys 

parent_folder = '/root/projet_tests' ## changer en '/output/git'

root_git = '/output/git'

load_dotenv('token.env')
token = os.getenv('GITHUB_TOKEN')

if token is None:
    print("GITHUB_TOKEN is not set in the environment", file = sys.stderr)
    raise SystemExit(0)
else: 
    print("GITHUB_TOKEN=",token)
os.makedirs(root_git, exist_ok=True)


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
            print("current working directory is:", folder_path)                                                                             
            url_git = f"https://github.com/{github_owner}/{github_repo}.git"                               
            result = subprocess.run(["git", "clone", url_git])
            
            
            # Copier le contenu du dossier cloné directement dans root_git
            print("copiage du dépôt en cours...")
            shutil.copytree(os.path.join(folder_path,github_repo), os.path.join(root_git, github_repo))
            print("Le clonage du dépôt est fini")
            
            #clone_folder = '__'.join([github_owner, github_repo])
            #destination_path = os.path.join(root_git, clone_folder)
            #shutil.copytree(folder_path, root_git)
            
            print("fetch_github.py...")                                                                     
            result = subprocess.run(["python3", "/root/fetch_github_bugs/fetch_github.py", github_owner, github_repo])
            if result.returncode != 0:
                print("Error:", result.returncode)
                raise SystemExit(result.returncode)
            
            print("git_log_to_array.py...")                                                                    
            result = subprocess.run(["python3", "/root/fetch_github_bugs/git_log_to_array.py", "--repo-path", github_repo, "--from-commit", Commit])
            if result.returncode != 0:
                print("Error:", result.returncode)
                raise SystemExit(result.returncode)
            
            print("find_bug_fixes.py...")                    
            result = subprocess.run(["python3", "/root/fetch_github_bugs/find_bug_fixes.py", "--gitlog", "./gitlog.json", "--issue-list", "./fetch_issues", "--gitlog-pattern", '"[Cc]loses #{nbr}\D|#{nbr}\D|[Ff]ixes #{nbr}\D"'])
            if result.returncode != 0:
                print("Error:", result.returncode)
                raise SystemExit(result.returncode)
            
            print("szz_find_bug_introducers-0.1.jar...")
            result = subprocess.run(["java", "-jar", "/root/szz/build/libs/szz_find_bug_introducers-0.1.jar", "-i", "./issue_list.json", "-r", github_repo])
            if result.returncode != 0:
                print("Error:", result.returncode)
                raise SystemExit(result.returncode)

            clone_folder= '__'.join([github_owner,github_repo])
            project_output = os.path.join("/output/results", clone_folder )
            os.makedirs(project_output, exist_ok=True)
            print("le dossier results est crée:",project_output)
            
            result = subprocess.run(["cp", "./results/annotations.json", project_output])
            if result.returncode != 0:
                print("Error copying annotations.json:", result.returncode)
                raise SystemExit(result.returncode)
            
            result = subprocess.run(["cp", "./results/commits.json", project_output])
            if result.returncode != 0:
                print("Error copying commits.json:", result.returncode)
                raise SystemExit(result.returncode)
            
            result = subprocess.run(["cp", "./results/fix_and_introducers_pairs.json", project_output])
            if result.returncode != 0:
                print("Error copying fix_and_introducers_pairs.json:", result.returncode)
                raise SystemExit(result.returncode)
            #result = subprocess.run(["cp", folder_path , root_git])
