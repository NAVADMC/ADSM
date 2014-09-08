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
            'DirFwd': 'because of Direct Forward Trace',
            'IndFwd': 'because of Indirect Forward Trace',
            'DirBack': 'because of Direct Back Trace',
            'IndBack': 'because of Indirect Back Trace',
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
explanations = defaultdict(lambda: '', tmp_dict)

#For DailyByProductionType model only
grammars = {'exp': [('c', 'n'), ('U', 'A'), ('', 'Dir', 'Ind', 'Air'), ('All', 'Cattle', 'Swine')],
            'firstDetection': [('', 'Clin', 'Test'), ('', 'Cattle', 'Swine')],
            'lastDetection': [('', 'Clin', 'Test'), ('', 'Cattle', 'Swine')],
            'det': [('c', 'n'), ('U', 'A'), ('All', 'Clin', 'Test'), ('', 'Cattle', 'Swine')],
            'tr': [('n', 'c'), ('U', 'A'), ('All', 'Dir', 'Ind'), ('', 'p'), ('', 'Cattle', 'Swine')],
            'exm': [('n', 'c'), ('U', 'A'), ('All', 'Ring', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack', 'Det'), ('', 'Cattle', 'Swine')],
            'tstnU': [('All', 'TruePos', 'FalsePos', 'TrueNeg', 'FalseNeg'), ('', 'Cattle', 'Swine')],
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
}

DailyControls = {'desw': [('U', 'A'), ('Max', 'MaxDay', 'TimeMax', 'TimeAvg', 'DaysInQueue'), ]}

ZONES = ('Background', 'HighRisk', 'MediumRisk')
PT = ('', 'Cattle', 'Swine')
PT_All = ('All', 'Cattle', 'Swine')
DailyByZoneAndProductionType = {'animalDaysInZone': [ZONES, PT],
                                'unitDaysInZone': [ZONES, PT],
                                'unitsInZone': [ZONES, PT]}


def push_explanation(field_name, start, explanation=None):
    if not explanation:
        explanation = []
    explanation.append(explanations[start])
    return field_name.replace(start, '', 1), explanation


def explain(field_name):
    """Recursively breaks a field name down into parts and explains each piece.  """
    start = sorted([k for k in grammars.keys() if field_name.startswith(k)], key=len)
    start = start[-1]  # last one is the longest
    grammar = grammars[start]
    field_name, explanation = push_explanation(field_name, start)
    for piece in grammar[:-1]:  # skip production type tuple at the end
        for option in sorted(piece, key=len, reverse=True):  # this puts the empty string as the last possibility
            if field_name.startswith(option):
                field_name, explanation = push_explanation(field_name, option, explanation)
                break  # go up on for loop level
    return ' '.join(explanation)
