import socket
import random
import pickle

# Server configuration
HOST = '172.28.1.81'
PORT = 12345

# Function to generate obstacles
def generate_obstacles():
    obstacles = []
    for _ in range(3):
        temp = 500 - 200 - 100
        obstacle_y = random.randint(100, temp)
        obstacle_height = 200  # Adjust according to your game screen size
        x = 50
        obstacles.append((x, obstacle_y, obstacle_height))
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
        server_socket.listen(30)
        print("Server is listening...")

        while True:
            conn, addr = server_socket.accept()
            print("Connected to:", addr)
            threaded_client(conn)

if __name__ == "__main__":
    main()
