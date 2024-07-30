from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за обработку входящих запросов от клиентов.
    """
    filename = "index.html"

    def read_index_file(self) -> Optional[str]:
        """
        Читает содержимое файла index.html.
        Возвращает содержимое как строку или None, если файл не найден.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return None

    def do_GET(self) -> None:
        """
        Метод для обработки входящих GET-запросов.
        """
        context = self.read_index_file()
        if context is not None:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(context, "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found: index.html not found.")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Сервер запущен http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер остановлен.")
