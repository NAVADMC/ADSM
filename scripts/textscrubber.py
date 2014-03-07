import re
from scripts.helptextimporter import split_field_line, is_field

__author__ = 'Josiah Seaman'

import os

"""Databases were originally created using a SQL DDL provided by Missy.  The process is:
textscrubber.lower_case_a_file('createTables.sql')
Terminal:
sqlite3.exe results.db < scripts/CreateDjangoOutputTables.sql
python manage.py inspectdb > Results/models.py
Manually delete all the lines that look like this:
    class Meta:
        managed = False
        db_table = 'outiterationbyzoneandproductiontype'
Search/Replace:
    TextField(   ->  CharField(max_length=255,
    description = CharField(max_length=255,  ->   description = TextField(

Search: "id =" these should be ForeignKeys.  You have to do these manually since they
 require judgement calls.  Example: distance_pdf = models.ForeignKey(ProbabilityEquation, related_name='+')
"""


def lowercase_a_file(filename):
    file = open(filename, 'r')
    content = file.read()
    file.close()
    content = content.lower()
    file = open(filename, 'w')
    file.write(content)
    # content = content.replace('production', '_production_')

    # print(content)
    # lines = file.readlines()
    # for text in lines:
    #     print(text, end='')


def add_if_excluded_field(excluded_fields, line):
    if line.lstrip() and line.lstrip()[0] == '_':  # field indentation and starts with _
        index = line.find('=')
        # print('Excluding: ', line)
        excluded_fields.append(line[:index].strip())
    return excluded_fields


def add_if_foreign_key(foreign_keys, line):
    if is_field(line) and 'ForeignKey' in line:
        indentation, name, ftype, params, end = split_field_line(line)
        target = re.split('\W+', params.replace("'", ''))[0]
        entry = "'" + name.strip() + "':Add_or_Select(attrs={'data-new-item-url': '/setup/"+target+"/new/'})"
        foreign_keys.append(entry)
    return foreign_keys

"""This generator assumes that there are no blank lines before the end of the class model definition.
 This means that if you def functions inside your class there must not be any blank lines between them."""


def handle_field_inheritance(excluded_fields, foreign_keys, model_, parent_model, parent_model_cache):
    if parent_model:
        excluded_fields += parent_model_cache[parent_model][0]
        foreign_keys += parent_model_cache[parent_model][1]
    parent_model_cache[model_] = (excluded_fields, foreign_keys)
    return excluded_fields, foreign_keys


def generate_forms_with_hidden_fields_and_ForeignKeys(filename, output_filename):
    form_lines = []
    excluded_fields = []
    foreign_keys = []
    parent_model_cache = {}
    fkey_count = 0
    model_ = ''
    parent_model = ''
    with open(filename, 'r') as models_file:
        for line_number, line in enumerate(models_file):
            if line.startswith('class'):
                words = re.split('\W+', line)
                model_ = words[1]
                parent_model = words[2] if words[2] != 'models' else ''
            excluded_fields = add_if_excluded_field(excluded_fields, line)
            foreign_keys = add_if_foreign_key(foreign_keys, line)

            if not line.strip() and model_:  # empty line, end of class
                excluded_fields, foreign_keys = handle_field_inheritance(excluded_fields, foreign_keys, model_,
                                                                         parent_model, parent_model_cache)
                print(model_ + '  ' + str(foreign_keys))
                form_lines.append('class ' + model_ + 'Form(ModelForm):')
                form_lines.append('    class Meta:')
                form_lines.append('        model = ' + model_)
                if excluded_fields:
                    form_lines.append('        exclude = ' + str(excluded_fields))
                if foreign_keys:
                    form_lines.append("        widgets = {" + ',\n                   '.join(foreign_keys) + '}')
                form_lines.append('\n')
                fkey_count += len(foreign_keys)

                excluded_fields = []
                foreign_keys = []
                model_ = ''
                parent_model = ''

    print("Found ForeignKeys: ", fkey_count)
    open(output_filename, 'w').write('\n'.join(form_lines))


def switch_to_boolean_fields(filename, output_filename):
    lines = open(filename, 'r').readlines()
    for index, line in enumerate(lines):
        field_name = line[:line.find('=')] if line.find('=') != -1 else ''
        boolean_prefixes = [' trace_', ' destroy_', '_can_', ' vaccinate_', '_is_', ' exam_', ' test_', '_track_', ' write_']  # ['save_', 'use_', 'include_']
        if any(map(lambda prefix: field_name.find(prefix) != -1, boolean_prefixes)):  # field name starts with 'use_' or 'save_'
            if line.find('BooleanField') != -1:
                print(field_name)
                continue  # no need to edit this line
            if line.find('IntegerField') == -1:
                continue  # this is a false positive because BooleanFields would already be Integer to start with
            print(field_name)
            line_ending = line[line.find('(') + 1:]  # starting after the first paren til the end
            line_ending = line_ending.replace('blank=True, null=True', '')
            lines[index] = field_name + " = models.BooleanField(default=False, " + line_ending

    open(output_filename, 'w').writelines(lines)

def createForeignKeys(filename, output_filename):
    'id = models.ForeignKey()'
    lines = open(filename, 'r').readlines()
    for index, line in enumerate(lines):
        field_name = line[:line.find('=')] if line.find('=') != -1 else ''
        field_name = '' if field_name[:4] != '    ' or field_name[4] == ' ' else field_name  #checking for proper indent
        id_index = line.find('id = ')
        if line[4] == '_' and id_index != -1:
            newline = field_name[:field_name.rfind('_')].replace('_', '', 1)  # slice out first and last _
            newline += ' = models.ForeignKey()'
            lines[index] = newline

    open(output_filename, 'w').writelines(lines)



if __name__ == '__main__':
    #Step #1:  Search:  db_column='[^']*', in models.py to remove column names
    print("Running from: ", os.getcwd())
    # lowercase_a_file('CreateDjangoOutputTables.sql')
    generate_forms_with_hidden_fields_and_ForeignKeys('../ScenarioCreator/models.py', 'auto-forms.py')
    # switch_to_boolean_fields('../ScenarioCreator/models.py', 'auto-models.py')
    # generate_urls_from_models('../ScenarioCreator/models.py', 'auto-urls.py')