from collections import defaultdict
import copy
from itertools import product


explanations = {'A': 'Animals',
            'U': 'Units',
            'n': 'New',
            'c': 'Cumulative',
            'w': 'Wait',
            'adq': 'Adequate Exposures',
            'Clin': 'from Clinical signs',  # This gets overridden by 'Clinical' below... not a big deal, but not perfect
            'Test': 'from Lab Tests',
            'p': 'Possible',
            'Dir': '- Direct Contact',
            'Ind': '- Indirect Contact',
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
            'tst': 'Lab Test',
            'tstcA': 'Lab Tests Cumulative Animals',
            'vac': 'Vaccinations',
            'vacw': 'Vaccination Wait Time',
            'inf': 'Infection',
            '': 'For Any Reason',  # TODO: Not sure about how to handle this since `'' in 'app'` == True 
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
# explanations = defaultdict(lambda: '', tmp_dict)

#For DailyByProductionType model only
grammars = {'exp': [('c', 'n'), ('U', 'A'), ('', 'Dir', 'Ind', 'Air')],
            'adq': [('c', 'n'), ('U', ), ('', 'Dir', 'Ind', 'Air')],
            'firstDetection': [('', 'Clin', 'Test')],
            'lastDetection': [('', 'Clin', 'Test')],
            'det': [('c', 'n'), ('U', 'A'), ('', 'Clin', 'Test')],
            'tr': [('n', 'c'), ('U', 'A'), ('', 'Dir', 'Ind'), ('', 'p')],
            'exm': [('n', 'c'), ('U', 'A'), ('', 'Ring', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack', 'Det')],
            'tst': [('n', 'c'), ('U', ), ('', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack', 'TruePos', 'FalsePos', 'TrueNeg', 'FalseNeg')],
            'tstcA': [('', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack')],
            'firstVaccination': [('', 'Ring')],
            'vacw': [('U', 'A'), ('', 'Max', 'MaxDay', 'TimeMax', 'TimeAvg', 'DaysInQueue')],
            'vac': [('n', 'c'), ('U', 'A'), ('', 'Ini', 'Ring')],
            'firstDestruction': [('', 'Ring', 'Det', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack')],
            'des': [('n', 'c'), ('U', 'A'), ('', 'Ring', 'Det', 'Ini', 'DirFwd', 'IndFwd', 'DirBack', 'IndBack')],
            'tsd': [('U', 'A'), ('Susc', 'Lat', 'Subc', 'Clin', 'NImm', 'VImm', 'Dest')],
            'inf': [('c', 'n'), ('U', 'A'), ('', 'Ini', 'Dir', 'Ind', 'Air')],
            'desw': [('U', 'A')],
}

DailyControls = {'desw': [('U', 'A'), ('Max', 'MaxDay', 'TimeMax', 'TimeAvg', 'DaysInQueue'), ]}

ZONES = ('Background', 'HighRisk', 'MediumRisk')
PT = ('', 'Cattle', 'Swine')
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
    for piece in grammar:
        for option in sorted(piece, key=len, reverse=True):  # this puts the empty string as the last possibility
            if field_name.startswith(option):
                field_name, explanation = push_explanation(field_name, option, explanation)
                break  # go up on for loop level
    return ' '.join(explanation)
