# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DailyReport'
        db.create_table('Results_dailyreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sparse_dict', self.gf('django.db.models.fields.TextField')()),
            ('full_line', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('Results', ['DailyReport'])

        # Adding model 'SpreadGroup'
        db.create_table('Results_spreadgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_blank', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('Clin', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('Test', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['DetectionBracketGroup'])

        # Adding model 'DetectionGroup'
        db.create_table('Results_detectiongroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('UTruePos', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UFalsePos', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UTrueNeg', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('UFalseNeg', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['TestOutcomeGroup'])

        # Adding model 'VaccinationGroup'
        db.create_table('Results_vaccinationgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('exp', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.SpreadGroup'], related_name='+')),
            ('inf', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.SpreadGroup'], related_name='+')),
            ('firstDetection', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.DetectionBracketGroup'], related_name='+')),
            ('lastDetection', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.DetectionBracketGroup'], related_name='+')),
            ('det', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.DetectionGroup'], related_name='+')),
            ('tr', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.TraceGroup'], related_name='+')),
            ('exm', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.TestTriggerGroup'], related_name='+')),
            ('tst', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.TestOutcomeGroup'], related_name='+')),
            ('tstc', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.TestTriggerGroup'], related_name='+')),
            ('firstVaccination', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('firstVaccinationRing', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('vac', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.VaccinationGroup'], related_name='+')),
            ('vacw', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.WaitGroup'], related_name='+')),
            ('firstDestruction', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.DestructionGroup'], related_name='+')),
            ('descU', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.DestructionGroup'], related_name='+')),
            ('descA', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.DestructionGroup'], related_name='+')),
            ('desw', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.WaitGroup'], related_name='+')),
            ('tsd', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['Results.StateGroup'], related_name='+')),
        ))
        db.send_create_signal('Results', ['DailyByProductionType'])

        # Adding model 'DailyByZoneAndProductionType'
        db.create_table('Results_dailybyzoneandproductiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('production_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'])),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone'])),
            ('unitsInZone', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('unitDaysInZone', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('animalDaysInZone', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('Results', ['DailyByZoneAndProductionType'])

        # Adding model 'DailyByZone'
        db.create_table('Results_dailybyzone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
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
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iteration', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
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
            'Meta': {'object_name': 'DailyByProductionType'},
            'day': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'descA': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.DestructionGroup']", 'related_name': "'+'"}),
            'descU': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.DestructionGroup']", 'related_name': "'+'"}),
            'desw': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.WaitGroup']", 'related_name': "'+'"}),
            'det': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.DetectionGroup']", 'related_name': "'+'"}),
            'exm': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.TestTriggerGroup']", 'related_name': "'+'"}),
            'exp': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.SpreadGroup']", 'related_name': "'+'"}),
            'firstDestruction': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.DestructionGroup']", 'related_name': "'+'"}),
            'firstDetection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.DetectionBracketGroup']", 'related_name': "'+'"}),
            'firstVaccination': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'firstVaccinationRing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inf': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.SpreadGroup']", 'related_name': "'+'"}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'lastDetection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.DetectionBracketGroup']", 'related_name': "'+'"}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'tr': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.TraceGroup']", 'related_name': "'+'"}),
            'tsd': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.StateGroup']", 'related_name': "'+'"}),
            'tst': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.TestOutcomeGroup']", 'related_name': "'+'"}),
            'tstc': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.TestTriggerGroup']", 'related_name': "'+'"}),
            'vac': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.VaccinationGroup']", 'related_name': "'+'"}),
            'vacw': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['Results.WaitGroup']", 'related_name': "'+'"})
        },
        'Results.dailybyzone': {
            'Meta': {'object_name': 'DailyByZone'},
            'day': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'finalZoneArea': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'finalZonePerimeter': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'maxZoneArea': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'maxZoneAreaDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'maxZonePerimeter': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'maxZonePerimeterDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'num_separate_areas': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Zone']"}),
            'zoneArea': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'zonePerimeter': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'Results.dailybyzoneandproductiontype': {
            'Meta': {'object_name': 'DailyByZoneAndProductionType'},
            'animalDaysInZone': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']"}),
            'unitDaysInZone': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'unitsInZone': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Zone']"})
        },
        'Results.dailycontrols': {
            'Meta': {'object_name': 'DailyControls'},
            'adqcU': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'adqnU': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'average_prevalence': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'costSurveillance': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'costsTotal': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'outbreakDuration': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
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
            'Meta': {'object_name': 'DailyReport'},
            'full_line': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'Meta': {'object_name': 'DestructionGroup'},
            'Ring': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Unsp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            '_blank': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.detectionbracketgroup': {
            'Clin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'DetectionBracketGroup'},
            'Test': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            '_blank': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.detectiongroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AClin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ATest': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'DetectionGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UClin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTest': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.spreadgroup': {
            'AAir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AInd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'SpreadGroup'},
            'UAir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UInd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.stategroup': {
            'AClin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADest': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ALat': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ANImm': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ASubc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ASusc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AVImm': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'StateGroup'},
            'UClin': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDest': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ULat': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UNImm': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'USubc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'USusc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UVImm': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.testoutcomegroup': {
            'Meta': {'object_name': 'TestOutcomeGroup'},
            'UFalseNeg': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UFalsePos': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTrueNeg': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTruePos': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.testtriggergroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADet': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADirBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADirFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AIndBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AIndFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ARing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'TestTriggerGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDet': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDirBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDirFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UIndBack': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UIndFwd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'URing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.tracegroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AAllp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADirp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AInd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AIndp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'TraceGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UAllp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDir': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDirp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UInd': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UIndp': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.vaccinationgroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AIni': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ARing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'VaccinationGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UIni': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'URing': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.waitgroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'ADaysInQueue': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'AMaxDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'Meta': {'object_name': 'WaitGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UDaysInQueue': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UMaxDay': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTimeAvg': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'UTimeMax': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ScenarioCreator.productiontype': {
            'Meta': {'object_name': 'ProductionType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'ScenarioCreator.zone': {
            'Meta': {'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone_description': ('django.db.models.fields.TextField', [], {}),
            'zone_radius': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['Results']