# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column(u'Results_dailybyproductiontype', u'vaccUAll', u'vaccU')
        db.rename_column(u'Results_dailybyproductiontype', u'descAAll', u'descA')
        db.rename_column(u'Results_dailybyproductiontype', u'detcUAll', u'detcU')
        db.rename_column(u'Results_dailybyproductiontype', u'tstnUAll', u'tstnU')
        db.rename_column(u'Results_dailybyproductiontype', u'vacnAAll', u'vacnA')
        db.rename_column(u'Results_dailybyproductiontype', u'vacwAAll', u'vacwA')
        db.rename_column(u'Results_dailybyproductiontype', u'exmnUAll', u'exmnU')
        db.rename_column(u'Results_dailybyproductiontype', u'trcUAll', u'trcU')
        db.rename_column(u'Results_dailybyproductiontype', u'detnUAll', u'detnU')
        db.rename_column(u'Results_dailybyproductiontype', u'trcAAll', u'trcA')
        db.rename_column(u'Results_dailybyproductiontype', u'vaccAAll', u'vaccA')
        db.rename_column(u'Results_dailybyproductiontype', u'desnUAll', u'desnU')
        db.rename_column(u'Results_dailybyproductiontype', u'vacnUAll', u'vacnU')
        db.rename_column(u'Results_dailybyproductiontype', u'trcUAllp', u'trcUp')
        db.rename_column(u'Results_dailybyproductiontype', u'desnAAll', u'desnA')
        db.rename_column(u'Results_dailybyproductiontype', u'trnAAllp', u'trnAp')
        db.rename_column(u'Results_dailybyproductiontype', u'tstcAAll', u'tstcA')
        db.rename_column(u'Results_dailybyproductiontype', u'exmcUAll', u'exmcU')
        db.rename_column(u'Results_dailybyproductiontype', u'trnAAll', u'trnA')
        db.rename_column(u'Results_dailybyproductiontype', u'tstcUAll', u'tstcU')
        db.rename_column(u'Results_dailybyproductiontype', u'trnUAll', u'trnU')
        db.rename_column(u'Results_dailybyproductiontype', u'detcAAll', u'detcA')
        db.rename_column(u'Results_dailybyproductiontype', u'descUAll', u'descU')
        db.rename_column(u'Results_dailybyproductiontype', u'trcAAllp', u'trcAp')
        db.rename_column(u'Results_dailybyproductiontype', u'detnAAll', u'detnA')
        db.rename_column(u'Results_dailybyproductiontype', u'trnUAllp', u'trnUp')
        db.rename_column(u'Results_dailybyproductiontype', u'exmnAAll', u'exmnA')
        db.rename_column(u'Results_dailybyproductiontype', u'exmcAAll', u'exmcA')
        db.rename_column(u'Results_dailybyproductiontype', u'vacwUAll', u'vacwU')


        db.rename_column(u'Results_dailycontrols', u'detcUqAll', u'detcUq')
        db.rename_column(u'Results_dailycontrols', u'firstDetUInfAll', u'firstDetUInf')
        db.rename_column(u'Results_dailycontrols', u'adqcUAll', u'adqcU')
        db.rename_column(u'Results_dailycontrols', u'adqnUAll', u'adqnU')
        db.rename_column(u'Results_dailycontrols', u'firstDetAInfAll', u'firstDetAInf')




    def backwards(self, orm):
        db.rename_column(u'Results_dailybyproductiontype', u'vaccU', u'vaccUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'descA', u'descAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'detcU', u'detcUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'tstnU', u'tstnUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'vacnA', u'vacnAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'vacwA', u'vacwAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'exmnU', u'exmnUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'trcU', u'trcUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'detnU', u'detnUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'trcA', u'trcAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'vaccA', u'vaccAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'desnU', u'desnUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'vacnU', u'vacnUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'trcUp', u'trcUAllp')
        db.rename_column(u'Results_dailybyproductiontype', u'desnA', u'desnAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'trnAp', u'trnAAllp')
        db.rename_column(u'Results_dailybyproductiontype', u'tstcA', u'tstcAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'exmcU', u'exmcUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'trnA', u'trnAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'tstcU', u'tstcUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'trnU', u'trnUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'detcA', u'detcAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'descU', u'descUAll')
        db.rename_column(u'Results_dailybyproductiontype', u'trcAp', u'trcAAllp')
        db.rename_column(u'Results_dailybyproductiontype', u'detnA', u'detnAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'trnUp', u'trnUAllp')
        db.rename_column(u'Results_dailybyproductiontype', u'exmnA', u'exmnAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'exmcA', u'exmcAAll')
        db.rename_column(u'Results_dailybyproductiontype', u'vacwU', u'vacwUAll')

        db.rename_column(u'Results_dailycontrols', u'detcUq', u'detcUqAll')
        db.rename_column(u'Results_dailycontrols', u'firstDetUInf', u'firstDetUInfAll')
        db.rename_column(u'Results_dailycontrols', u'adqcU', u'adqcUAll')
        db.rename_column(u'Results_dailycontrols', u'adqnU', u'adqnUAll')
        db.rename_column(u'Results_dailycontrols', u'firstDetAInf', u'firstDetAInfAll')


    models = {
        u'Results.dailybyproductiontype': {
            'Meta': {'object_name': 'DailyByProductionType'},
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descADet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descADirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descADirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descAIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descAIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descAIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descARing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descAUnsp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descUDet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descUDirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descUDirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descUIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descUIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descUIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descURing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descUUnsp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnADet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnADirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnADirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnAIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnAIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnAIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnARing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnAUnsp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnUDet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnUDirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnUDirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnUIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnUIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnUIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnURing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'desnUUnsp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detcA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detcAClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detcATest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detcU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detcUClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detcUTest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detnA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detnAClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detnATest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detnU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detnUClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detnUTest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcADet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcADirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcADirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcAIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcAIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcARing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcUDet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcUDirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcUDirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcUIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcUIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmcURing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnADet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnADirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnADirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnAIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnAIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnARing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnUDet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnUDirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnUDirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnUIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnUIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exmnURing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expcA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expcAAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expcADir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expcAInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expcU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expcUAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expcUDir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expcUInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expnA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expnAAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expnADir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expnAInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expnU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expnUAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expnUDir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expnUInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDestruction': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDestructionDet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDestructionDirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDestructionDirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDestructionIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDestructionIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDestructionIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDestructionRing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDestructionUnsp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDetection': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDetectionClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDetectionTest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstVaccination': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstVaccinationRing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infcA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infcAAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infcADir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infcAInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infcAIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infcU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infcUAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infcUDir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infcUInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infcUIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnAAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnADir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnAInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnAIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnUAir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnUDir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnUInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'infnUIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lastDetection': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lastDetectionClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lastDetectionTest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ScenarioCreator.ProductionType']", 'null': 'True', 'blank': 'True'}),
            'trcA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcADir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcADirp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcAInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcAIndp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcAp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcUDir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcUDirp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcUInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcUIndp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trcUp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnADir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnADirp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnAInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnAIndp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnAp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnUDir': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnUDirp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnUInd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnUIndp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trnUp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdAClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdADest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdALat': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdANImm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdASubc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdASusc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdAVImm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdUClin': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdUDest': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdULat': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdUNImm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdUSubc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdUSusc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tsdUVImm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcADirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcADirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcAIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcAIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcUDirBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcUDirFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcUFalseNeg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcUFalsePos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcUIndBack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcUIndFwd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcUTrueNeg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstcUTruePos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstnU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstnUFalseNeg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstnUFalsePos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstnUTrueNeg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tstnUTruePos': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccAIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccARing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccUIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccURing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacnA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacnAIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacnARing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacnU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacnUIni': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacnURing': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwA': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vacwADaysInQueue': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vacwAMax': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vacwAMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwATimeAvg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vacwATimeMax': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vacwU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUDaysInQueue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUTimeAvg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vacwUTimeMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'Results.dailybyzone': {
            'Meta': {'object_name': 'DailyByZone'},
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'finalZoneArea': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'finalZonePerimeter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maxZoneArea': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'maxZoneAreaDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maxZonePerimeter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'maxZonePerimeterDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'numSeparateAreas': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ScenarioCreator.Zone']", 'null': 'True', 'blank': 'True'}),
            'zoneArea': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'zonePerimeter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'Results.dailybyzoneandproductiontype': {
            'Meta': {'object_name': 'DailyByZoneAndProductionType'},
            'animalDaysInZone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ScenarioCreator.ProductionType']", 'null': 'True', 'blank': 'True'}),
            'unitDaysInZone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unitsInZone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ScenarioCreator.Zone']", 'null': 'True', 'blank': 'True'})
        },
        u'Results.dailycontrols': {
            'Meta': {'object_name': 'DailyControls'},
            'adqcU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'adqnU': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'averagePrevalence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'costSurveillance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'costsTotal': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destrAppraisal': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'destrCleaning': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'destrDisposal': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'destrEuthanasia': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'destrIndemnification': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'destrOccurred': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'destrSubtotal': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'deswADaysInQueue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswAMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswAMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswATimeAvg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'deswATimeMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswUDaysInQueue': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswUMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswUMaxDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deswUTimeAvg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'deswUTimeMax': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detOccurred': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'detcUq': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'diseaseDuration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDetAInf': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'firstDetUInf': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outbreakDuration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ratio': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccOccurred': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vaccSetup': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vaccSubtotal': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vaccVaccination': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'Results.dailyreport': {
            'Meta': {'object_name': 'DailyReport'},
            'full_line': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sparse_dict': ('django.db.models.fields.TextField', [], {})
        },
        u'Results.unitstats': {
            'Meta': {'object_name': 'UnitStats'},
            'cumulative_destroyed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cumulative_infected': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cumulative_vaccinated': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'cumulative_zone_focus': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unit': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ScenarioCreator.Unit']", 'unique': 'True'})
        },
        u'ScenarioCreator.population': {
            'Meta': {'object_name': 'Population'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_file': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'ScenarioCreator.productiontype': {
            'Meta': {'object_name': 'ProductionType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'ScenarioCreator.unit': {
            'Meta': {'object_name': 'Unit'},
            '_population': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ScenarioCreator.Population']"}),
            'days_in_initial_state': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'days_left_in_initial_state': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'initial_state': ('django.db.models.fields.CharField', [], {'default': "u'S'", 'max_length': '255'}),
            'latitude': ('django_extras.db.models.fields.LatitudeField', [], {}),
            'longitude': ('django_extras.db.models.fields.LongitudeField', [], {}),
            'production_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ScenarioCreator.ProductionType']"}),
            'user_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'ScenarioCreator.zone': {
            'Meta': {'object_name': 'Zone'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'radius': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['Results']