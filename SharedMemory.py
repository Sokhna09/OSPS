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
max_exchanges = 5

newpid = os.fork()

if newpid < 0:
    print("fork() impossible")
    os.abort()

if newpid == 0:
    print("je suis le fils")
    # Simuler l'attachement d'un second processus au même segment mémoire partagée en utilisant le même nom que précédemment
    # ainsi que lecture et affichage des données dans la mémoire partagée
    shm_segment2 = shared_memory.SharedMemory(shm_segment1.name)
    data = bytes(shm_segment2.buf[:])
    print(f"Fils : contenu de la mémoire partagée : {data} (valeurs ASCII : {list(data)})")
    #lecture et écriture dans les tubes
    os.close(dwtube1_w)
    os.close(wdtube1_r)
    exchanges = 0

    while True :
        message = os.read(dwtube1_r, 1024).decode()
        if message == "stop":
            print("Fils : arrêté après le message stop")
            break
        print(f"Fils : j'ai lu '{message}'")
        os.write(wdtube1_w, b"pong")
        exchanges += 1
        #if exchanges >= max_exchanges :
        #    os.write(wdtube1_w, b"stop")
        #    break
    # Accès + écriture de données via le second accès au MÊME segment mémoire partagée
    # print('Taille du segment mémoire partagée en octets via second accès :', len(shm_segment2.buf))
    # print('Contenu du segment mémoire partagée en octets via second accès :', bytes(shm_segment2.buf))
    # os.execlp("ipcs", "ipcs", "-m");
    os.close(dwtube1_r)
    os.close(wdtube1_w)
    shm_segment2.close()

else:
    print('je suis le père')
    os.close(dwtube1_r)
    os.close(wdtube1_w)
    exchanges = 0

    # lecture et écriture dans les tubes
    while True :
        os.write(dwtube1_w, b"ping")
        message = os.read(wdtube1_r, 1024).decode()
        print(f"Pere:j'ai lu'{message}' ")
        exchanges += 1
        if exchanges >= max_exchanges:
            os.write(dwtube1_w, b"stop")
            break
    os.wait()
    os.close(dwtube1_w)
    os.close(wdtube1_r)
    shm_segment1.close()
    shm_segment1.unlink()


