from ADSMSettings.utils import workspace_path, scenario_filename
from ScenarioCreator.models import ProbabilityDensityFunction


def export_relational_functions(functions):
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
