from django.db import models

from register.models import Organization

class ImportedEntity(models.Model):
    CATEGORIES = (
        ('C', 'company'),
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
                    
            
