import csv
import itertools
import os
import xml.etree.ElementTree as ET
import ScenarioCreator.models


def gettext(elem):
    return ",".join(elem.itertext())


def lowercase_header(iterator):
    """Source: http://stackoverflow.com/questions/16937457/python-dictreader-how-to-make-csv-column-names-lowercase"""
    return itertools.chain([next(iterator).lower()], iterator)



def convert_numeric_status_codes(entry):
    try:
        state_code = int(entry['initial_state'])
        letter = ScenarioCreator.models.Unit.initial_state_choices[state_code][0]
        entry['initial_state'] = letter
        return entry
    except ValueError:
        return entry
    except IndexError:
        raise ET.ParseError("State code " + str(entry['initial_state']) + " not recognized.  The only known unit statuses are:" + 
                         str(ScenarioCreator.models.Unit.initial_state_choices))


class PopulationParser(object):
    model_labels = ['user_notes', 'production_type', 'latitude', 'longitude', 'initial_state', 'initial_size']
    xml_fields =   ['id',         'production-type', 'latitude', 'longitude', 'status',        'size']
    text_fields = list(zip(model_labels, xml_fields))

    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise OSError("'" + filename + "' is not a file.")

        if not os.path.getsize(filename):
            raise EOFError("File Read returned a blank string.")

        self.population = []
        self.filename = filename
        self.is_xml = '.xml' in filename
        if self.is_xml:
            tree = ET.ElementTree(file=filename)
            self.top_level = tree.getroot()
        else:  #csv
            self.__parse_csv(filename)

    def parse_to_dictionary(self):
        if self.is_xml:
            self.__parse_xml_population_fields(self.text_fields)
        else:
            pass  # csv parsing already done
        return self.population

    def __parse_csv_units(self, filename, mapping):
        with open(filename) as csvfile:
            reader = csv.DictReader(lowercase_header(csvfile))
            for unit in reader:
                entry = {store_key: unit[header] for header, store_key in mapping.items()}
                entry = convert_numeric_status_codes(entry)
                # preserve the information from any colulmns I didn't use
                entry['user_notes'] = ', '.join(["%s=%s" % (key, value) for key, value in unit.items() if key not in mapping])
                self.population.append(entry)

    def __parse_csv(self, filename):
        """Make sure that formats with more keys are at the top and formats with fewer keys are at the bottom.
        This is because a format that has fewer options, but same names will match to a format that has more options
        containing all the options of the smaller one. This case will end up throwing an error for missing columns."""
        possible_formats = [
            {'id': 'unit_id',  # NAADSM CSV no HerdSize, with status and state timers, and with unitid
             'productiontype': 'production_type',
             'unitsize': 'initial_size',
             'lat': 'latitude',
             'lon': 'longitude',
             'status': 'initial_state',
             'daysinstate': 'days_in_initial_state',
             'daysleftinstate': 'days_left_in_initial_state'},
            {'unitid': 'unit_id', # NAADSM CSV no HerdSize, with status and state timers, and with unitid
             'productiontype': 'production_type',
             'unitsize': 'initial_size',
             'lat': 'latitude',
             'lon': 'longitude',
             'status': 'initial_state',
             'daysinstate': 'days_in_initial_state',
             'daysleftinstate': 'days_left_in_initial_state'},
            {'productiontype': 'production_type',  # NAADSM CSV no HerdSize, with status and state timers
             'unitsize': 'initial_size',
             'lat': 'latitude',
             'lon': 'longitude',
             'status': 'initial_state',
             'daysinstate': 'days_in_initial_state',
             'daysleftinstate': 'days_left_in_initial_state'},
            {'productiontype': 'production_type',  # NAADSM CSV includes HerdSize synonym
             'lon': 'longitude',
             'lat': 'latitude',
             'herdsize': 'initial_size',
             'status': 'initial_state',
             'daysinstate': 'days_in_initial_state',
             'daysleftinstate': 'days_left_in_initial_state'},
            {'production-type': 'production_type',  # NAADSM CSV mapping
             'longitude': 'longitude',
             'latitude': 'latitude',
             'size': 'initial_size',
             'status': 'initial_state'},
            {'productiontype': 'production_type',  # NAADSM CSV includes HerdSize synonym without state timers
             'lon': 'longitude',
             'lat': 'latitude',
             'herdsize': 'initial_size',
             'status': 'initial_state'},
            {'productiontype': 'production_type',  # NAADSM CSV population export without state timers
             'lon': 'longitude',
             'lat': 'latitude',
             'unitsize': 'initial_size',
             'status': 'initial_state'},
        ]
        parsing_success = False
        for mapping in possible_formats:
            if not parsing_success:
                try:
                    self.__parse_csv_units(filename, mapping)
                    parsing_success = True
                except KeyError:
                    parsing_success = False
        if not parsing_success:
            raise ET.ParseError('Unrecognized csv header format! Please refer to the <a href="https://github.com/NAVADMC/ADSM/wiki/Population-File-Requirements" class="wiki" target="_blank">wiki</a> for help.')



    def __parse_xml_population_fields(self, text_fields):
        for herd in self.top_level.iter('herd'):
            self.population.append( dict() ) #empty
            for t in text_fields:
                if isinstance(t, tuple):
                    self.__populate_xml_text_field(herd, *t)
                else:
                    self.__populate_xml_text_field(herd, t)

    def __populate_xml_text_field(self, herd, field_name, xml_name=''):
        if not xml_name:
            xml_name = field_name
        try:
            element = next(herd.iter(xml_name))
            text = gettext(element)
        except:
            raise IOError("Couldn't find '%s' label in xml" % xml_name)
        if str(xml_name).lower() in ('id', 'unitid') and text:
             field_name = "unit_id"
        self.population[-1][field_name] = text
