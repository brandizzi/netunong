from django.db import models

from register.models import Organization, Project, Task, Employee

def get_original_ids_from_dicts(dicts):
    return (d['original_id'] for d in dicts)

def get_original_ids_from_entities(entities):
    return (entity.original_id for entity in entities)

def get_original_ids_from_already_imported(category, dicts):
    ids = get_original_ids_from_dicts(dicts)
    already_imported = ImportedEntity.objects.filter(category=category,
            original_id__in=ids)
    return get_original_ids_from_entities(already_imported)

def get_not_imported_ones(category, dicts):
    already_imported_ids = get_original_ids_from_already_imported(category,
                dicts)
    return [d for d in dicts if d['original_id'] not in already_imported_ids]

class ImportedEntity(models.Model):
    CATEGORIES = (
        ('C', 'company'),
        ('P', 'project'),
        ('T', 'task'),
        ('U', 'user')
    )
    category = models.CharField(max_length=1, choices=CATEGORIES)
    original_id = models.IntegerField()
    new_id = models.IntegerField()

    @staticmethod
    def import_companies_as_organizations(companies):
        companies = get_not_imported_ones('C', companies)
        for company in companies:
            organization = Organization(
                    name=company['name'], description=company['description'])
            organization.save()
            entity = ImportedEntity(
                    category='C', original_id=company['original_id'],
                    new_id=organization.id)
            entity.save()

    @staticmethod
    def import_projects(projects):
        projects = get_not_imported_ones('P', projects)
        for project_dict in projects:
            company_entity = ImportedEntity.objects.get(category='C',
                    original_id=project_dict['company_id'])
            organization = Organization.objects.get(id=company_entity.new_id)
            project = Project(name=project_dict['name'],
                    description=project_dict['description'],
                    organization=organization)
            project.save()
            entity = ImportedEntity(
                    category='P', original_id=project_dict['original_id'],
                    new_id=project.id)
            entity.save()

    @staticmethod
    def import_task(task_dict):
        if task_dict['type'] == 'parent': raise SavingParentTask()
        project_entity = ImportedEntity.objects.get(category='P',
                original_id=task_dict['project_id'])
        project = Project.objects.get(id=project_entity.new_id)
        task = Task(name=task_dict['name'],
                description=task_dict['description'],
                project=project)
        task.save()
        entity = ImportedEntity(
                category='T', original_id=task_dict['original_id'],
                new_id=task.id)
        entity.save()

    @staticmethod
    def import_users_as_employees(users):
        users = get_not_imported_ones('U', users)
        for user_dict in users:
            company_entity = ImportedEntity.objects.get(category='C',
                    original_id=user_dict['company_id'])
            organization = Organization.objects.get(id=company_entity.new_id)
            employee = Employee.create_employee(
                    organization=organization, username=user_dict['username'],
                    password=user_dict['password'], 
                    first_name=user_dict['first_name'], 
                    middle_name=user_dict['middle_name'],
                    last_name=user_dict['last_name'], email=user_dict['email'])
            entity = ImportedEntity(
                    category='U', original_id=user_dict['original_id'],
                    new_id=employee.id)
            entity.save()


class SavingParentTask(Exception):
    pass
