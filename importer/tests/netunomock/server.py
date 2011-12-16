import os.path
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage
from urlparse import urlparse, parse_qs

ADDRESS = (SERVER, PORT) = ('localhost', 32020)
ROOT_PATH=''
ROOT_URL = 'http://%s:%s/'  % ADDRESS
HTML_DIR = os.path.join(os.path.dirname(__file__), 'html')

class IndexRequestHandler(BaseHTTPRequestHandler):

    logged_in = False

    def do_GET(self):
        if self.path.endswith(('css','png','js','gif', 'jpg')):
            self.wfile.write('')
            return
            
        url = urlparse(self.path)
        params = parse_qs(url.query)
        print_debug(self.path)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        

        if not IndexRequestHandler.logged_in:
            self.wfile.write(self.read_html_file('login.html'))
        elif 'logout' in params:
            IndexRequestHandler.logged_in = False
            self.wfile.write(self.read_html_file('login.html'))
        elif 'm' in params:
            if 'companies' in params.get('m'):
                self.list_companies(params)
        else:
            self.wfile.write(self.read_html_file('index.html'))

    def do_POST(self):
        environment = {
            'REQUEST_METHOD':'POST',
            'CONTENT_TYPE':self.headers['Content-Type']
        }
        url = urlparse(self.path)
        params = parse_qs(url.query)

        form = FieldStorage(fp=self.rfile, headers=self.headers,
                environ=environment)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if set(['username', 'password']).issubset(set(form)):
            self.do_login(form)
        elif 'm' in params:
            if 'companies' in params.get('m'):
                self.list_companies(params, form)

    def list_companies(self, params, form=None):
        if form and form['owner_filter_id'].value == '0':
            self.wfile.write(self.read_html_file('companies_all.html'))
        else:
            self.wfile.write(self.read_html_file('companies.html'))

    def do_login(self, form):
        if form['username'].value == 'adam' and form['password'].value == 'senha':
            IndexRequestHandler.logged_in = True
            self.wfile.write(self.read_html_file('index.html'))
        else:
            self.wfile.write(self.read_html_file('login_falho.html'))

    def log_message(self, format, *args):
        return

    def read_html_file(self, html_file):
        filename = os.path.join(HTML_DIR, html_file)
        return open(filename).read()

DEBUG=False

def print_debug(info):
    if DEBUG:
        print info
               

def run_server():
    server = HTTPServer(ADDRESS, IndexRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
    
