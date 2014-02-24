__author__ = 'Josiah'


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





if __name__ == '__init__':
    lowercase_a_file('CreateDjangoInputTables.txt')