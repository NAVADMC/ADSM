import multiprocessing
import csv

from django.conf import settings
from django.db.models import Avg, Min, Max
from ADSMSettings.utils import workspace_path, scenario_filename
from Results.output_grammar import explain


def create_csv_file(location, headers, data):
    with open(location, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        writer.writeheader()
        [writer.writerow(x) for x in data]


def django_percentile(field_name, query_set, cutoff_percentile, count):
    index = (count - 1) * (cutoff_percentile / 100)
    return query_set.order_by(field_name)[index]


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

        location = workspace_path(scenario_filename() + '/summary.csv')  # Note: scenario_filename uses the database
        headers, data = self.get_summary_data_table()

        create_csv_file(location, headers, data)


    def get_summary_data_table(self):
        """Generates a python data structure with all the information for the CSV file.  Structured in a list[row][column] 2D array that mimics the spreadsheet
        layout and follows the column order.  This could be changed to an OrderedDict( OrderedDict<column, value> ) if you want more flexibility in storage
        and retreival, but it's simplest to just calculate and store them in order."""
        from Results.models import DailyByProductionType
        fields_of_interest = [] # only cumulative, last day fields in DailyByProductionType for all production types
        query_set = DailyByProductionType.objects.filter(last_day=True, production_type__isnull=True, )
        count = query_set.count()  # only needs to be evaluated once
        for field, val in DailyByProductionType():
            if 'c' in field:
                fields_of_interest.append(field)
        headers = ['Field Name', 'Explanation', 'Mean', 'StdDev', 'Low', 'High', 'p5', 'p25', 'p50', 'p75', 'p95']
        data = []  # 2D

        for field_name in fields_of_interest:
            data.append(self.summary_row(field_name, query_set, headers, count))

        return ','.join(headers), data


    def summary_row(self, field_name, query_set, headers, count):

        resolvers = {'Field Name': lambda field, query: field_name,
                     'Explanation': lambda field, query: explain(field_name),
                     'Mean': lambda field, query: query.aggregate(Avg(field)),
                     'StdDev': lambda field, query: 1.0,
                     'Low': lambda field, query: query.aggregate(Min(field)),
                     'High': lambda field, query: query.aggregate(Max(field)),
                     'p5': lambda field, query: django_percentile(field, query, 5, count),
                     'p25': lambda field, query: django_percentile(field, query, 25, count),
                     'p50': lambda field, query: django_percentile(field, query, 50, count),
                     'p75': lambda field, query: django_percentile(field, query, 75, count),
                     'p95': lambda field, query: django_percentile(field, query, 95, count),
        }
        row = []
        for column in headers:
            if column in resolvers.keys():
                row.append(resolvers[column](field_name, query_set))
            else:
                raise NotImplemented("The column name " + column + " does not have a function associated with it.")

        return row







