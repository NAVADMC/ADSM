__author__ = 'Josiah Seaman'


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
            if line.lstrip()[0] == '_':
                index = line.find('(') + 1
                edited_lines.append( line[:index] + 'editable=false, ' + line[index:] )
            else:
                edited_lines.append(line)

    open(filename, 'w').write(edited_lines)



if __name__ == '__init__':
    # lowercase_a_file('CreateDjangoInputTables.txt')
    hide_fields('auto-models.py')
