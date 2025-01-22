import os
import socket
import time
from Dispatcher import Dispatcher


class WatchDog:

    def __init__(self, host, port, max_restarts=3):
        self.host = host
        self.port = port
        self.max_restarts = max_restarts
        self.restart_count = 0

    def run(self):
        while self.restart_count < self.max_restarts:
            try:
                print(f"WatchDog: Démarrage du serveur principal (tentative {self.restart_count + 1})")
                pid = os.fork()

                if pid == 0:
                    # Processus enfant : lance le dispatcher
                    dispatcher = Dispatcher(self.host, self.port)
                    dispatcher.affiche()
                    os._exit(0)  # S'assurer que le processus enfant termine correctement

                else:
                    # Processus parent (watch-dog)
                    time.sleep(1)  # Attendre un peu pour laisser le serveur principal se lancer

                    try:
                        with socket.create_connection((self.host, self.port), timeout=5) as s:
                            s.sendall(b"watchdog_check")
                            response = s.recv(1024).decode()

                            if response == "alive":
                                print("WatchDog: Le serveur principal est actif.")
                                os.waitpid(pid, 0)  # Attend la fin du processus principal
                                break
                            else:
                                print("WatchDog: Réponse inattendue du serveur principal.")
                    except (socket.error, ConnectionRefusedError):
                        print("WatchDog: Impossible de communiquer avec le serveur principal.")
                    except Exception as e:
                        print(f"WatchDog: Erreur inattendue : {e}")

                    print("WatchDog: Le serveur principal a planté. Redémarrage...")
                    os.kill(pid, 9)  # Forcer l'arrêt du processus enfant
                    self.restart_count += 1

            except OSError as e:
                print(f"WatchDog: Erreur lors du fork() : {e}")
                break
            except Exception as e:
                print(f"WatchDog: Erreur inattendue : {e}")
                break

        if self.restart_count >= self.max_restarts:
            print("WatchDog: Nombre maximum de redémarrages atteint. Arrêt.")
