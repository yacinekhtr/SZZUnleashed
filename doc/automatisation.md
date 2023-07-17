pour run le code dans le bash éxécuter la commande suivante : python automatisation_commande.py

Le code effectue les actions suivantes: 

Manipulation des données : La colonne 'URL ' du DataFrame Projet est extraite dans une liste url_list, et la colonne 'Commit ' est extraite dans une liste commit_list. Une opération de remplacement est effectuée sur la colonne 'URL ' pour supprimer les parties non nécessaires.

Définition de la fonction test() : Une fonction appelée test() est définie. Elle prend une liste url_list en argument.

Boucle principale : La boucle principale parcourt chaque ligne du DataFrame Projet à l'aide de iterrows(). Pour chaque ligne, la fonction test() est appelée avec des paramètres appropriés.

Création de dossiers : À l'intérieur de la fonction test(), un chemin de dossier est construit en utilisant les informations de l'URL GitHub. Un dossier est créé à l'aide de os.makedirs() si le dossier n'existe pas déjà.

Exécution des commandes Docker : Plusieurs commandes Docker sont exécutées à l'aide du module subprocess. Les commandes incluent la construction de l'image Docker, l'exécution d'un conteneur Docker avec des variables d'environnement, l'exécution de scripts Python à l'intérieur du conteneur, la copie de fichiers depuis le conteneur vers un emplacement local, etc.

Les commandes Docker sont exécutées pour chaque URL dans la liste url_list.