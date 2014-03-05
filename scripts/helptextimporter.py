__author__ = 'Josiah Seaman'


def is_field(line):
    return line[:4] == '    ' and line[4] != ' ' and 'class ' not in line and '=' in line


def insert_help_text_to_models(input_file, documentation_file, output_file):
    code = open(input_file, 'r').readlines()
    for index, line in enumerate(code):
        if is_field(line):
            code[index] = line[:4] + '_' + line[4:]

    open(output_file, 'w').writelines(code)

if __name__ == '__main__':
    insert_help_text_to_models('all-models.py', 'field-documentation.csv', 'auto-models.py')
    print('Done')
