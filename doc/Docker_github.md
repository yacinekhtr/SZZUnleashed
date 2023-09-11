# new docker command for Github repositories:

```bash

```

```powershell


```
```How to Run SZZUnleashed Algorithm with automatisation commands and github repositories ```

docker build -t szz_github -f Dockerfile_github .


### Executer ensuite le fichier pipeline.py que pour les dépôts githubs.

docker run -e GITHUB_TOKEN=$env:GITHUB_TOKEN -v  h:/SZZUnleashed/entree:/input  -v  h:/SZZUnleashed/sortie:/output 
szz  

### commande qui exécute le processus d'automatisation des commandes sur le powershell une fois que l'utilisateur a entré son GITHUB_TOKEN dans son environnement.



### Obtention de l'image Moose afin d'effectuer les tests

aller télécharger les fichiers du projet SZZ_results_analyser sur mon github dont le lien est le suivant: 

https://github.com/yacinekhtr/SZZ_results_analyser

Lancer ensuite Moose et aller sur "Iceberg" qui se trouve dans le label Browse puis ajouter le répertoire précédemment télécharger "SZZ_results_analyser" à l'aide du bouton "ADD"

puis clique droit sur le répertoire et cliquer sur "packages" et ajouter "SZZ_analysis" à l'aide du bouton "ADD package". 


### Commande de création d'un environnement virtuel pour le projet python à exécuter dans le powershell

python -m venv my_env

.\my_venv\Scripts\Activate.ps1 

pip install numpy pandas

python .\driver\pipeline.py

