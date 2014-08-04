from collections import defaultdict
import copy
from itertools import product


tmp_dict = {'A': 'Animals',
            'U': 'Units',
            'n': 'New',
            'c': 'Cumulative',
            'w': 'Wait',
            'Clin': 'from Clinical signs',  # This gets overridden by 'Clinical' below... not a big deal, but not perfect
            'Test': 'from Lab Tests',
            'p': 'Possible',
            'Dir': 'Direct Spread',
            'Ind': 'Indirect Spread',
            'Air': 'Airborne Spread',
            'des': 'Destruction',
            'desw': 'Destruction Wait Time',
            'det': 'Detection',
            'exm': 'Examination',
            'exp': 'Exposure',
            'firstDestruction': "First Destruction",
            'firstDetection': "First Detection",
            'firstVaccination': 'First Vaccination',
            'lastDetection': "Last Detection",
            'tr': 'Trace',
            'tsd': 'Transition State Daily',
            'tstcA': 'Lab Test Cumulative Animals',
            'tstcU': 'Lab Test Cumulative Units',
            'tstnU': 'Lab Test New Units',
            'vacc': 'Vaccination Cumulative',
            'vacn': 'Vaccination New',
            'vacw': 'Vaccination Wait Time',
            'inf': 'Infection',
            'All': 'For Any Reason',
            'Max': 'Max',
            'MaxDay': 'Day with Max',
            'TimeMax': 'Max Time',
            'TimeAvg': 'Average Time',
            'DaysInQueue': 'Days in Queue',
            'DirFwd': 'because of Direct Forward trace',
            'IndFwd': 'because of Indirect Forward trace',
            'DirBack': 'because of Direct Back trace',
            'IndBack': 'because of Indirect Back trace',
            'Ring': 'because of Ring',
            'Ini': 'Initially',
            'TruePos': 'True Positives',
            'FalsePos': 'False Positives',
            'TrueNeg': 'True Negatives',
            'FalseNeg': 'False Negatives',
            'Unsp': 'Unspecified',
            'Det': 'because of Detection',
            'Susc': 'Susceptible',
            'Lat': 'Latent',
            'Subc': 'Subclinical',
            'Clin': 'Clinical',
            'NImm': 'Natural Immune',
            'VImm': 'Vaccine Immune',
            'Dest': 'Destroyed',
}
explainations = defaultdict(lambda: '', tmp_dict)

#For DailyByProductionType model only
grammars = {'exp': [('c', 'n'), ('U', 'A'), ('', 'Dir', 'Ind', 'Air'), ('All', 'Cattle', 'Swine')],
            'firstDetection': [('', 'Clin', 'Test'), ('', 'Cattle', 'Swine')],
            'det': [('c', 'n'), ('U', 'A'), ('All', 'Clin', 'Test'), ('', 'Cattle', 'Swine')],
            'tr': [('n', 'c'), ('U', 'A'), ('All', 'Dir', 'Ind'), ('', 'p'), ('', 'Cattle', 'Swine')],
            'exm': [('n', 'c'), ('U', 'A'), ('All', 'Ring', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack', 'Det'), ('', 'Cattle', 'Swine')],
            'tstnU': [('TruePos', 'FalsePos', 'TrueNeg', 'FalseNeg'), ('', 'Cattle', 'Swine')],
            'tstcU': [('All', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack', 'TruePos', 'FalsePos', 'TrueNeg', 'FalseNeg'), ('', 'Cattle', 'Swine')],
            'tstcA': [('All', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack'), ('', 'Cattle', 'Swine')],
            'firstVaccination': [('', 'Ring'), ('', 'Cattle', 'Swine')],
            'vacw': [('U', 'A'), ('All', 'Max', 'MaxDay', 'TimeMax', 'TimeAvg', 'DaysInQueue'), ('', 'Cattle', 'Swine')],
            'vacn': [('U', 'A'), ('All', 'Ini', 'Ring'), ('', 'Cattle', 'Swine')],
            'vacc': [('U', 'A'), ('All', 'Ini', 'Ring'), ('', 'Cattle', 'Swine')],
            'firstDestruction': [('', 'Unsp', 'Ring', 'Det', 'Ini', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack'), ('', 'Cattle', 'Swine')],
            'des': [('n', 'c'), ('U', 'A'), ('All', 'Unsp', 'Ring', 'Det', 'Ini', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack'), ('', 'Cattle', 'Swine')],
            'tsd': [('U', 'A'), ('Susc', 'Lat', 'Subc', 'Clin', 'NImm', 'VImm', 'Dest'), ('', 'Cattle', 'Swine')],
            'inf': [('c', 'n'), ('U', 'A'), ('', 'Ini', 'Dir', 'Ind', 'Air'), ('All', 'Cattle', 'Swine')],
            'desw': [('U', 'A'), ('All', 'Cattle', 'Swine')],
            'exp': [('c', 'n'), ('U', 'A'), ('', 'Dir', 'Ind', 'Air'), ('', 'Cattle', 'Swine')],
}

DailyControls = {'desw': [('U', 'A'), ('Max', 'MaxDay', 'TimeMax', 'TimeAvg', 'DaysInQueue'), ]}

ZONES = ('Background', 'HighRisk', 'MediumRisk')
PT = ('', 'Cattle', 'Swine')
PT_All = ('All', 'Cattle', 'Swine')
DailyByZoneAndProductionType = {'animalDaysInZone': [ZONES, PT],
                                'unitDaysInZone': [ZONES, PT],
                                'unitsInZone': [ZONES, PT]}


def explain(field_name, explained_parts=None):
    """Recursively breaks a field name down into parts and explains each piece.  If you're having trouble
    with this method after adding new fields, you'll need to modify explanations{} to have longer prefixes,
    or modify this algorithm so that it doesn't shortcut down a dead end."""
    return ''
    if explained_parts is None:  # It's import you don't initialize this in the signature, it side-effects the result since [] is mutable
        explained_parts = []
    if not field_name:
        return ' '.join(explained_parts)

    if field_name in explainations.keys():  # shortcut the larger cases
        explained_parts.append(explainations[field_name])  # at the beginning
        return explain('', explained_parts)

    for suffix in explainations.keys():
        if field_name.startswith(suffix):
            explained_parts.append(explainations[suffix])  # at the beginning
            return explain(field_name[len(suffix) : ], explained_parts)
    #If we reach here it is because there's a string that couldn't be explained
    raise ValueError("Got a field name that doesn't match anything in explanations: %s, %s" % (str(explained_parts), str(field_name)))

