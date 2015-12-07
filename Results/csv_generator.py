import multiprocessing

from django.conf import settings


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

        # TODO: Generate the Statistics Summary Report CSV File

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