# tinywebserver

Tinywebserver is a python3 implementation of a simple web server.

* Serves static web pages.
* Provides you a way to handle posted data.
* While you run your tinywebserver backed application, your code will get auto-reloaded everytime you make changes
or add new content anywhere in the project directory structure.

You can run tinywebserver as a standalone application, as well as a module by importing it to your projects.
It will serve your files and will let you implement all other logic like parsing posted data from forms or URL queries
and then, do your magic!

## Why?
Yeap, I know SimpleHTTPServer and I know reinventing the wheel is evil.
At the same time, it's fun and educating.

&nbsp;

## Installation

You can download the source code using Git:

    git clone https://github.com/mylk/tinywebserver.git

or, you can [get the zip archive](https://github.com/mylk/tinywebserver/zipball/master "tinywebserver source code") of the project.
In case you preferred the zip archive, you need to extract it first.

Enter the directory containing the code and run:

    python setup.py install

In Linux, you will need to precede the command with `sudo`.

&nbsp;

## Configuration / Setup

### For module usage
In case you run it as a module inside your project, you will need a configuration file in your project.
Take [this demo application's config](https://github.com/mylk/espeaker/blob/master/config.py "espeaker configuration file") as an example.
Give any name you wish to the configuration file.

### For standalone application usage
In case you run it as a standalone application put the configuration file in the tinywebserver/tinywebserver directory.
In the standalone version you need to name the configuration file `config.py`.

&nbsp;

Anyway you consume tinywebserver, you will need to create a web root directory for the web server, lets say www/.
The name of your directory, has to meet the name referred in the configuration file (`root_dir` property).

### For module usage
In case you use it as a module, this directory is going to be placed in your project.

### For standalone application usage
If you use it as a standalone application, you will need to create this directory in tinywebserver/tinywebserver.

&nbsp;

You may have a 404.html / 404.htm file in your web root directory, else some predefined content will be used for 404s.

&nbsp;

## Usage

### For module usage
In case you are going to use tinywebserver as a module:
```python
# import the required modules
from tinywebserver.server import Server
from tinywebserver.request import Request
# import your project relative configuration file
from config import Config

config = Config
server = Server
request = Request

# implement this if you wish to intercept the request data
def on_request(request):
    [...]

# start the server
srv = server(config)
srv.start(on_request)
```

You can still take [this demo application](https://github.com/mylk/espeaker/blob/master/espeaker.py "espeaker source code") as an example.

### For standalone application usage
If you need to run it as a standalone application, you just need to run the following commands:

    cd tinywebserver/tinywebserver
    chomod +x server.py
    ./server.py

&nbsp;

## Dependencies

Tinywebserver depends on really common python modules but, anyway, you can find them listed below:

* socket
* sys
* threading
* os
* time
* urllib
* html
