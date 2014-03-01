import re

__author__ = 'Josiah Seaman'

import os


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


def generate_forms_with_hidden_fields(filename, output_filename):
    form_lines = []
    excluded_fields = []
    model_ = ''
    with open(filename, 'r') as models_file:
        for line_number, line in enumerate(models_file):
            if line.startswith('class'):
                model_ = re.split('\W+', line)[1]  # line.split()[1].split(sep='(')[0]
            if line.lstrip() and line.lstrip()[0] == '_':  # field indentation and starts with _
                index = line.find('=')
                print('Excluding: ', line)
                excluded_fields.append(line[:index].strip())
            if not line.strip() and model_:  # empty line, end of class
                print('Printing ' + str(excluded_fields))
                form_lines.append('class ' + model_ + 'Form(ModelForm):')
                form_lines.append('    class Meta:')
                form_lines.append('        model = ' + model_)
                if excluded_fields:
                    form_lines.append('        exclude = ' + str(excluded_fields))
                form_lines.append('\n')
                excluded_fields = []
                model_ = ''

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


def generate_urls_from_models(input_file, output_filename):
    lines = open(input_file, 'r').readlines()
    edited_lines = []
    for line in lines:
        if 'class' in line[:5]:
            model_name = re.split('\W+', line)[1]
            edited_lines.append("url('^" + model_name + "/new/$', 'ScenarioCreator.views.new_entry'),")
            edited_lines.append("url('^" + model_name + "/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),\n")

    open(output_filename, 'w').write('\n'.join(edited_lines))


if __name__ == '__main__':
    #Step #1:  Search:  db_column='[^']*', in models.py to remove column names
    print("Running from: ", os.getcwd())
    # lowercase_a_file('CreateDjangoOutputTables.sql')
    # generate_forms_with_hidden_fields('../ScenarioCreator/models.py', 'auto-forms.py')
    # switch_to_boolean_fields('../ScenarioCreator/models.py', 'auto-models.py')
    generate_urls_from_models('../ScenarioCreator/models.py', 'auto-urls.py')