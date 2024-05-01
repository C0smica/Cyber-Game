import socket
import random
import pickle

# Server configuration
HOST = '127.0.0.1'
PORT = 12345

# Function to generate obstacles
def generate_obstacles():
    obstacles = []
    for _ in range(3):
        obstacle_height = random.randint(1, 10)
        obstacle_y = random.randint(1, 20 - obstacle_height)  # Adjust according to your game screen size
        obstacles.append((30, obstacle_y, obstacle_height))
    return obstacles

def threaded_client(conn):
    while True:
        try:
            obstacles = generate_obstacles()
            obstacles_data = pickle.dumps(obstacles)
            conn.sendall(obstacles_data)
            ack = conn.recv(1024)  # Wait for acknowledgement from client
            if not ack:
                break
        except Exception as e:
            print("Error in threaded_client:", e)
            break

    print("Connection closed")
    conn.close()

def main():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server is listening...")

        while True:
            conn, addr = server_socket.accept()
            print("Connected to:", addr)
            threaded_client(conn)

if __name__ == "__main__":
    main()
