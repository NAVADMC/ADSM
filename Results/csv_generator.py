import multiprocessing
import csv

from django.conf import settings

from ADSMSettings.utils import workspace_path, scenario_filename


def create_csv_file(location, headers, data):
    csvfile = open(location, 'wb')
    writer = csv.writer(csvfile)

    writer.writerow(headers)

    [writer.writerow(x) for x in data]

    csvfile.close()


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
        headers, data = "test1, test2", ["1blah1, 1blah2", "2blah1, 2blah2"]  # TODO: Use class method to get these

        create_csv_file(location, headers, data)

    def get_summary_data_table(self):
        """Generates a python data structure with all the information for the CSV file.  Structured in a list[row][column] 2D array that mimics the spreadsheet
        layout and follows the column order.  This could be changed to an OrderedDict( OrderedDict<column, value> ) if you want more flexibility in storage
        and retreival, but it's simplest to just calculate and store them in order."""
        from Results.models import DailyByProductionType
        fields_of_interest = [] # only cumulative, last day fields in DailyByProductionType for all production types
        DailyByProductionType.objects.filter(last_day=True, production_type__isnull=True, )
        for field, val in DailyByProductionType():
            if 'c' in field:
                fields_of_interest.append(field)


        pass