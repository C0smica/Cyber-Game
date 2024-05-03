import game
import socket

def check_server():
    # Checks if the server is running
    server_address = ("172.28.3.71", 36695)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect(server_address)
            return True
        except ConnectionRefusedError:
            return False

if __name__ == "__main__":
    if check_server():
        g = game.Game(500, 500)
        g.run()
    else:
        print("Server is not running. Please start the server and try again.")
