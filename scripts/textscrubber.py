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


def hide_fields(filename, output_filename):
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


def switch_to_boolean_field(filename):
    lines = ['', '']
    lines = open(filename, 'r').readlines()
    for index, line in enumerate(lines):
        if line.lstrip().find('use_') == 0:  # field name starts with 'use_'
            field_name = line.split()[0]
            line_ending = line[line.find('(') + 1:]  # starting after the first paren til the end
            lines[index] = field_name + " = models.BooleanField(default=False, " + line_ending

    open(filename, 'w').writelines(lines)


if __name__ == '__main__':
    print("Running from: ", os.getcwd())
    # lowercase_a_file('CreateDjangoInputTables.txt')
    hide_fields('auto-models.py', 'auto-forms.py')
    # switch_to_boolean_field('auto-models.py')