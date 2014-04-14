__author__ = 'JSeaman'
"""Made with Ipython Notebooks"""


def is_field(line):
    return line[:4] == '    ' and line[4] not in ' #' and 'class ' not in line and '=' in line and 'def ' not in line


lines = open('models.py', 'r').readlines()
class_lines = map(lambda x: x.replace("(models.Model):\n", ''), filter(lambda x: x.startswith('class'), lines))
field_lines = filter(is_field, lines)


def split_field_line(line):
    indentation = line[:4]
    name = line[4: line.find('=')]
    ftype = line[line.find('='): line.find('(')+1]
    params = line[line.find('(')+1: line.rfind(')')]
    if params and params.rfind(',') < len(params)-2:
        params += ','
    end = line[line.rfind(')'):]
    return indentation, name, ftype, params, end


def get_help_text(line_number):
    for line in lines[line_number+1:line_number+10]:
        if is_field(line):
            return ''
        start = line.find("help_text")
        if start != -1:
            return line[start+11:-5]
    return ''


def main():
    iter_class = iter(class_lines)
    for line_number, line in enumerate(lines):
        if line.startswith('class'):
            print("\n%s" % iter_class.next())
        if is_field(line):
            indentation, name, ftype, params, end = split_field_line(line)
            help_text = get_help_text(line_number)
            print("%s, %s, %s" % (name.strip(), ftype.replace("= models.", '').replace('(', ''), help_text))

if __name__ == '__main__':
    main()
