import os.path

import unittest2 as unittest

from django.contrib.auth import authenticate

from register.models import Organization, Employee
from importer.models import ImportedEntity

from importer.tests.util import ImportedEntityTestCase

class UserSavingTestCase(ImportedEntityTestCase):

    def save_users(self):
        # needed
        companies = [
            {'name': 'org1', 'original_id': 4, 'description': 'Organization 1'},
            {'name': 'org2', 'original_id': 8, 'description': 'Organization 2'},
        ]
        ImportedEntity.import_companies_as_organizations(companies)

        users = [
            {
                'username': 'adam.brandizzi', 
                'original_id': 1, 
                'company_id': 4, 
                'first_name': 'Adam Victor',
                'middle_name' : 'Nazareth',
                'last_name' : 'Brandizzi',
                'email' : 'adam.brandizzi@seatecnologia.com.br',
                'password' : 'kitty!'
            },
            {
                'username': 'joao.melao', 
                'original_id': 3, 
                'company_id': 8, 
                'first_name': 'Joao',
                'middle_name' : 'Ja',
                'last_name' : 'Melao',
                'email' : 'joao.melaoi@org2.com.br',
                'password' : 'puppy!'
            },
        ]
        ImportedEntity.import_users_as_employees(users)
        
        entities = ImportedEntity.objects.filter(category='U')
        self.assertEquals(2, len(entities))
        for entity, user_dict in zip(entities, users):
            self.assertEquals('U', entity.category)
            self.assertEquals('user', entity.get_category_display())
            self.assertEquals(user_dict['original_id'], entity.original_id)

            employee = Employee.objects.get(id=entity.new_id)
            self.assertEquals(user_dict['username'], employee.username)
            self.assertEquals(user_dict['first_name'], employee.first_name)
            self.assertEquals(user_dict['middle_name'], employee.middle_name)
            self.assertEquals(user_dict['last_name'], employee.last_name)
            self.assertEquals(user_dict['email'], employee.email)
            user = authenticate(username=user_dict['username'],
                    password=user_dict['password'])
            self.assertIsNotNone(user)
            self.assertEqual(user, employee.user)
            company_entity = ImportedEntity.objects.get(
                    category='C', original_id=user_dict['company_id'])
            organization = Organization.objects.get(id=company_entity.new_id)
            self.assertEquals(organization, employee.organization)

    def save_only_new_users(self):
        # needed
        companies = [
            {'name': 'org1', 'original_id': 4, 'description': 'Organization 1'},
            {'name': 'org2', 'original_id': 8, 'description': 'Organization 2'},
        ]
        ImportedEntity.import_companies_as_organizations(companies)

        users = [
            {
                'username': 'adam.brandizzi', 
                'original_id': 1, 
                'company_id': 4, 
                'first_name': 'Adam Victor',
                'middle_name' : 'Nazareth',
                'last_name' : 'Brandizzi',
                'email' : 'adam.brandizzi@seatecnologia.com.br',
                'password' : 'kitty!'
            },
        ]
        ImportedEntity.import_users_as_employees(users)
        
        entities = ImportedEntity.objects.filter(category='U')
        self.assertEquals(1, len(entities))
        # As usual
        entity, user_dict = entities[0], users[0]
        self.assertEquals('U', entity.category)
        self.assertEquals('user', entity.get_category_display())
        self.assertEquals(user_dict['original_id'], entity.original_id)

        employee = Employee.objects.get(id=entity.new_id)
        self.assertEquals(user_dict['username'], employee.username)
        self.assertEquals(user_dict['first_name'], employee.first_name)
        self.assertEquals(user_dict['middle_name'], employee.middle_name)
        self.assertEquals(user_dict['last_name'], employee.last_name)
        self.assertEquals(user_dict['email'], employee.email)
        user = authenticate(username=user_dict['username'],
                password=user_dict['password'])
        self.assertIsNotNone(user)
        self.assertEqual(user, employee.user)
        company_entity = ImportedEntity.objects.get(
                category='C', original_id=user_dict['company_id'])
        organization = Organization.objects.get(id=company_entity.new_id)
        self.assertEquals(organization, employee.organization)

        users += [
            {
                'username': 'joao.melao', 
                'original_id': 3, 
                'company_id': 8, 
                'first_name': 'Joao',
                'middle_name' : 'Ja',
                'last_name' : 'Melao',
                'email' : 'joao.melaoi@org2.com.br',
                'password' : 'puppy!'
            }
        ]

        ImportedEntity.import_users_as_employees(users)
        entities = ImportedEntity.objects.filter(category='U')
        # Should be 2, not 3
        self.assertEquals(2, len(entities))
        entities = ImportedEntity.objects.filter(category='U')
        self.assertEquals(2, len(entities))
        for entity, user_dict in zip(entities, users):
            self.assertEquals('U', entity.category)
            self.assertEquals('user', entity.get_category_display())
            self.assertEquals(user_dict['original_id'], entity.original_id)

            employee = Employee.objects.get(id=entity.new_id)
            self.assertEquals(user_dict['username'], employee.username)
            self.assertEquals(user_dict['first_name'], employee.first_name)
            self.assertEquals(user_dict['middle_name'], employee.middle_name)
            self.assertEquals(user_dict['last_name'], employee.last_name)
            self.assertEquals(user_dict['email'], employee.email)
            user = authenticate(username=user_dict['username'],
                    password=user_dict['password'])
            self.assertIsNotNone(user)
            self.assertEqual(user, employee.user)
            company_entity = ImportedEntity.objects.get(
                    category='C', original_id=user_dict['company_id'])
            organization = Organization.objects.get(id=company_entity.new_id)
            self.assertEquals(organization, employee.organization)

testSuite = unittest.TestSuite()
testSuite.addTest(UserSavingTestCase('save_users'))
testSuite.addTest(UserSavingTestCase('save_only_new_users'))
