import socket




URLS = {
    '/':'hello World',
    '/hleb':'hello hleb'
}

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return(method,url)


def genetate_headers(method,url):
    if not method == 'GET':
        return('HTTP/1.1 405 Method not allowed\n\n', 405)

    if not url in URLS:
        return('HTTP/1.1 404  Not found\n\n',404)

    return ('HTTP/1.1 200 OK\n\n',200)

def generate_response(request):
    #забираем у request метод и url запроса
    method, url = parse_request(request)

    #получить заголовки и статус код
    headers, code = genetate_headers(method, url)
    return (headers + 'hello').encode()



def run():
    # параметры socket 1-протокол ip, 2-протокол tcp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #параметры 1-на каком уровне настройки(на наш socket_server),2 - допустить переиспользовать адресс,3-true
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    #параметры подключения (1-к какому домену,2-к какому порту)
    server_socket.bind(('localhost', 5000))

    # прослушка данного домена и порта на подключения
    server_socket.listen()

    #что бы все работало подключаем бесконечный цикл
    while True:
        #принимает подключения 1-клиентский сокет-его адресс
        client_socket, addr = server_socket.accept()

        print('addr',addr)
        print()

        #чтение данных из socket (int:количество байт)
        request = client_socket.recv(1024)
        print(request.decode('utf-8'))

        responce = generate_response(request.decode('utf-8'))

        #ответ клиенту
        client_socket.sendall(responce)

        #закрыть соединение
        client_socket.close()


if __name__ == '__main__':
    run()
