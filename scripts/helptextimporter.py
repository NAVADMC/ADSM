__author__ = 'Josiah Seaman'
import csv



def is_field(line):
    return line[:4] == '    ' and line[4] != ' ' and 'class ' not in line and '=' in line

def valid_doc_field(row):
    return row[0] and row[1] and row[2] and row[4]

def scrub_field(field=''):
    return field.lower().strip().replace('_', '').replace('id', '')


def split_field_line(line):
    indentation = line[:4]
    name = line[4: line.find('=')]
    ftype = line[line.find('='): line.find('(')+1]
    params = line[line.find('(')+1: line.rfind(')')]
    if params and params.rfind(',') < len(params)-2:
        params += ','
    end = line[line.rfind(')'):]
    return indentation, name, ftype, params, end


def insert_help_text_to_models(input_file, documentation_file, output_file):
    code = open(input_file, 'r').readlines()
    documentation = [row for row in csv.reader(open(documentation_file, 'r'))]
    doc_fields = {scrub_field(row[2]): row[4] for row in documentation if valid_doc_field(row)}
    for index, line in enumerate(code):
        if is_field(line):
            indentation, name, ftype, params, end = split_field_line(line)
            if scrub_field(name) in doc_fields:
                help_text = doc_fields[scrub_field(name)]
                code[index] = indentation + name + ftype + params + " \n" + \
                              indentation*2 + "help_text='" + help_text + "'" + end
            else:
                print(name)

    open(output_file, 'w').writelines(code)

if __name__ == '__main__':
    insert_help_text_to_models('all-models.py', 'field-documentation.csv', 'auto-models.py')
    print('Done')
