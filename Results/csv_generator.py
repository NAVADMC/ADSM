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