from urllib import parse as urllib_parse
from html import unescape
# project specific modules
from tinywebserver.utils import Utils

#utils = utils.Utils

class Request:
    def is_method(self, request, method):
        return method.upper() in request

    def has_data(request):
        return "Data" in request

    # parse the data section of the request
    def get_data(self, headers):
        data = {}

        # extract data from POST requests
        if headers.startswith("POST"):
            headers_split = headers.split("\r\n\r\n")
            data_raw = headers_split[1]
        # extract data from GET requests
        elif headers.startswith("GET"):
            headers_split = headers.split("\r\n")
            data_raw = headers_split[0].split(" ")[1]

        # get the actual data from the request
        if "?" in data_raw:
            data_raw = data_raw.split("?")[1]

        # has data
        if data_raw.find("=") > -1:
            for param_raw in data_raw.split("&"):
                param = param_raw.split("=")
                # unquote_plus decodes URL encoding and replaces +s to spaces
                # decode html encoding for unicode characters
                data[param[0]] = unescape(urllib_parse.unquote_plus(str(param[1]))).replace("+", " ")

        return data

    # objectify the raw http request
    def objectify(self, headers):
        request = {}

        # get the data section of the request
        request["Data"] = self.get_data(headers)

        # parse the headers' section
        if headers.startswith("POST"):
            headers_split = headers.split("\r\n\r\n")
            headers = headers_split[0]

        for row in headers.split("\r\n"):
            if row != "":
                if row.find(": ") > -1:
                    header = row.split(": ")
                else:
                    header = row.split(" ")

                request[header[0]] = header[1]

        return request

    # get the name of the requested file or dir
    def process(self, data):
        request = self.objectify(data)

        if self.is_method(request, "GET"):
            request_method = "GET"
        elif self.is_method(request, "POST"):
            request_method = "POST"

        # get the filename, excluding url query params
        requested_file = request[request_method].split("?")[0]

        return requested_file
