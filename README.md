# OSPS
## 1.A Quel module utilisez-vous pour manipuler un segment mémoire partagé en Python 3 ?
Veillez à utiliser le module le plus « simple » possible tout en choisissant un module « officiel/maintenu/à jour »

Le module shared_memory du package multiprocessing est idéal pour manipuler des segments de mémoire partagée en Python 3. Il est :
Simple : facile à utiliser pour créer et gérer des segments de mémoire partagée.
Officiel : fait partie de la bibliothèque standard Python.
Maintenu et à jour : inclus dans Python depuis la version 3.8 et régulièrement mis à jour.


### PROBLÈMES AVEC LA VERSION FOURNIE PAR "multiptocessing::shared_memory" :
#### -> Qui gère les droits ?
(A remplir)
#### -> Pourquoi ipcs ne "voit" pas le segment ?
Avec multiprocessing.shared_memory, le segment de mémoire est créé et accessible uniquement aux processus Python qui connaissent le nom spécifié (ici '012345'). Cependant, il ne sera pas visible via ipcs, car multiprocessing.shared_memory utilise une méthode de gestion de mémoire partagée propre à Python, qui est souvent basée sur les fonctionnalités de mémoire partagée de POSIX, mais qui n'utilise pas exactement la même interface que celle des segments de mémoire partagée système (les segments de mémoire POSIX visibles avec ipcs)

## 2.b) Quel serveur doit s’arrêter en premier pour éviter les zombies ? Qu’est-ce qu’un zombie au sens informatique ?
Pour éviter la création de processus zombies, c’est le processus enfant (serveur secondaire) qui devrait s’arrêter en premier. Dans le contexte d'un parent et d'un enfant :

Un zombie est un processus qui a terminé son exécution mais dont le parent n’a pas encore récupéré le code de retour. Il reste alors dans la table des processus avec un état « zombie ».
Un processus zombie occupe des ressources et de la place dans la table des processus jusqu'à ce que son parent appelle wait() pour récupérer son code de sortie.

