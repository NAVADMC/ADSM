# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OutputBaseModel'
        db.create_table('Results_outputbasemodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('Results', ['OutputBaseModel'])

        # Adding model 'DailyReport'
        db.create_table('Results_dailyreport', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('sparse_dict', self.gf('django.db.models.fields.TextField')()),
            ('full_line', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('Results', ['DailyReport'])

        # Adding model 'SpreadGroup'
        db.create_table('Results_spreadgroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('UAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UDir', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UInd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UAir', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ADir', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AInd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AAir', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['SpreadGroup'])

        # Adding model 'DetectionBracketGroup'
        db.create_table('Results_detectionbracketgroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('_blank', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('Clin', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('Test', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['DetectionBracketGroup'])

        # Adding model 'DetectionGroup'
        db.create_table('Results_detectiongroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('UAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UClin', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UTest', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AClin', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ATest', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['DetectionGroup'])

        # Adding model 'TraceGroup'
        db.create_table('Results_tracegroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('UAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UAllp', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UDir', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UDirp', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UInd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UIndp', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AAllp', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ADir', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ADirp', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AInd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AIndp', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['TraceGroup'])

        # Adding model 'TestTriggerGroup'
        db.create_table('Results_testtriggergroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('UAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('URing', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UDirFwd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UIndFwd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UDirBack', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UIndBack', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UDet', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ARing', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ADirFwd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AIndFwd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ADirBack', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AIndBack', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ADet', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['TestTriggerGroup'])

        # Adding model 'TestOutcomeGroup'
        db.create_table('Results_testoutcomegroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('UTruePos', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UFalsePos', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UTrueNeg', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UFalseNeg', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['TestOutcomeGroup'])

        # Adding model 'VaccinationGroup'
        db.create_table('Results_vaccinationgroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('UAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UIni', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('URing', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AIni', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ARing', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['VaccinationGroup'])

        # Adding model 'WaitGroup'
        db.create_table('Results_waitgroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('UAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UMax', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UMaxDay', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AMax', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AMaxDay', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UTimeMax', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UTimeAvg', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UDaysInQueue', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ADaysInQueue', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['WaitGroup'])

        # Adding model 'DestructionGroup'
        db.create_table('Results_destructiongroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('_blank', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('All', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('Unsp', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('Ring', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('Det', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('Ini', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('DirFwd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('IndFwd', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('DirBack', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('IndBack', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['DestructionGroup'])

        # Adding model 'StateGroup'
        db.create_table('Results_stategroup', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('USusc', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ULat', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('USubc', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UClin', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UNImm', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UVImm', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UDest', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ASusc', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ALat', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ASubc', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AClin', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ANImm', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('AVImm', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ADest', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['StateGroup'])

        # Adding model 'DailyByProductionType'
        db.create_table('Results_dailybyproductiontype', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(blank=True, db_column='iteration', null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(blank=True, db_column='iteration', null=True)),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.SpreadGroup'], blank=True, related_name='+', null=True)),
            ('inf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.SpreadGroup'], blank=True, related_name='+', null=True)),
            ('firstDetection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.DetectionBracketGroup'], blank=True, related_name='+', null=True)),
            ('lastDetection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.DetectionBracketGroup'], blank=True, related_name='+', null=True)),
            ('det', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.DetectionGroup'], blank=True, related_name='+', null=True)),
            ('tr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.TraceGroup'], blank=True, related_name='+', null=True)),
            ('exm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.TestTriggerGroup'], blank=True, related_name='+', null=True)),
            ('tst', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.TestOutcomeGroup'], blank=True, related_name='+', null=True)),
            ('tstc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.TestTriggerGroup'], blank=True, related_name='+', null=True)),
            ('firstVaccination', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('firstVaccinationRing', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vac', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.VaccinationGroup'], blank=True, related_name='+', null=True)),
            ('vacw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.WaitGroup'], blank=True, related_name='+', null=True)),
            ('firstDestruction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.DestructionGroup'], blank=True, related_name='+', null=True)),
            ('descU', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.DestructionGroup'], blank=True, related_name='+', null=True)),
            ('descA', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.DestructionGroup'], blank=True, related_name='+', null=True)),
            ('desw', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.WaitGroup'], blank=True, related_name='+', null=True)),
            ('tsd', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Results.StateGroup'], blank=True, related_name='+', null=True)),
        ))
        db.send_create_signal('Results', ['DailyByProductionType'])

        # Adding model 'DailyByZoneAndProductionType'
        db.create_table('Results_dailybyzoneandproductiontype', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(blank=True, db_column='iteration', null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(blank=True, db_column='iteration', null=True)),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone'])),
            ('unitsInZone', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('unitDaysInZone', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('animalDaysInZone', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['DailyByZoneAndProductionType'])

        # Adding model 'DailyByZone'
        db.create_table('Results_dailybyzone', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(blank=True, db_column='iteration', null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(blank=True, db_column='iteration', null=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone'])),
            ('zoneArea', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('maxZoneArea', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('maxZoneAreaDay', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('zonePerimeter', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('maxZonePerimeter', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('maxZonePerimeterDay', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('finalZoneArea', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('finalZonePerimeter', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('num_separate_areas', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['DailyByZone'])

        # Adding model 'DailyControls'
        db.create_table('Results_dailycontrols', (
            ('outputbasemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Results.OutputBaseModel'], primary_key=True, unique=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(blank=True, db_column='iteration', null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(blank=True, db_column='iteration', null=True)),
            ('diseaseDuration', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('adqnU', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('adqcU', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('detOccurred', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('costSurveillance', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vaccOccurred', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vacwUMax', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vacwUMaxDay', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vacwUDaysInQueue', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vacwUTimeAvg', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vacwUTimeMax', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vacwAMax', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vacwAMaxDay', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vacwADaysInQueue', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vaccSetup', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vaccVaccination', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vaccSubtotal', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('destrOccurred', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('deswUMax', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('deswUMaxDay', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('deswUDaysInQueue', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('deswUTimeAvg', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('deswUTimeMax', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('deswAMax', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('deswAMaxDay', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('deswADaysInQueue', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('destrAppraisal', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('destrEuthanasia', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('destrIndemnification', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('destrDisposal', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('destrCleaning', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('destrSubtotal', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('outbreakDuration', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('costsTotal', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('firstDetUInfAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('firstDetAInfAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('ratio', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('average_prevalence', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('detcUqAll', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['DailyControls'])


    def backwards(self, orm):
        # Deleting model 'OutputBaseModel'
        db.delete_table('Results_outputbasemodel')

        # Deleting model 'DailyReport'
        db.delete_table('Results_dailyreport')

        # Deleting model 'SpreadGroup'
        db.delete_table('Results_spreadgroup')

        # Deleting model 'DetectionBracketGroup'
        db.delete_table('Results_detectionbracketgroup')

        # Deleting model 'DetectionGroup'
        db.delete_table('Results_detectiongroup')

        # Deleting model 'TraceGroup'
        db.delete_table('Results_tracegroup')

        # Deleting model 'TestTriggerGroup'
        db.delete_table('Results_testtriggergroup')

        # Deleting model 'TestOutcomeGroup'
        db.delete_table('Results_testoutcomegroup')

        # Deleting model 'VaccinationGroup'
        db.delete_table('Results_vaccinationgroup')

        # Deleting model 'WaitGroup'
        db.delete_table('Results_waitgroup')

        # Deleting model 'DestructionGroup'
        db.delete_table('Results_destructiongroup')

        # Deleting model 'StateGroup'
        db.delete_table('Results_stategroup')

        # Deleting model 'DailyByProductionType'
        db.delete_table('Results_dailybyproductiontype')

        # Deleting model 'DailyByZoneAndProductionType'
        db.delete_table('Results_dailybyzoneandproductiontype')

        # Deleting model 'DailyByZone'
        db.delete_table('Results_dailybyzone')

        # Deleting model 'DailyControls'
        db.delete_table('Results_dailycontrols')


    models = {
        'Results.dailybyproductiontype': {
            'Meta': {'object_name': 'DailyByProductionType', '_ormbases': ['Results.OutputBaseModel']},
            'day': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'db_column': "'iteration'", 'null': 'True'}),
            'descA': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.DestructionGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'descU': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.DestructionGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'desw': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.WaitGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'det': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.DetectionGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'exm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.TestTriggerGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'exp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.SpreadGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'firstDestruction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.DestructionGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'firstDetection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.DetectionBracketGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'firstVaccination': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'firstVaccinationRing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'inf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.SpreadGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'db_column': "'iteration'", 'null': 'True'}),
            'lastDetection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.DetectionBracketGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'tr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.TraceGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'tsd': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.StateGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'tst': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.TestOutcomeGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'tstc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.TestTriggerGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'vac': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.VaccinationGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'vacw': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Results.WaitGroup']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'})
        },
        'Results.dailybyzone': {
            'Meta': {'object_name': 'DailyByZone', '_ormbases': ['Results.OutputBaseModel']},
            'day': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'db_column': "'iteration'", 'null': 'True'}),
            'finalZoneArea': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'finalZonePerimeter': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'db_column': "'iteration'", 'null': 'True'}),
            'maxZoneArea': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'maxZoneAreaDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'maxZonePerimeter': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'maxZonePerimeterDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'num_separate_areas': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Zone']"}),
            'zoneArea': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'zonePerimeter': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'Results.dailybyzoneandproductiontype': {
            'Meta': {'object_name': 'DailyByZoneAndProductionType', '_ormbases': ['Results.OutputBaseModel']},
            'animalDaysInZone': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'db_column': "'iteration'", 'null': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'db_column': "'iteration'", 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'unitDaysInZone': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'unitsInZone': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Zone']"})
        },
        'Results.dailycontrols': {
            'Meta': {'object_name': 'DailyControls', '_ormbases': ['Results.OutputBaseModel']},
            'adqcU': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'adqnU': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'average_prevalence': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'costSurveillance': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'costsTotal': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'db_column': "'iteration'", 'null': 'True'}),
            'destrAppraisal': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destrCleaning': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destrDisposal': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destrEuthanasia': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destrIndemnification': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destrOccurred': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'destrSubtotal': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'deswADaysInQueue': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'deswAMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'deswAMaxDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'deswUDaysInQueue': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'deswUMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'deswUMaxDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'deswUTimeAvg': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'deswUTimeMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'detOccurred': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'detcUqAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'diseaseDuration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'firstDetAInfAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'firstDetUInfAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'db_column': "'iteration'", 'null': 'True'}),
            'outbreakDuration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'}),
            'ratio': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccOccurred': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccSetup': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccSubtotal': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vaccVaccination': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vacwADaysInQueue': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vacwAMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vacwAMaxDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vacwUDaysInQueue': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vacwUMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vacwUMaxDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vacwUTimeAvg': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'vacwUTimeMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'Results.dailyreport': {
            'Meta': {'object_name': 'DailyReport', '_ormbases': ['Results.OutputBaseModel']},
            'full_line': ('django.db.models.fields.TextField', [], {}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'}),
            'sparse_dict': ('django.db.models.fields.TextField', [], {})
        },
        'Results.destructiongroup': {
            'All': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Det': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'DirBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'DirFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'IndBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'IndFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Ini': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'DestructionGroup', '_ormbases': ['Results.OutputBaseModel']},
            'Ring': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Unsp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            '_blank': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Results.detectionbracketgroup': {
            'Clin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'DetectionBracketGroup', '_ormbases': ['Results.OutputBaseModel']},
            'Test': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            '_blank': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Results.detectiongroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AClin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ATest': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'DetectionGroup', '_ormbases': ['Results.OutputBaseModel']},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UClin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTest': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Results.outputbasemodel': {
            'Meta': {'object_name': 'OutputBaseModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.spreadgroup': {
            'AAir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AInd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'SpreadGroup', '_ormbases': ['Results.OutputBaseModel']},
            'UAir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UInd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Results.stategroup': {
            'AClin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADest': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ALat': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ANImm': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ASubc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ASusc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AVImm': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'StateGroup', '_ormbases': ['Results.OutputBaseModel']},
            'UClin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDest': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ULat': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UNImm': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'USubc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'USusc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UVImm': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Results.testoutcomegroup': {
            'Meta': {'object_name': 'TestOutcomeGroup', '_ormbases': ['Results.OutputBaseModel']},
            'UFalseNeg': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UFalsePos': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTrueNeg': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTruePos': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Results.testtriggergroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADet': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADirBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADirFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AIndBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AIndFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ARing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'TestTriggerGroup', '_ormbases': ['Results.OutputBaseModel']},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDet': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDirBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDirFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UIndBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UIndFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'URing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Results.tracegroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AAllp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADirp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AInd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AIndp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'TraceGroup', '_ormbases': ['Results.OutputBaseModel']},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UAllp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDirp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UInd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UIndp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Results.vaccinationgroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AIni': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ARing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'VaccinationGroup', '_ormbases': ['Results.OutputBaseModel']},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UIni': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'URing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Results.waitgroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADaysInQueue': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AMaxDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'WaitGroup', '_ormbases': ['Results.OutputBaseModel']},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDaysInQueue': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UMaxDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTimeAvg': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTimeMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outputbasemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Results.OutputBaseModel']", 'primary_key': 'True', 'unique': 'True'})
        },
        'ScenarioCreator.productiontype': {
            'Meta': {'object_name': 'ProductionType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'ScenarioCreator.zone': {
            'Meta': {'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone_description': ('django.db.models.fields.TextField', [], {}),
            'zone_radius': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['Results']