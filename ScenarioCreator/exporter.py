import os
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
        os.mkdir(workspace_path(scenario_filename() + "\\Exports\\"))
    except FileExistsError:
        pass
    file = open(workspace_path(scenario_filename() + "\\Exports\\") + "REL_" + scenario_filename().replace(" ", "") + ".csv", "w")
    # for all of the functions
    for function in functions:
        # for each of the export keys for each relational function
        for key in RelationalFunction.export_fields:
            # try to write it, if this fails it is due to a NULL field and we pass
            try:
                file.write(str(getattr(function, key)) + ",")
            except AttributeError:
                pass
        # for each point in ALL points
        for point_set in points:
            # if this point set belongs to the current function
            if point_set.relational_function == function:
                # for x and y in the points
                for key in RelationalPoint.export_fields:
                    # try to write that values, if this fails it is due to a NULL field and we pass
                    try:
                        file.write(str(getattr(point_set, key)) + ",")
                    except AttributeError:
                        pass
        # current function output complete, write a newline before the next function is output
        file.write("\n")
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
        os.mkdir(workspace_path(scenario_filename() + "\\Exports\\"))
    except FileExistsError:
        pass
    file = open(workspace_path(scenario_filename() + "\\Exports\\") + "PDF_" + scenario_filename().replace(" ", "") + ".csv", "w")
    # for each of the existing pdfs
    for function in functions:
        # for each key we need to output
        for key in ProbabilityDensityFunction.export_fields:
            # try to write that value, if this fails it is due to a NULL field and we pass
            try:
                file.write(str(getattr(function, key)) + ",")
            except AttributeError:
                pass
            # write a newline before the next function
        file.write("\n")
    # close the file to save and avoid corruption
    file.close()
    return
