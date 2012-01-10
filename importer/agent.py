from importer.models import ImportedEntity
from importer.parser import get_companies, get_users, get_projects, \
        get_list_of_partial_tasks, get_task
from importer.crawler import NetunoCrawler

class Importer(object):

    def __init__(self, url, username, password):
        self.crawler = NetunoCrawler(url)
        self.username = username
        self.password = password

    def sign_in(self):
        if not self.crawler.logged_in:
            self.crawler.login(self.username, self.password)

    def import_organizations(self):
        self.sign_in()
        self.crawler.go_to_all_companies()
        companies = get_companies(self.crawler.content)
        ImportedEntity.import_companies_as_organizations(companies)

    def import_employees(self):
        self.sign_in()
        companies = ImportedEntity.objects.filter(category='C')
        for company in companies:
            self.crawler.go_to_users_from_company(company.original_id)
            users = get_users(self.crawler.content)
            ImportedEntity.import_users_as_employees(users)

    def import_projects(self):
        self.sign_in()
        self.crawler.go_to_all_projects()
        projects = get_projects(self.crawler.content)
        ImportedEntity.import_projects(projects)

    def import_tasks(self, partial_task_ids=None):
        if partial_task_ids is None:
            self.sign_in()
            self.crawler.go_to_all_tasks()
            partial_task_ids = [
                    task['original_id'] 
                    for task in get_list_of_partial_tasks(self.crawler.content)
            ]
        for task_id in partial_task_ids:
            self.crawler.go_to_task(task_id)
            task = get_task(self.crawler.content)
            ImportedEntity.import_task(task)
            if task['type'] == 'parent':
                self.import_tasks(task['subtasks_ids'])
