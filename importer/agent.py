from importer.models import ImportedEntity
from importer.parser import get_companies, get_users, get_projects, \
        get_list_of_partial_tasks, get_task
from importer.crawler import NetunoCrawler

(
    ORGANIZATIONS, EMPLOYEES, PROJECTS, TASKS
) = (
    "ORGANIZATIONS", "EMPLOYEES", "PROJECTS", "TASKS"
)

class Importer(object):

    def __init__(self, url, username, password):
        self.crawler = NetunoCrawler(url)
        self.username = username
        self.password = password
        self.already_done = []

    def sign_in(self):
        if not self.crawler.logged_in:
            self.crawler.login(self.username, self.password)

    def import_all(self):
        self.import_organizations()
        self.import_projects()
        self.import_employees()
        self.import_tasks()                

    def import_organizations(self):
        self.sign_in()
        self.crawler.go_to_all_companies()
        companies = get_companies(self.crawler.content)
        ImportedEntity.import_companies_as_organizations(companies)
        self.already_done.append(ORGANIZATIONS)
        
    def import_employees(self):
        self.sign_in()
        companies = ImportedEntity.objects.filter(category='C')
        for company in companies:
            self.crawler.go_to_users_from_company(company.original_id)
            users = get_users(self.crawler.content)
            ImportedEntity.import_users_as_employees(users)
        self.already_done.append(EMPLOYEES)

    def import_projects(self):
        self.sign_in()
        self.crawler.go_to_all_projects()
        projects = get_projects(self.crawler.content)
        ImportedEntity.import_projects(projects)
        self.already_done.append(PROJECTS)

    def import_tasks(self, task_ids=None):
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
            self.crawler.go_to_task(task_id)
            task = get_task(self.crawler.content)
            ImportedEntity.import_task(task)
            if task['type'] == 'parent':
                self.import_tasks(task['subtasks_ids'])
        if task_ids is None:
            self.already_done.append(TASKS)
