import os
import csv
from ADSMSettings.utils import workspace_path, scenario_filename
from ScenarioCreator.models import ProbabilityDensityFunction, RelationalFunction, RelationalPoint


def export_relational_functions(functions, points):
    '''
    Export the existing relational functions.

    Relational functions are exported with their points.

    :param functions: existing relational functions
    :param points: all of the relational point objects, these must be matched to functions before being exported
    :return: None
    '''
    # open and erase or create the export file
    try:
        os.makedirs(workspace_path("\\Exports\\Exported Functions\\"))
    except FileExistsError:
        pass
    file = open(workspace_path("\\Exports\\Exported Functions\\") + "REL_" + scenario_filename().replace(" ", "") + ".csv", "w")
    csvwriter = csv.writer(file, delimiter=",", quotechar='¿', quoting=csv.QUOTE_ALL)
    # for all of the functions
    for function in functions:
        next_func = [str(getattr(function, key)) for key in RelationalFunction.export_fields]
        for point_set in points:
            if point_set.relational_function == function:
                next_func += [str(getattr(point_set, key)) for key in RelationalPoint.export_fields]
        csvwriter.writerow(next_func)
    # close the file to save and avoid corruption
    file.close()
    return


def export_pdfs(functions):
    '''
    Export the probability density functions

    :param functions: The existing pdfs
    :return: None
    '''
    # Open and erase or create the output file
    try:
        os.makedirs(workspace_path("\\Exports\\Exported Functions\\"))
    except FileExistsError:
        pass
    file = open(workspace_path("\\Exports\\Exported Functions\\") + "PDF_" + scenario_filename().replace(" ", "") + ".csv", "w")
    csvwriter = csv.writer(file, delimiter=",", quotechar='¿', quoting=csv.QUOTE_ALL)
    # for each of the existing pdfs
    for function in functions:
        # for each key we need to output
        csvwriter.writerow([str(getattr(function, key)) for key in ProbabilityDensityFunction.export_fields])
    # close the file to save and avoid corruption
    file.close()
    return
