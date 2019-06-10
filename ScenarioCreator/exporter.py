from ADSMSettings.utils import workspace_path, scenario_filename
from ScenarioCreator.models import ProbabilityDensityFunction, RelationalFunction, RelationalPoint


def export_relational_functions(functions, points):
    file = open(workspace_path(scenario_filename() + "\\") + "REL_" + scenario_filename().replace(" ", "") + ".csv", "w")
    for function in functions:
        for key in RelationalFunction.export_fields:
            try:
                file.write(str(getattr(function, key)) + ",")
            except AttributeError:
                pass
        for point_set in points:
            if point_set.relational_function == function:
                for key in RelationalPoint.export_fields:
                    try:
                        file.write(str(getattr(point_set, key)) + ",")
                    except AttributeError:
                        pass
        file.write("\n")
    file.close()
    return


def export_pdfs(functions):
    file = open(workspace_path(scenario_filename() + "\\") + "PDF_" + scenario_filename().replace(" ", "") + ".csv", "w")
    for function in functions:
        for key in ProbabilityDensityFunction.export_fields:
            try:
                file.write(str(getattr(function, key)) + ",")
            except AttributeError:
                pass
        file.write("\n")
    file.close()
    return
