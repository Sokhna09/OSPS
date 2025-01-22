import os
import sys
from multiprocessing import shared_memory

try:
    # Création du segment mémoire partagée
    shm_segment1 = shared_memory.SharedMemory(name='012345', create=True, size=10)
    print('Nom du segment mémoire partagée :', shm_segment1.name)

    # Accès + écriture de données
    print('Taille du segment mémoire partagée en octets via premier accès :', len(shm_segment1.buf))
    shm_segment1.buf[:] = bytearray([74, 73, 72, 71, 70, 69, 68, 67, 66, 65])
except Exception as e:
    print(f"Erreur lors de la création du segment mémoire partagée : {e}")
    sys.exit(1)

try:
    # Création des tubes
    dwtube1_r, dwtube1_w = os.pipe()
    wdtube1_r, wdtube1_w = os.pipe()
except OSError as e:
    print(f"Erreur lors de la création des tubes : {e}")
    shm_segment1.close()
    shm_segment1.unlink()
    sys.exit(1)

max_exchanges = 5

try:
    newpid = os.fork()
except OSError as e:
    print(f"Erreur lors du fork() : {e}")
    shm_segment1.close()
    shm_segment1.unlink()
    sys.exit(1)

if newpid == 0:
    try:
        print("je suis le fils")
        shm_segment2 = shared_memory.SharedMemory(shm_segment1.name)
        data = bytes(shm_segment2.buf[:])
        print(f"Fils : contenu de la mémoire partagée : {data} (valeurs ASCII : {list(data)})")
        os.close(dwtube1_w)
        os.close(wdtube1_r)
        exchanges = 0

        while True:
            message = os.read(dwtube1_r, 1024).decode()
            if message == "stop":
                print("Fils : arrêté après le message stop")
                break
            print(f"Fils : j'ai lu '{message}'")
            os.write(wdtube1_w, b"pong")
            exchanges += 1

        os.close(dwtube1_r)
        os.close(wdtube1_w)
        shm_segment2.close()
    except Exception as e:
        print(f"Erreur dans le processus fils : {e}")
        sys.exit(1)
else:
    try:
        print('je suis le père')
        os.close(dwtube1_r)
        os.close(wdtube1_w)
        exchanges = 0

        while True:
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
    except Exception as e:
        print(f"Erreur dans le processus père : {e}")
        shm_segment1.close()
        shm_segment1.unlink()
        sys.exit(1)
