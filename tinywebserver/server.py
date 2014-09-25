#!/usr/bin/python3
import socket
import sys
from os import path
# project specific modules
from tinywebserver.request import Request
from tinywebserver.utils import Utils

utils = Utils()

class Server:
    def __init__(self, config):
        self.config = config

        self.config_test()

        self.root_dir = config.root_dir

        # checking for code changes in project importing tinywebserver,
        # to automatically restart server, in order for the changes to take effect
        utils.watch_start(config.project_dir)

    def get_404(self):
        for filename in ["404.html", "404.htm"]:
            return self.root_dir + filename if path.isfile(self.root_dir + filename) else None

        return None

    def get_index(self, requested_dir = ""):
        requested_dir = requested_dir + "/"

        for filename in ["index.html", "index.htm"]:
            return requested_dir + filename if path.isfile(requested_dir + filename) else None

        return None

    def get_file(self, requested_file):
        requested_file = self.root_dir + requested_file

        # if requested file is a dir, get the dir index file
        if requested_file[-1] == "/":
            requested_file = self.get_index(requested_file)

        if requested_file and path.isfile(requested_file):
            response_code = "200 OK"
            return {"file":requested_file, "code":response_code}
        else:
            response_code = "404 Not Found"
            four_oh_four = self.get_404()

            if four_oh_four and path.isfile(four_oh_four):
                return {"file":four_oh_four, "code":response_code}
            else:
                return None

    def serve(self, requested_file):
        response_data = ""

        utils.log("Client requested %s." % requested_file)

        response_meta = self.get_file(requested_file)

        if response_meta:
            response_code = response_meta["code"]

            f = open(response_meta["file"], "r")

            while True:
                file_line = f.readline()

                if len(file_line) == 0:
                    utils.log("Transmission completed!")
                    f.close()
                    break
                else:
                    response_data += file_line
        else:
            # catch the case 404 file does not exist
            utils.log("Sorry, requested file not found.")
            response_code = response_data = "404 Not Found"

        return {"data":response_data, "code":response_code}

    def start(self, on_request = None):
        global request
        request = Request()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # reuse socket, fixes "OSError: [Errno 98] Address already in use" after killing the server
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_address = (self.config.hostname, self.config.port)
        sock.bind(server_address)
        sock.listen(1)

        utils.log("Listening on port %s." % server_address[1])

        # trying to catch kill signaling keyboard input
        try:
            while True:
                # wait for incoming connection
                connection, client_address = sock.accept()

                try:
                    utils.log("Connection from %s:%s." % client_address)

                    # loop until we read all the request chunks
                    while True:
                        data = connection.recv(4096).decode()

                        # reached end of request
                        if len(data) < 4096:
                            utils.log("No more data from client.")
                            break

                    if(len(data) > 0):
                        request_object = request.objectify(data)
                        requested_file = request.process(data)

                        response = self.serve(requested_file)

                        # if exists, execute function that will process the posted data
                        on_request(request_object) if on_request else None

                        utils.log("Sending response...")
                        connection.send(bytes("HTTP/1.1 " + response["code"] + "\r\nContent-Type:text/html\r\n\r\n", "UTF-8"))
                        connection.sendall(bytes(response["data"], "UTF-8"))
                finally:
                    connection.close()
                    utils.log("Connection closed, waiting for next request...\n")
        except(KeyboardInterrupt, SystemExit):
            utils.log("Process got killed...")

    def config_test(self):
        # check if all required options are present, web root dir
        if not (hasattr(self.config, "hostname") and hasattr(self.config, "port") and hasattr(self.config, "root_dir")):
            print("Missing parameters in config.py file...")
            sys.exit(1)

        if not path.exists(self.config.root_dir):
            print("Server's root directory doesn't exist...")
            sys.exit(1)

def self_test():
    # check there is a config.py file
    try:
        from tinywebserver.config import Config
        return True
    except ImportError:
        return False

# check if the app runs as standalone script and not as imported a module
if __name__ == "__main__":
    if self_test():
        from tinywebserver.config import Config

        config = Config()

        srv = Server(config)
        srv.start()
    else:
        print("Please create a config.py file...")
        sys.exit(1)
