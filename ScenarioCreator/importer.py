from ADSMSettings.utils import workspace_path, scenario_filename
from ScenarioCreator.models import ProbabilityDensityFunction

from os import listdir


def import_relational_functions():
    return


def import_pdfs(existing_functions):
    file_names = [file for file in listdir(workspace_path(scenario_filename() + "\\")) if
             str(file).startswith("PDF_") and
             str(file).endswith(".csv") and
             scenario_filename().replace(" ", "") not in str(file)]
    existing_pdf_names = [pdf.name for pdf in existing_functions]
    import_fields = ["name", "x_axis_units", "notes", "equation_type", "mean", "std_dev", "min", "mode", "max", "alpha",
                     "alpha2", "beta", "location", "scale", "shape", "n", "p", "m", "d", "theta", "a", "s", "graph"]
    for file_name in file_names:
        file = open(workspace_path(scenario_filename() + "\\") + file_name, "r")
        for pdf in file.readlines():
            new_pdf = ProbabilityDensityFunction()
            for index, field in enumerate(pdf.split(",")[:-1]):
                if index == 0:
                    while field in existing_pdf_names:
                        field += " - imported"
                if field == "None" or field == "None\n":
                    pass
                else:
                    setattr(new_pdf, import_fields[index], field)
            new_pdf.save()
    return
