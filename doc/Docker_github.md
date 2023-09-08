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