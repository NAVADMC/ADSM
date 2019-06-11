from ADSMSettings.utils import workspace_path, scenario_filename
from ScenarioCreator.models import ProbabilityDensityFunction, RelationalFunction, RelationalPoint

from os import listdir


def import_relational_functions(existing_functions):
    file_names = [file for file in listdir(workspace_path(scenario_filename() + "\\")) if
                  str(file).startswith("REL_") and
                  str(file).endswith(".csv") and
                  scenario_filename().replace(" ", "") not in str(file)]
    existing_rel_names = [rel.name for rel in existing_functions]
    rel_import_fields = ["name", "x_axis_units", "notes", "y_axis_units"]
    point_import_fields = ["x", "y"]

    for file_name in file_names:
        file = open(workspace_path(scenario_filename() + "\\") + file_name, "r")
        for rel in file.readlines():
            new_rel = RelationalFunction()
            for index, field in enumerate(rel.split(",")):
                # import the relational function fields
                if index < 4:
                    if index == 0:
                        while field in existing_rel_names:
                            field += " - imported"
                    if field == "" or field == "\n":
                        pass
                    else:
                        setattr(new_rel, rel_import_fields[index], field)
                # import the relational function points
                else:
                    if index == 4:
                        new_rel.save()
                    if index % 2 == 0:
                        new_points = RelationalPoint()
                        new_points.relational_function_id = new_rel.id

                    if field == "" or field == "\n":
                        pass
                    else:
                        setattr(new_points, point_import_fields[index % 2], float(field.replace("\n", "")))
                    if index % 2 == 1:
                        new_points.save()
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
