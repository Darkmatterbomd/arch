import socket

this_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    this_socket.connect(('localhost', 52000))
    try:
        # Считываем первое сообщение
        answer = this_socket.recv(1024)
        print(bytes.decode(answer))
    except ConnectionResetError:
        print("Server has terminated the connection")
        this_socket.close()
    while True:
        try:
            # Создание запроса(1)
            message = str.encode(input("Enter your message: "))
            this_socket.send(message)
            # Ожидание ответа(2)
            answer = this_socket.recv(1024)
            # Чтение ответа(3)
            print(bytes.decode(answer))
            # Обработка ошибок(4)
            if not answer:
                print("Disconnected. Close program")
                break
        except ConnectionResetError:
            print("Server has terminated the connection")
            break
except ConnectionRefusedError:
    # Ошибка при подключении
    print("Can not connect to server")
this_socket.close()

