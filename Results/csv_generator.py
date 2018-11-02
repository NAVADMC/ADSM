import multiprocessing
import math
import csv

from django.conf import settings
from django.db import connections, OperationalError
from django.db.models import Avg, Min, Max
from math import sqrt
from statistics import pstdev

from ADSMSettings.utils import workspace_path, scenario_filename
from Results.models import DailyControls
from Results.output_grammar import explain


SUMMARY_FILE_NAME = 'Summary.csv'


def create_csv_file(location, headers, data):
    with open(location, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        writer.writeheader()
        for x in data:
            writer.writerow(x)


def django_percentile(field_name, query_set, cutoff_percentile, count):
    index = int((count - 1) * (cutoff_percentile / 100))
    model_instance = query_set.order_by(field_name)[index]
    return getattr(model_instance, field_name)


class SummaryCSVGenerator(multiprocessing.Process):
    import django
    django.setup()

    testing = False

    def __init__(self, testing=False, **kwargs):
        super(SummaryCSVGenerator, self).__init__(**kwargs)
        self.testing = testing

    def run(self):
        if self.testing:
            for database in settings.DATABASES:
                settings.DATABASES[database]['NAME'] = settings.DATABASES[database]['TEST']['NAME'] if 'TEST' in settings.DATABASES[database] else settings.DATABASES[database]['TEST_NAME']

        location = workspace_path(scenario_filename() + '/' + "Supplemental Output Files" + '/' + SUMMARY_FILE_NAME)  # Note: scenario_filename uses the database
        headers, data = self.get_summary_data_table()

        create_csv_file(location, headers, data)


    def get_summary_data_table(self):
        """Generates a python data structure with all the information for the CSV file.  Structured in a list[row][column] 2D array that mimics the spreadsheet
        layout and follows the column order.  This could be changed to an OrderedDict( OrderedDict<column, value> ) if you want more flexibility in storage
        and retrieval, but it's simplest to just calculate and store them in order."""
        from Results.models import DailyByProductionType
        headers = ['Field Name', 'Explanation', 'Mean', 'StdDev', 'Low', 'High', 'p5', 'p25', 'p50', 'p75', 'p95']
        data = []  # 2D

        fields_of_interest = [field for field, val in DailyByProductionType() if 'Cumulative' in explain(field)]  # only cumulative, last day fields in DailyByProductionType for all production types
        grab_pt = 'infcUIni infcAIni infcUAir infcAAir infcUDir infcADir infcUInd infcAInd expcUDir expcADir expcUInd expcAInd detcUClin detcAClin detcUTest detcATest descUIni descAIni descUDet descADet descUDirFwd descADirFwd descUIndFwd descAIndFwd descUDirBack descADirBack descUIndBack descAIndBack descURing descARing vaccUIni vaccAIni vaccURing vaccARing vacwUMax vacwAMax vacwUMaxDay vacwAMaxDay vacwUTimeMax vacwUTimeAvg exmcUDirFwd exmcADirFwd exmcUIndFwd exmcAIndFwd exmcUDirBack exmcADirBack exmcUIndBack exmcAIndBack tstcUDirFwd tstcADirFwd tstcUIndFwd tstcAIndFwd tstcUDirBack tstcADirBack tstcUIndBack tstcAIndBack tstcUTruePos tstcUTrueNeg tstcUFalsePos tstcUFalseNeg firstDetection lastDetection firstVaccination firstDestruction tsdUSusc tsdASusc tsdULat tsdALat tsdUSubc tsdASubc tsdUClin tsdAClin tsdUNImm tsdANImm tsdUVImm tsdAVImm tsdUDest tsdADest'.split()
        query_set = DailyByProductionType.objects.filter(last_day=True, production_type__isnull=True, )
        count = query_set.count()  # only needs to be evaluated once per model
        for field_name in set().union(grab_pt, fields_of_interest):
            data.append(self.summary_row(field_name, query_set, headers, count))

        grab_controls = 'deswUMax deswAMax deswUMaxDay deswAMaxDay deswUTimeMax deswUTimeAvg deswUDaysInQueue deswADaysInQueue detOccurred firstDetUInf firstDetAInf vaccOccurred destrOccurred diseaseDuration outbreakDuration'.split()
        query_set = DailyControls.objects.filter(last_day=True)
        count = query_set.count()  # only needs to be evaluated once per model
        for field_name in grab_controls:
            data.append(self.summary_row(field_name, query_set, headers, count))

        # TODO: These are field names mentioned in the original NAADSM file that I have not yet accounted for
        unaccounted_for = 'infcUAll infcAAll expcUAll expcAAll trcUDirFwd trcADirFwd trcUIndFwd trcAIndFwd trcUDirpFwd trcADirpFwd trcUIndpFwd trcAIndpFwd trcUDirBack trcADirBack trcUIndBack trcAIndBack trcUDirpBack trcADirpBack trcUIndpBack trcAIndpBack trcUDirAll trcADirAll trcUIndAll trcAIndAll trcUAll trcAAll tocUDirFwd tocUIndFwd tocUDirBack tocUIndBack tocUDirAll tocUIndAll tocUAll detcUAll detcAAll descUAll descAAll vaccUAll vaccAAll exmcUDirAll exmcADirAll exmcUIndAll exmcAIndAll exmcUAll exmcAAll tstcUDirAll tstcADirAll tstcUIndAll tstcAIndAll tstcUAll tstcAAll tstcATruePos tstcATrueNeg tstcAFalsePos tstcAFalseNeg zoncFoci diseaseEnded outbreakEnded'.split()

        return headers, data


    def summary_row(self, field_name, query_set, headers, count):

        resolvers = {'Field Name': lambda field, query: field_name,
                     'Explanation': lambda field, query: explain(field_name),
                     'Mean': lambda field, query: query.aggregate(Avg(field)).popitem()[1],  # grabs value
                     'StdDev': std_dev,
                     'Low': lambda field, query: query.aggregate(Min(field)).popitem()[1],  # grabs value
                     'High': lambda field, query: query.aggregate(Max(field)).popitem()[1],  # grabs value
                     'p5': lambda field, query:  django_percentile(field, query, 5, count),
                     'p25': lambda field, query: django_percentile(field, query, 25, count),
                     'p50': lambda field, query: django_percentile(field, query, 50, count),
                     'p75': lambda field, query: django_percentile(field, query, 75, count),
                     'p95': lambda field, query: django_percentile(field, query, 95, count),
        }
        row = {}
        for column in headers:
            if column in resolvers.keys():
                row[column] = resolvers[column](field_name, query_set)
            else:
                raise NotImplemented("The column name " + column + " does not have a function associated with it.")

        return row


def std_dev(field, query):
    """This is the __Population__ Standard Deviation formula translated into RAW SQL statement, specifically SQLite version."""
    #TODO: try/except for whole column

    #get next table name based on given query
    table_name = query.model._meta.db_table
    cursor = connections["scenario_db"].cursor()

    #two statements, one is for tables that have production_type_id and one for tables that dont
    # try and use the query for tables with production_type_id, if that fails use the other query
    try:
        last_day_vals = "SELECT {field} FROM {table} WHERE last_day = 1 and production_type_id is null".format(table=table_name, field=field)
        cursor.execute(last_day_vals)
    except OperationalError:
        last_day_vals = "SELECT {field} FROM {table} WHERE last_day = 1".format(table=table_name, field=field)
        cursor.execute(last_day_vals)

    row = cursor.fetchall()

    #every value in the query return that is an integer to a list, these are the values used in calculation
    values = [element[0] for element in row if isinstance(element[0], int)]

    if values:
        #return the standard deviation
        return round(pstdev(values), 2)
    else:
        return 0
