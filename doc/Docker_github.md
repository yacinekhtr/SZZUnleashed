# How to Run SZZUnleashed Algorithm using github repositories and bug trackers

Build the docker image that works with GitHub:

```bash
docker build -t szz_github -f Dockerfile_github .
```

Run the sample automation script `pipeline.py` that expects a list of projects in `entree/Projects.csv`. This example will calculate correlation of the bugs with the size of the files. It uses a Pharo image in part of the steps. You must have a variable GITHUB_TOKEN defined in your environment, because it accesses the GitHub API. Get a token following [these instructions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens). 

```bash
docker run -e GITHUB_TOKEN=$env:GITHUB_TOKEN -v h:/SZZUnleashed/entree:/input -v h:/SZZUnleashed/sortie:/output szz  
```

### How to get the Pharo/Moose image used in the pipeline


aller télécharger les fichiers du projet SZZ_results_analyser sur mon github dont le lien est le suivant: 

https://github.com/yacinekhtr/SZZ_results_analyser

Lancer ensuite Moose et aller sur "Iceberg" qui se trouve dans le label Browse puis ajouter le répertoire précédemment télécharger "SZZ_results_analyser" à l'aide du bouton "ADD"

puis clique droit sur le répertoire et cliquer sur "packages" et ajouter "SZZ_analysis" à l'aide du bouton "ADD package". 


### Commande de création d'un environnement virtuel pour le projet python à exécuter dans le powershell

python -m venv my_env

.\my_venv\Scripts\Activate.ps1 

pip install numpy pandas

python .\driver\pipeline.py

