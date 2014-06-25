from Results.models import DailyReport
from ast import literal_eval


def populate_db_from_daily_report(report):
    """Parses the C Engine stdout and populates the appropriate models with the information.  Takes one line
    at a time, representing one DailyReport."""
    assert isinstance(report, DailyReport)
    sparse_info = literal_eval(report.sparse_dict)
    for name, value in sparse_info.items():
        print(name, value)