import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_request(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(b"Demande echange ping pong")
                data = s.recv(1024)
                print(f"Received {data!r}")
        except ConnectionRefusedError:
            print("Erreur: Impossible de se connecter au serveur.")
        except socket.timeout:
            print("Erreur: Temps de connexion au serveur expiré.")
        except Exception as e:
            print(f"Erreur inattendue: {e}")


if __name__ == "__main__":
    client = Client("127.0.0.1", 2222)
    client.send_request()
