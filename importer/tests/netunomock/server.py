import os.path
from datetime import datetime
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage
from urlparse import urlparse, parse_qs

ADDRESS = (SERVER, PORT) = ('localhost', 32020)
ROOT_PATH=''
SHOW_LOGS_PATH = 'showlogs'
ROOT_URL = 'http://%s:%s/'  % ADDRESS
HTML_DIR = os.path.join(os.path.dirname(__file__), 'html')

logs = []

LOGS_MASK = """Task id: %s<br/>
Log creator: %s<br/>
Date: %s<br/>
Worked hours: %s<br/>
Description: %s<br/>"""

class IndexRequestHandler(BaseHTTPRequestHandler):

    logged_in = False

    def __init__(self, *args, **kwargs):
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

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

        if self.path.endswith(SHOW_LOGS_PATH):
            self.show_logs(logs)
        elif not IndexRequestHandler.logged_in:
            self.wfile.write(self.read_html_file('login.html'))
        elif 'logout' in params:
            IndexRequestHandler.logged_in = False
            self.wfile.write(self.read_html_file('login.html'))
        elif 'm' in params:
            m = params.get('m')[0]
            shower = IndexRequestHandler.showers[m]
            shower(self, params)
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
            m = params.get('m')[0]
            shower = IndexRequestHandler.showers[m]
            shower(self, params, form)


    def show_companies(self, params, form=None):
        if 'company_id' in params:
            if 'tab' in params and '3' in params['tab']:
                company_id = params['company_id']
                doc = self.read_html_file('company%s-users.html'%company_id[0])
                self.wfile.write(doc)
            else:
                company_id = params['company_id']
                doc = self.read_html_file('company%s.html'%company_id[0])
                self.wfile.write(doc)
        elif form and form['owner_filter_id'].value == '0':
            self.wfile.write(self.read_html_file('companies_all.html'))
        else:
            self.wfile.write(self.read_html_file('companies.html'))

    def show_projects(self, params, form=None):
        if form and form['department'].value == 'company_0':
            self.wfile.write(self.read_html_file('projects_all.html'))
        else:
            self.wfile.write(self.read_html_file('projects.html'))

    def show_tasks(self, params, form=None):
        if 'task_id' in params and 'a' in params and params['a'][0]  == 'view':
            task_id = params['task_id'][0]
            if 'tab' in params and params['tab'][0] == '1' and not form:
                template = self.read_html_file('task-new-log.html')
                template = template.replace('%MOCK_TASK_ID%', task_id)
                template = template.replace('%MOCK_USER_ID%', '1')
                d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                template = template.replace('%MOCK_TASK_LOG_DATE%', d)
                self.wfile.write(template)
            elif form and form['dosql'].value == 'do_updatetask':
                log = (
                        form['task_log_task'].value,
                        form['task_log_creator'].value,
                        form['task_log_date'].value,
                        form['task_log_hours'].value,
                        form['task_log_description'].value,
                )
                logs.append(log)
                self.show_logs(logs)
            else:
                self.wfile.write(self.read_html_file('task%s.html'%task_id))
        elif form and form['f'].value == 'all':
            self.wfile.write(self.read_html_file('tasks_all.html'))
        else:
            self.wfile.write(self.read_html_file('tasks.html'))


    def do_login(self, form):
        if form['username'].value == 'adam' and form['password'].value == 'senha':
            IndexRequestHandler.logged_in = True
            self.wfile.write(self.read_html_file('index.html'))
        else:
            self.wfile.write(self.read_html_file('login_falho.html'))

    def show_logs(self, logs):
        for log in logs:
            self.wfile.write(LOGS_MASK % log)

    def log_message(self, format, *args):
        return

    def read_html_file(self, html_file):
        filename = os.path.join(HTML_DIR, html_file)
        return open(filename).read()

    showers = {
        'companies' : show_companies,
        'projects' : show_projects,
        'tasks'  : show_tasks
    }

DEBUG=False

def print_debug(info):
    if DEBUG:
        print info
               

def run_server():
    try:
        server = HTTPServer(ADDRESS, IndexRequestHandler)
        server.serve_forever()
    except Exception as e:
        print e

if __name__ == "__main__":
    run_server()
    
