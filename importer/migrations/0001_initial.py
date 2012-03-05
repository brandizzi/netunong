# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ImportedEntity'
        db.create_table('importer_importedentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('original_id', self.gf('django.db.models.fields.IntegerField')()),
            ('new_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('importer', ['ImportedEntity'])


    def backwards(self, orm):
        
        # Deleting model 'ImportedEntity'
        db.delete_table('importer_importedentity')


    models = {
        'importer.importedentity': {
            'Meta': {'object_name': 'ImportedEntity'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_id': ('django.db.models.fields.IntegerField', [], {}),
            'original_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['importer']
