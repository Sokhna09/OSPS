# OSPS
##Contexte
Initialement, j'ai conçu ce projet en utilisant un code non orienté objet pour gérer le segment mémoire. Cependant, en avançant sur le projet, j'ai réalisé qu'il serait plus judicieux de le structurer en programmation orientée objet (POO) afin de rendre le code plus lisible et mieux organisé.
## Quel module utilisez-vous pour manipuler un segment mémoire partagé en Python 3 ?
Veillez à utiliser le module le plus « simple » possible tout en choisissant un module « officiel/maintenu/à jour »

Le module shared_memory du package multiprocessing est idéal pour manipuler des segments de mémoire partagée en Python 3. Il est :
Simple : facile à utiliser pour créer et gérer des segments de mémoire partagée.
Officiel : fait partie de la bibliothèque standard Python.
Maintenu et à jour : inclus dans Python depuis la version 3.8 et régulièrement mis à jour.


### PROBLÈMES AVEC LA VERSION FOURNIE PAR "multiptocessing::shared_memory" :

#### -> Pourquoi ipcs ne "voit" pas le segment ?
Avec multiprocessing.shared_memory, le segment de mémoire est créé et accessible uniquement aux processus Python qui connaissent le nom spécifié (ici '012345'). Cependant, il ne sera pas visible via ipcs, car multiprocessing.shared_memory utilise une méthode de gestion de mémoire partagée propre à Python, qui est souvent basée sur les fonctionnalités de mémoire partagée de POSIX, mais qui n'utilise pas exactement la même interface que celle des segments de mémoire partagée système (les segments de mémoire POSIX visibles avec ipcs)

##  Quel serveur doit s’arrêter en premier pour éviter les zombies ? Qu’est-ce qu’un zombie au sens informatique ?
Pour éviter la création de processus zombies, c’est le processus enfant (serveur secondaire) qui devrait s’arrêter en premier. Dans le contexte d'un parent et d'un enfant :

Un zombie est un processus qui a terminé son exécution mais dont le parent n’a pas encore récupéré le code de retour. Il reste alors dans la table des processus avec un état « zombie ».
Un processus zombie occupe des ressources et de la place dans la table des processus jusqu'à ce que son parent appelle wait() pour récupérer son code de sortie.

## Exécution du Segment Mémoire

Mémoire mise à jour
Voici un exemple de README pour ton projet, basé sur ce que tu as décrit :

Projet de Communication entre Worker et Dispatcher
Contexte
Initialement, j'ai conçu ce projet en utilisant un code non orienté objet pour gérer le segment mémoire. Cependant, en avançant sur le projet, j'ai réalisé qu'il serait plus judicieux de le structurer en programmation orientée objet (POO) afin de rendre le code plus lisible et mieux organisé.

Exécution du Segment Mémoire
Pour exécuter le segment mémoire, il suffit de lancer le fichier SharedMemory.py dans un terminal Linux : "python3 SharedMemory.py"


##Tentative d'Implémentation du Watchdog

Au départ, j'avais essayé d'implémenter un watchdog pour surveiller le dispatcher, qui communique à son tour avec le worker via des tubes. Cependant, cette approche a échoué à cause de conflits d'écriture sur les tubes. J'ai aussi tenté d'utiliser des signaux, mais cela n'a pas fonctionné non plus.

##Solution Retenue
J'ai finalement décidé d'utiliser une seule paire de tubes pour la communication entre le worker et le dispatcher, et des sockets pour la communication entre le client et le dispatcher. Cette architecture simplifie la communication et évite les conflits d'écriture.

## Exécution Finale
Pour exécuter le projet, il faut ouvrir deux terminaux en parallèle :

Dans le premier terminal, lancez le dispatcher :
"python3 Dispatcher.py"

Le dispatcher attendra une requête du client.

Dans le second terminal, lancez le client :
"python3 Client.py"

Cela établira la communication entre le client et le dispatcher.

## Limitations
Je n'ai pas pu implémenter le watchdog comme prévu en raison des difficultés rencontrées avec les tubes et les signaux.Si j'avais eu plus de temps, j'aurai essayé de l'implementer avec les sockets comme j'ai reussi à le faire avec le client
