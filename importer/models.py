from django.db import models

from register.models import Organization, Project

class ImportedEntity(models.Model):
    CATEGORIES = (
        ('C', 'company'),
        ('P', 'project')
    )
    category = models.CharField(max_length=1, choices=CATEGORIES)
    original_id = models.IntegerField()
    new_id = models.IntegerField()

    @staticmethod
    def import_companies_as_organizations(companies):
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
        for project_dict in projects:
            entity = ImportedEntity.objects.get(category='C',
                    original_id=project_dict['company_id'])
            organization = Organization.objects.get(id=entity.new_id)
            project = Project(name=project_dict['name'],
                    description=project_dict['description'],
                    organization=organization)
            project.save()
            entity = ImportedEntity(
                    category='P', original_id=project_dict['original_id'],
                    new_id=project.id)
            entity.save()
