# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.execute(
            """declare @cmd varchar(4000)
declare cmds cursor for
select 'drop table [' + Table_Name + ']'
from INFORMATION_SCHEMA.TABLES
where Table_Name like 'prefix%'

open cmds
while 1=1
begin
    fetch cmds into @cmd
    if @@fetch_status != 0 break
    exec(@cmd)
end
close cmds;
deallocate cmds""")
#             """SELECT 'DROP TABLE "' + TABLE_NAME + '"'
# FROM INFORMATION_SCHEMA.TABLES
# WHERE TABLE_NAME LIKE 'Results_%'";""")  # Drop the entire App before creating it fresh

        # Adding model 'OutputBaseModel'
        db.create_table('Results_outputbasemodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('Results', ['OutputBaseModel'])

        # Adding model 'DailyReport'
        db.create_table('Results_dailyreport', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['Results.OutputBaseModel'], primary_key=True)),
            ('sparse_dict', self.gf('django.db.models.fields.TextField')()),
            ('full_line', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('Results', ['DailyReport'])

        # Adding model 'DailyByProductionType'
        db.create_table('Results_dailybyproductiontype', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['Results.OutputBaseModel'], primary_key=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(db_column='iteration', null=True, blank=True)),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
        ))
        db.send_create_signal('Results', ['DailyByProductionType'])

        # Adding model 'DailyByZoneAndProductionType'
        db.create_table('Results_dailybyzoneandproductiontype', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['Results.OutputBaseModel'], primary_key=True)),
            ('filler', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('Results', ['DailyByZoneAndProductionType'])

        # Adding model 'DailyByZone'
        db.create_table('Results_dailybyzone', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['Results.OutputBaseModel'], primary_key=True)),
            ('filler', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('Results', ['DailyByZone'])

        # Adding model 'DailyControls'
        db.create_table('Results_dailycontrols', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['Results.OutputBaseModel'], primary_key=True)),
            ('filler', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('Results', ['DailyControls'])

        # Adding model 'Iteration'
        db.create_table('Results_iteration', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['Results.OutputBaseModel'], primary_key=True)),
            ('headers', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('Results', ['Iteration'])


    def backwards(self, orm):
        # Deleting model 'OutputBaseModel'
        db.delete_table('Results_outputbasemodel')

        # Deleting model 'DailyReport'
        db.delete_table('Results_dailyreport')

        # Deleting model 'DailyByProductionType'
        db.delete_table('Results_dailybyproductiontype')

        # Deleting model 'DailyByZoneAndProductionType'
        db.delete_table('Results_dailybyzoneandproductiontype')

        # Deleting model 'DailyByZone'
        db.delete_table('Results_dailybyzone')

        # Deleting model 'DailyControls'
        db.delete_table('Results_dailycontrols')

        # Deleting model 'Iteration'
        db.delete_table('Results_iteration')


    models = {
        'Results.dailybyproductiontype': {
            'Meta': {'object_name': 'DailyByProductionType', '_ormbases': ['Results.OutputBaseModel']},
            'iteration': ('django.db.models.fields.IntegerField', [], {'db_column': "'iteration'", 'null': 'True', 'blank': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"})
        },
        'Results.dailybyzone': {
            'Meta': {'object_name': 'DailyByZone', '_ormbases': ['Results.OutputBaseModel']},
            'filler': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True'})
        },
        'Results.dailybyzoneandproductiontype': {
            'Meta': {'object_name': 'DailyByZoneAndProductionType', '_ormbases': ['Results.OutputBaseModel']},
            'filler': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True'})
        },
        'Results.dailycontrols': {
            'Meta': {'object_name': 'DailyControls', '_ormbases': ['Results.OutputBaseModel']},
            'filler': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True'})
        },
        'Results.dailyreport': {
            'Meta': {'object_name': 'DailyReport', '_ormbases': ['Results.OutputBaseModel']},
            'full_line': ('django.db.models.fields.TextField', [], {}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True'}),
            'sparse_dict': ('django.db.models.fields.TextField', [], {})
        },
        'Results.iteration': {
            'Meta': {'object_name': 'Iteration', '_ormbases': ['Results.OutputBaseModel']},
            'headers': ('django.db.models.fields.TextField', [], {}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True'})
        },
        'Results.outputbasemodel': {
            'Meta': {'object_name': 'OutputBaseModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ScenarioCreator.productiontype': {
            'Meta': {'object_name': 'ProductionType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['Results']