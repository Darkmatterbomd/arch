import socket
import phone_dir

pd = phone_dir.DB_Arch('f.json', 'folder')

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # тип адресации, тип сокета
listener.bind(('localhost', 52000)) # (ip, port),
# Ожидает запрос
listener.listen(1)
client, client_info = listener.accept() # client_info - ip-адрес и порт клиента
print("Client joined")
init_message = "Wellcome to phone directory!\n Choose number of action: \n 0. Leave\n 1. Create dir\n 2. Open dir\n 3. Delete dir\n 4. Create backup "
client.send(str.encode(init_message))
while True:
    # Обрабатывает запрос(2.1)

    data = client.recv(1024)
    ans = bytes.decode(data)
    print(f'Message from client: {ans}')
    if ans == '0':
        print("client leave")
        break
    elif ans == '1':
        pd.create_db()
        client.send(b'Phone dir was created')
    elif ans == '2':
        pd.open_db()
        client.send(b'Phone dir was opened')
    elif ans == '3':
        pd.del_db()
        client.send(b'Phone dir was removed')
    elif ans == '4':
        pd.create_backup()
        client.send(b'backup was created')
    else:
        client.send(b'Repeat input please')

client.close()
listener.close()

