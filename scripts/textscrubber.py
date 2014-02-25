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


def hide_fields(filename):
    edited_lines = []
    with open(filename, 'r') as models_file:
        for line in models_file:
            if line.lstrip() and line.lstrip()[0] == '_':
                index = line.find('(') + 1
                print( "Editing: ", line)
                edited_lines.append( line[:index] + 'editable=False, ' + line[index:] )
            else:
                edited_lines.append(line)

    open(filename, 'w').writelines(edited_lines)


def switch_to_boolean_field(filename):
    lines = ['', '']
    lines = open(filename, 'r').readlines()
    for index, line in enumerate(lines):
        if line.lstrip().find('use_') == 0:  # field name starts with 'use_'
            field_name = line.split()[0]
            line_ending = line[line.find('(')+1 : ]  # starting after the first paren til the end
            lines[index] = field_name + " = models.BooleanField(default=False, " + line_ending

    open(filename, 'w').writelines(lines)

if __name__ == '__main__':
    print("Running from: ", os.getcwd())
    # lowercase_a_file('CreateDjangoInputTables.txt')
    hide_fields('auto-models.py')
    switch_to_boolean_field('auto-models.py')