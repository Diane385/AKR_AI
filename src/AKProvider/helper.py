import os
import yaml

class Endpoint:
    def __init__(self, url, **param):
        self.url = url
        self.param = param

    def show(self):
        print(self.url)
        print(self.param)

class Headers:
    def __init__(self):
        self.headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
    }
        Dirname = os.path.dirname(__file__) # current directory
        Filename = os.path.join(Dirname, '../config/config.yml') # relative path to config file 
        with open(Filename, 'r') as file:
            config = yaml.safe_load(file)

        self.api_key = config['api']['key']
        #self.api_key =  {"api-key": open(os.path.join(os.path.expanduser('.'), ".akr_key.txt"), 'r').read().strip()}

class HttpRequest(Endpoint, Headers): # heritage multiple
    def __init__(self, url, **param):
        Endpoint.__init__(self, url, **param)
        Headers.__init__(self)

    def show(self):
        print(f"show from HttpRequest: {self.url.format(**self.param)}") # gérer les erreur
        print(f"show from HttpRequest: {self.headers}")