# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Organization'
        db.create_table('register_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('register', ['Organization'])

        # Adding model 'Project'
        db.create_table('register_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['register.Organization'])),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('register', ['Project'])

        # Adding model 'Task'
        db.create_table('register_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['register.Project'])),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('register', ['Task'])

        # Adding model 'Employee'
        db.create_table('register_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['register.Organization'])),
        ))
        db.send_create_signal('register', ['Employee'])

        # Adding M2M table for field tasks on 'Employee'
        db.create_table('register_employee_tasks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('employee', models.ForeignKey(orm['register.employee'], null=False)),
            ('task', models.ForeignKey(orm['register.task'], null=False))
        ))
        db.create_unique('register_employee_tasks', ['employee_id', 'task_id'])

        # Adding model 'WorkingPeriod'
        db.create_table('register_workingperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['register.Employee'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('intended', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('intended_task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='intended_working_periods', null=True, to=orm['register.Task'])),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('executed', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('executed_task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='executed_working_periods', null=True, to=orm['register.Task'])),
        ))
        db.send_create_signal('register', ['WorkingPeriod'])


    def backwards(self, orm):
        
        # Deleting model 'Organization'
        db.delete_table('register_organization')

        # Deleting model 'Project'
        db.delete_table('register_project')

        # Deleting model 'Task'
        db.delete_table('register_task')

        # Deleting model 'Employee'
        db.delete_table('register_employee')

        # Removing M2M table for field tasks on 'Employee'
        db.delete_table('register_employee_tasks')

        # Deleting model 'WorkingPeriod'
        db.delete_table('register_workingperiod')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'register.employee': {
            'Meta': {'object_name': 'Employee'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['register.Organization']"}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['register.Task']", 'null': 'True', 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'register.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'register.project': {
            'Meta': {'object_name': 'Project'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['register.Organization']"})
        },
        'register.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['register.Project']"})
        },
        'register.workingperiod': {
            'Meta': {'ordering': "['start', 'end']", 'object_name': 'WorkingPeriod'},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['register.Employee']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'executed': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'executed_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'executed_working_periods'", 'null': 'True', 'to': "orm['register.Task']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intended': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'intended_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'intended_working_periods'", 'null': 'True', 'to': "orm['register.Task']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['register']
