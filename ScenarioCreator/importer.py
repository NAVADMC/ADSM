from ADSMSettings.utils import workspace_path, scenario_filename
from ScenarioCreator.models import ProbabilityDensityFunction, RelationalFunction, RelationalPoint

from os import listdir
import csv


def import_relational_functions(existing_functions):
    '''

    Import the relational functions

    Relational functions are saved with their points, however the database stores the functions and the points
    seperatly. We need to build a funciton for each line of each file, as well as an unknown number of points that
    also need to be linked to the correct funciton.

    :param existing_functions: list of existing relational functions, this is used to avoid duplicate names
    :return: None
    '''

    # stamp into cmd (#1016)
    print("Starting REL function import...")

    # get a list of all file names delimited by "REL_", are .csv, and do not have the current scenario's name
    file_names = [file for file in listdir(workspace_path(scenario_filename() + "\\Imports\\")) if
                  str(file).startswith("REL_") and
                  str(file).endswith(".csv")]
    # get a list of the existing rels names.
    existing_rel_names = [rel.name for rel in existing_functions]
    rel_import_fields = ["name", "x_axis_units", "notes", "y_axis_units"]
    point_import_fields = ["x", "y"]

    # this variable is opened here so it is never referenced unassigned
    new_points = ""

    # for each file found
    for file_name in file_names:
        # open that file
        file = open(workspace_path(scenario_filename() + "\\Imports\\") + file_name, "r")
        csvreader = csv.reader(file, delimiter=",", quotechar='"', escapechar='\\', quoting=csv.QUOTE_MINIMAL)
        # for each relational function saved within
        for rel in csvreader:
            if len(rel) > 0:
                # create a new blank relational funciton
                new_rel = RelationalFunction()
                # for each field found within
                for index, field in enumerate(rel):
                    # import the relational function fields
                    if index < 4:
                        # if it is the first field (name)
                        if index == 0:
                            # append " - imported" until the name is no longer a duplicate name
                            while field in existing_rel_names:
                                field += " - imported"
                        # if the field is blank or a newline, pass
                        if field == "" or field == "\n":
                            pass
                        # else save that field to the corresponding object part
                        else:
                            setattr(new_rel, rel_import_fields[index], field)
                    # import the relational function points
                    else:
                        # if the index is 4, it is the first point
                        if index == 4:
                            # save the relational function already created
                            new_rel.save()
                        # if the index % 2 == 0, the cell is the first in a set of points.
                        if index % 2 == 0:
                            # create a new relational point
                            new_points = RelationalPoint()
                            # assign the new point to the previously created relational function
                            new_points.relational_function_id = new_rel.id

                        # if the field is blank or a newline, pass
                        if field == "" or field == "\n":
                            pass
                        # else save that field to the corresponding object part
                        else:
                            setattr(new_points, point_import_fields[index % 2], float(field.replace("\n", "")))

                        # if the index % 2 == 1, the cell is the last in a set of points
                        if index % 2 == 1:
                            # save the relational point object.
                            new_points.save()
        # close the file to avoid corruption
        file.close()

    # stamp out of cmd (#1016)
    print("Function import complete.")
    return


def import_pdfs(existing_functions):
    '''
    Import the pdfs

    Each pdf needs to be read in from the file and built in an object for the database

    :param existing_functions: list of existing functions, used to avoid creating duplicate function names
    :return: None
    '''

    # stamp into cmd (#1016)
    print("Starting PDF import...")

    # get a list of all file names delimited by "PDF_", are .csv, and do not have the current scenario's name
    file_names = [file for file in listdir(workspace_path(scenario_filename() + "\\Imports\\")) if
             str(file).startswith("PDF_") and
             str(file).endswith(".csv")]
    # get a list of the existing pdf's names.
    existing_pdf_names = [pdf.name for pdf in existing_functions]
    # list of fields that need to be imported
    import_fields = ["name", "x_axis_units", "notes", "equation_type", "mean", "std_dev", "min", "mode", "max", "alpha",
                     "alpha2", "beta", "location", "scale", "shape", "n", "p", "m", "d", "theta", "a", "s", "graph"]
    # for each of the located files
    for file_name in file_names:
        # open that file
        file = open(workspace_path(scenario_filename() + "\\Imports\\") + file_name, "r")
        csvreader = csv.reader(file, delimiter=",", quotechar='"', escapechar='\\', quoting=csv.QUOTE_MINIMAL)
        # for each of the pdfs saved within
        for pdf in csvreader:
            if len(pdf) > 0:
                # create a blank new pdf object
                new_pdf = ProbabilityDensityFunction()
                # for each field located in the file
                for index, field in enumerate(pdf):
                    # remove quotes from field
                    field = field.replace("'", "")
                    # if it is the first field (name field)
                    if index == 0:
                        # append " - imported" until the name is not a duplicate
                        while field in existing_pdf_names:
                            field += " - imported"
                    # if the field is blank, pass
                    if field == "None" or field == "None\n":
                        pass
                    # else set the attribute of the new object to that value
                    else:
                        setattr(new_pdf, import_fields[index], field)
                # save the object before moving on to the next line
                new_pdf.save()
        # close the file to avoid corruption.
        file.close()

    # stamp out of cmd (#1016)
    print("Function import complete.")

    return
