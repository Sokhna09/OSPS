import os
import sys
from multiprocessing import shared_memory

# Création du segment mémoire partagée + accès à son "nom" (utilisé pour générer une clef)
# (le nom peut être généré automatiquement, mais l'avantage de le fixer est que les n processus
# qui accèdent au même segment ont "juste besoin de connaitre ce nom pour y accéder")
#

shm_segment1 = shared_memory.SharedMemory(name='012345', create=True, size=10)
print('Nom du segment mémoire partagée :', shm_segment1.name)

# Accès + écriture de données via le premier accès au segment mémoire partagée
print('Taille du segment mémoire partagée en octets via premier accès :', len(shm_segment1.buf))
shm_segment1.buf[:] = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])

# Creation des tubes pour la synchronisation
dwtube1_r, dwtube1_w = os.pipe()
wdtube1_r, wdtube1_w = os.pipe()

newpid = os.fork()
if newpid < 0:
    print("fork() impossible")
    os.abort()
if newpid == 0:
    print("je suis le fils")
    # Simuler l'attachement d'un second processus au même segment mémoire partagée
    # en utilisant le même nom que précédemment :
    shm_segment2 = shared_memory.SharedMemory(shm_segment1.name)
    #lecture et écriture dans les tubes
    os.close(dwtube1_w)
    os.close(wdtube1_r)
    message = os.read(dwtube1_r, 1024).decode()
    print(f"Fils : j'ai lu '{message}'")

    os.write(wdtube1_w, b"pong")
    # Accès + écriture de données via le second accès au MÊME segment mémoire partagée
    # print('Taille du segment mémoire partagée en octets via second accès :', len(shm_segment2.buf))
    # print('Contenu du segment mémoire partagée en octets via second accès :', bytes(shm_segment2.buf))
    # os.execlp("ipcs", "ipcs", "-m");
    os.close(dwtube1_r)
    os.close(wdtube1_w)
    shm_segment2.close()
else:
    #os.wait()
    print('je suis le père')
    os.close(dwtube1_r)
    os.close(wdtube1_w)
    # lecture et écriture dans les tubes
    os.write(dwtube1_w, b"ping")
    message = os.read(wdtube1_r, 1024).decode()
    print(f"Pere:j'ai lu'{message}' ")

    os.close(dwtube1_w)
    os.close(wdtube1_r)


shm_segment1.close()
shm_segment1.unlink()

# 1.A Quel module utilisez-vous pour manipuler un segment mémoire partagé en Python 3 ?
# Veillez à utiliser le module le plus « simple » possible tout en choisissant un module « officiel/maintenu/à jour »

# Le module shared_memory du package multiprocessing est idéal pour manipuler des segments de mémoire partagée en Python 3. Il est :
# Simple : facile à utiliser pour créer et gérer des segments de mémoire partagée.
# Officiel : fait partie de la bibliothèque standard Python.
# Maintenu et à jour : inclus dans Python depuis la version 3.8 et régulièrement mis à jour.


# Avec multiprocessing.shared_memory, le segment de mémoire est créé et accessible uniquement
# aux processus Python qui connaissent le nom spécifié (ici '012345'). Cependant, il ne sera pas
# visible via ipcs, car multiprocessing.shared_memory utilise une méthode de gestion de mémoire
# partagée propre à Python, qui est souvent basée sur les fonctionnalités de mémoire partagée de
# POSIX, mais qui n'utilise pas exactement la même interface que celle des segments de mémoire
# partagée système (les segments de mémoire POSIX visibles avec ipcs)

# PROBLÈMES AVEC LA VERSION FOURNIE PAR "multiptocessing::shared_memory" :
# -> Qui gère les droits ?
# -> Pourquoi ipcs ne "voit" pas le segment ?
