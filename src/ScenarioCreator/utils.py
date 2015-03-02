import itertools

__author__ = 'Josiah'


def lowercase_header(iterator):
    """Source: http://stackoverflow.com/questions/16937457/python-dictreader-how-to-make-csv-column-names-lowercase"""
    return itertools.chain([next(iterator).lower()], iterator)

