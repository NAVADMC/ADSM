# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DailyByZone.zone'
        db.alter_column('Results_dailybyzone', 'zone_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone'], null=True))

        # Changing field 'DailyByZoneAndProductionType.production_type'
        db.alter_column('Results_dailybyzoneandproductiontype', 'production_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'], null=True))

        # Changing field 'DailyByZoneAndProductionType.zone'
        db.alter_column('Results_dailybyzoneandproductiontype', 'zone_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone'], null=True))

        # Changing field 'DailyByProductionType.production_type'
        db.alter_column('Results_dailybyproductiontype', 'production_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'DailyByZone.zone'
        raise RuntimeError("Cannot reverse this migration. 'DailyByZone.zone' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'DailyByZone.zone'
        db.alter_column('Results_dailybyzone', 'zone_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone']))

        # User chose to not deal with backwards NULL issues for 'DailyByZoneAndProductionType.production_type'
        raise RuntimeError("Cannot reverse this migration. 'DailyByZoneAndProductionType.production_type' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'DailyByZoneAndProductionType.production_type'
        db.alter_column('Results_dailybyzoneandproductiontype', 'production_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType']))

        # User chose to not deal with backwards NULL issues for 'DailyByZoneAndProductionType.zone'
        raise RuntimeError("Cannot reverse this migration. 'DailyByZoneAndProductionType.zone' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'DailyByZoneAndProductionType.zone'
        db.alter_column('Results_dailybyzoneandproductiontype', 'zone_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.Zone']))

        # User chose to not deal with backwards NULL issues for 'DailyByProductionType.production_type'
        raise RuntimeError("Cannot reverse this migration. 'DailyByProductionType.production_type' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'DailyByProductionType.production_type'
        db.alter_column('Results_dailybyproductiontype', 'production_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ScenarioCreator.ProductionType']))

    models = {
        'Results.dailybyproductiontype': {
            'Meta': {'object_name': 'DailyByProductionType'},
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descA': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.DestructionGroup']", 'blank': 'True'}),
            'descU': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.DestructionGroup']", 'blank': 'True'}),
            'desw': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.WaitGroup']", 'blank': 'True'}),
            'det': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.DetectionGroup']", 'blank': 'True'}),
            'exm': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.TestTriggerGroup']", 'blank': 'True'}),
            'exp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.SpreadGroup']", 'blank': 'True'}),
            'firstDestruction': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.DestructionGroup']", 'blank': 'True'}),
            'firstDetection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.DetectionBracketGroup']", 'blank': 'True'}),
            'firstVaccination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstVaccinationRing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inf': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.SpreadGroup']", 'blank': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lastDetection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.DetectionBracketGroup']", 'blank': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'null': 'True', 'blank': 'True'}),
            'tr': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.TraceGroup']", 'blank': 'True'}),
            'tsd': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.StateGroup']", 'blank': 'True'}),
            'tst': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.TestOutcomeGroup']", 'blank': 'True'}),
            'tstc': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.TestTriggerGroup']", 'blank': 'True'}),
            'vac': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.VaccinationGroup']", 'blank': 'True'}),
            'vacw': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['Results.WaitGroup']", 'blank': 'True'})
        },
        'Results.dailybyzone': {
            'Meta': {'object_name': 'DailyByZone'},
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'finalZoneArea': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'finalZonePerimeter': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maxZoneArea': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maxZoneAreaDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maxZonePerimeter': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maxZonePerimeterDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_separate_areas': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Zone']", 'null': 'True', 'blank': 'True'}),
            'zoneArea': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zonePerimeter': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'Results.dailybyzoneandproductiontype': {
            'Meta': {'object_name': 'DailyByZoneAndProductionType'},
            'animalDaysInZone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.ProductionType']", 'null': 'True', 'blank': 'True'}),
            'unitDaysInZone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unitsInZone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ScenarioCreator.Zone']", 'null': 'True', 'blank': 'True'})
        },
        'Results.dailycontrols': {
            'Meta': {'object_name': 'DailyControls'},
            'adqcUAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'adqnUAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'average_prevalence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'costSurveillance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'costsTotal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destrAppraisal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destrCleaning': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destrDisposal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destrEuthanasia': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destrIndemnification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destrOccurred': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destrSubtotal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswADaysInQueue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswAMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswAMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswUDaysInQueue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswUMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswUMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswUTimeAvg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswUTimeMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detOccurred': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detcUqAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'diseaseDuration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDetAInfAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDetUInfAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outbreakDuration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ratio': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccOccurred': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccSetup': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccSubtotal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccVaccination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwADaysInQueue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwAMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwAMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUDaysInQueue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUTimeAvg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUTimeMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'Results.dailyreport': {
            'Meta': {'object_name': 'DailyReport'},
            'full_line': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sparse_dict': ('django.db.models.fields.TextField', [], {})
        },
        'Results.destructiongroup': {
            'All': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Det': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'DirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'DirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'IndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'IndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Ini': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'DestructionGroup'},
            'Ring': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Unsp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_blank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.detectionbracketgroup': {
            'Clin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'DetectionBracketGroup'},
            'Test': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_blank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.detectiongroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ATest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'DetectionGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UTest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.spreadgroup': {
            'AAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ADir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'SpreadGroup'},
            'UAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UDir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.stategroup': {
            'AClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ADest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ALat': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ANImm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ASubc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ASusc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AVImm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'StateGroup'},
            'UClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UDest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ULat': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UNImm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'USubc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'USusc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UVImm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.testoutcomegroup': {
            'Meta': {'object_name': 'TestOutcomeGroup'},
            'UFalseNeg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UFalsePos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UTrueNeg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UTruePos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.testtriggergroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ADet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ADirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ADirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ARing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'TestTriggerGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UDet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UDirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UDirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'URing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.tracegroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AAllp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ADir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ADirp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AIndp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'TraceGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UAllp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UDir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UDirp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UIndp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.vaccinationgroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ARing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'VaccinationGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'URing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Results.waitgroup': {
            'AAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ADaysInQueue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'AMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'WaitGroup'},
            'UAll': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UDaysInQueue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UTimeAvg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'UTimeMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ScenarioCreator.productiontype': {
            'Meta': {'object_name': 'ProductionType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'ScenarioCreator.zone': {
            'Meta': {'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'radius': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['Results']