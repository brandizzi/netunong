import threading
import traceback
from datetime import datetime

from register.models import Task
from importer.models import ImportedEntity, ExportedLog
from importer.parser import get_companies, get_users, get_projects, \
        get_list_of_partial_tasks, get_task, get_exported_description
from importer.crawler import NetunoCrawler

(
    ORGANIZATIONS, EMPLOYEES, PROJECTS, TASKS
) = (
    "ORGANIZATIONS", "EMPLOYEES", "PROJECTS", "TASKS"
)

def open_logfile(agent_method):
    def logged(self, *args, **kwargs):
        logfile = None
        t = datetime.now().strftime("%Y%m%d%H%M%S")
        if self.logfile is None:
            logfile = open('importer.%s.log'% t, 'w')
            self.logfile = logfile
        result = agent_method(self, *args, **kwargs)
        if logfile is not None:
            logfile.close()
            self.logfile = None
        return result
    return logged

class Importer(object):

    def __init__(self, url, username, password):
        self.crawler = NetunoCrawler(url)
        self.lock = threading.Lock()
        self.username = username
        self.password = password
        self.already_done = []
        self.is_running = False
        self.logfile = None

    @open_logfile
    def import_all(self, url=None, username=None, password=None):
        t = datetime.now().strftime("%Y%m%d%H%M%S")
        if self.is_running: return
        with self.lock:
            self.is_running = True
            if url: self.crawler.url = url
            if username: self.username = username
            if password: self.password = password
            self.already_done = []
            try:
                self.import_organizations()
                self.import_projects()
                self.import_employees()
                self.import_tasks()
            finally:
                self.is_running = False

    def sign_in(self):
        self.crawler.login(self.username, self.password)

    @open_logfile
    def import_organizations(self): 
        self.sign_in()
        self.crawler.go_to_all_companies()
        companies = get_companies(self.crawler.content)
        ImportedEntity.import_companies_as_organizations(companies)
        self.already_done.append(ORGANIZATIONS)
        self.logfile.write('Organizations imported')

    @open_logfile        
    def import_employees(self):
        self.sign_in()
        companies = ImportedEntity.objects.filter(category='C')
        for company in companies:
            self.crawler.go_to_users_from_company(company.original_id)
            users = get_users(self.crawler.content)
            ImportedEntity.import_users_as_employees(users)
        self.already_done.append(EMPLOYEES)
        self.logfile.write('Employees imported')

    @open_logfile
    def import_projects(self):
        self.sign_in()
        self.crawler.go_to_all_projects()
        projects = get_projects(self.crawler.content)
        ImportedEntity.import_projects(projects)
        self.already_done.append(PROJECTS)
        self.logfile.write('Projects imported')

    @open_logfile
    def import_tasks(self, task_ids=None, parent=None):
        if task_ids is None:
            self.sign_in()
            self.crawler.go_to_all_tasks()
            partial_task_ids = [
                    task['original_id'] 
                    for task in get_list_of_partial_tasks(self.crawler.content)
            ]
        else:
            partial_task_ids = task_ids
        for task_id in partial_task_ids:
            self.logfile.write('Importing task (id=%d)\n' % task_id)
            try:
                self.crawler.go_to_task(task_id)
                task_dict = get_task(self.crawler.content)
                ImportedEntity.import_task(task_dict, parent)
                entity = ImportedEntity.objects.get(
                    original_id=task_dict['original_id'], category='T')
                task = Task.objects.get(id=entity.new_id)
                if task_dict['type'] == 'parent':
                    self.import_tasks(task_dict['subtasks_ids'], parent=task)
            except Exception as e:
                self.logfile.write('Task (id=%d) not imported because of error:\n' % task_id)
                traceback.print_exc(file=self.logfile)
                self.logfile.write('URL: ' + self.crawler.browser.geturl())
                self.logfile.write('Content: ' + self.crawler.content)
            else:
                self.logfile.write('Task (id=%d) and subtasks imported\n' % task_id)
        if task_ids is None:
            self.already_done.append(TASKS)

class Exporter(object):

    def __init__(self):
        self.lock = threading.Lock()
        self.is_running = False

    def export_logs(self, wps, url, username, password):
        crawler = NetunoCrawler(url)
        if not crawler.logged_in:
            crawler.login(username, password)
        exportables = (wp 
                for wp in wps 
                if not ExportedLog.is_exported(wp)
                    and wp.is_complete())
        for wp in exportables:
            task_id = wp.executed_task.id
            entity = ImportedEntity.objects.get(category='T', new_id=task_id)
            original_task_id  = entity.original_id
            crawler.go_to_task_log_registration(original_task_id)
            crawler.register_log(wp.end, wp.total_time, get_exported_description(wp))
            log = ExportedLog(working_period=wp)
            log.save()

importer = Importer('','','')
