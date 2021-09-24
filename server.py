#  coding: utf-8 
import socketserver
import mimetypes
import os
from urllib.parse import urlparse
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        try:
            self.data = self.request.recv(1024).strip()
            print ("Got a request of: %s\n" % self.data)
            # print(self.request)
            # print(self.server)
            # print(self.client_address)
            # print(self.data.decode("utf-8").split()[1])
            # print(self.data.decode("utf-8").split()[0])
            data = self.data.decode("utf-8")

            if len(data) == 0:
                return
            # get_path = "/"
            if len(data) > 0:
                get_path = self.data.decode("utf-8").split()[1]
                request = self.data.decode("utf-8").split()[0]
                print(urlparse(get_path))

                if get_path[-1] == "/":
                    new_path = get_path[0:-1]
                    split = get_path.split("/")
                    print(get_path)
                    print(split)
                    if ".html" not in split[-1]:
                        get_path = "%s/index.html" % new_path
                    else:
                        get_path =  get_path


                if get_path == "/":
                    get_path = "/index.html"
                


            print(get_path)


            cur_dir = os.path.dirname(__file__)
            file_path = os.path.join(cur_dir, "www" + get_path)
            f = open(file_path, "r")

            # print(f.read())

            mimetype, _ = mimetypes.guess_type(file_path)
            msg = f.read()
            # f.close()

            response_proto = "HTTP/1.1"
            response_status = "200"
            response_status_text = "OK" # this can be random

            if request.upper() in ["POST", "PUT", "DELETE"]:
                response_status = "405"
                response_status_text = "405 Not FOUND!"
                msg = """
                    <html>
                    <body>
                    <h1>405 Not FOUND!</h1>
                    </body>
                    </html>
                    """

            r = "%s %s %s\r\n" % (response_proto, response_status, response_status_text)
            response_headers = {
                "Content-Type": "%s; ecoding=utf-8" % mimetype,
                "Content-Length": len(msg),
                "Connection": "close",
            }

            response_headers_raw = "".join("%s: %s\r\n" % (k, v) for k, v in response_headers.items())

            self.request.send(bytearray(r,"utf-8"))
            self.request.send(bytearray(response_headers_raw,"utf-8"))
            self.request.send(bytearray("\r\n","utf-8"))
            self.request.send(bytearray(msg,"utf-8"))
            self.request.close()
        except (IsADirectoryError) as e:
            msg = """
            <html>
            <body>
            <h1>404 Not FOUND!</h1>
            </body>
            </html>
            """
            response_headers = {
                "Content-Type": "text/html; ecoding=utf-8",
                "Content-Length": len(msg),
                "Connection": "close",
            }

            response_headers_raw = "".join("%s: %s\r\n" % (k, v) for k, v in response_headers.items())

            response_proto = "HTTP/1.1"
            response_status = "303"
            response_status_text = "Not FOUND!" # this can be random
            r = "%s %s %s\r\n" % (response_proto, response_status, response_status_text)

            self.request.send(bytearray(r,"utf-8"))
            self.request.send(bytearray(response_headers_raw,"utf-8"))
            self.request.send(bytearray("\r\n","utf-8"))
            self.request.send(bytearray(msg,"utf-8"))
            self.request.close()
        except( FileNotFoundError, NotADirectoryError )as e:
            msg = """
            <html>
            <body>
            <h1>404 Not FOUND!</h1>
            </body>
            </html>
            """
            response_headers = {
                "Content-Type": "text/html; ecoding=utf-8",
                "Content-Length": len(msg),
                "Connection": "close",
            }

            response_headers_raw = "".join("%s: %s\r\n" % (k, v) for k, v in response_headers.items())

            response_proto = "HTTP/1.1"
            response_status = "404"
            response_status_text = "Not FOUND!" # this can be random

            r = "%s %s %s\r\n" % (response_proto, response_status, response_status_text)

            self.request.send(bytearray(r,"utf-8"))
            self.request.send(bytearray(response_headers_raw,"utf-8"))
            self.request.send(bytearray("\r\n","utf-8"))
            self.request.send(bytearray(msg,"utf-8"))
            self.request.close()

        except Exception as e:
            print(e)
        # FileNotFoundError, IsADirectoryError

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
