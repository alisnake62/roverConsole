from .console import Instructions, RoverMessage
import socket

class MarsLink:

    _ip     : str = '127.0.0.1'
    _port   : int = 3333
    
    _socket: socket

    def __enter__(self) -> 'MarsLink':
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._ip, self._port))
        print("Connexion établie avec le rover")

        return self

    def __exit__(self) -> None:
        self._socket.close()

    def sendInstructions(self, instructions:Instructions) -> RoverMessage:

        self._socket.send(bytes(instructions.linkFormat(), "utf-8"))

        message = self._socket.recv(1024).decode()
        print(f"Response from mars : {message}")

        return RoverMessage(value=message)