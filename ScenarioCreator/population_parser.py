import csv
import itertools
import os
import xml.etree.ElementTree as ET
import ScenarioCreator.models

from ADSMSettings.utils import workspace_path, scenario_filename
from django.conf import settings


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
            {'id': 'unit_id',  # NAADSM CSV no HerdSize, with initial_state and state timers, and with unitid. Also format for ADSM csv export
             'productiontype': 'production_type',
             'unitsize': 'initial_size',
             'lat': 'latitude',
             'lon': 'longitude',
             'initial_state': 'initial_state',
             'daysinstate': 'days_in_initial_state',
             'daysleftinstate': 'days_left_in_initial_state'},
            {'id': 'unit_id',  # NAADSM CSV no HerdSize, with status and state timers, and with unitid. Old format for ADSM csv export
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
            {'unit_id': 'unit_id',  # NAADSM CSV no HerdSize, with status and state timers, and with unitid
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
            if xml_name == "status":
                xml_name = "initial_state"
                try:
                    element = next(herd.iter(xml_name))
                    text = gettext(element)
                except:
                    raise IOError("Couldn't find '%s' label in xml" % xml_name)
            else:
                raise IOError("Couldn't find '%s' label in xml" % xml_name)
        if str(xml_name).lower() in ('id', 'unitid') and text:
             field_name = "unit_id"
        self.population[-1][field_name] = text


class ExportPopulation(object):

    def __init__(self, format):
        self.population = ScenarioCreator.models.Unit.objects

        self.save_location = settings.WORKSPACE_PATH + "\\Exports\\Exported Populations\\"  # Note: scenario_filename uses the database
        self.format = format
        return

    def export(self):

        try:
            os.makedirs(self.save_location)
        except FileExistsError:
            pass

        if self.format == "csv":
            self.__export_csv()
        else:
            self.__export_xml()
        return

    def __export_xml(self):
        file = open(self.save_location + "pop_" + scenario_filename().replace(" ", "") + ".xml", "w")
        file.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        file.write("<herds\n")
        file.write('  xmlns:naadsm="http://www.naadsm.org/schema"\n')
        file.write('  xmlns:xsd="http://www.w3.org/2001/XMLSchema"\n')
        file.write('  xmlns:gml="http://www.opengis.net/gml"\n')
        file.write('  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')
        file.write("\n")
        for unit in self.population.all():
            file.write(self.__write_next_xml_herd(unit) + "\n\n")
        file.write("</herds>")
        return

    def __write_next_xml_herd(self, unit):
        herd_text = "  <herd>\n"

        herd_text += "    <id>"
        herd_text += str(unit.id)
        herd_text += "</id>\n"

        herd_text += "    <production-type>"
        herd_text += str(unit.production_type)
        herd_text += "</production-type>\n"

        herd_text += "    <size>"
        herd_text += str(unit.initial_size)
        herd_text += "</size>\n"

        herd_text += "    <location>\n"
        herd_text += "      <latitude>"
        herd_text += str(unit.latitude)
        herd_text += "</latitude>\n"
        herd_text += "      <longitude>"
        herd_text += str(unit.longitude)
        herd_text += "</longitude>\n"
        herd_text += "    </location>\n"

        herd_text += "    <initial_state>"
        if unit.initial_state == "S":
            herd_text += "Susceptible"
        elif unit.initial_state == "L":
            herd_text += "Latent"
        elif unit.initial_state == "B":
            herd_text += "Subclinical"
        elif unit.initial_state == "C":
            herd_text += "Clinical"
        elif unit.initial_state == "N":
            herd_text += "Naturally Immune"
        elif unit.initial_state == "V":
            herd_text += "Vaccine Immune"
        elif unit.initial_state == "D":
            herd_text += "Destroyed"
        herd_text += "</initial_state>\n"

        herd_text += "    <days-in-initial-state>"
        herd_text += (str(unit.days_in_initial_state) if str(unit.days_in_initial_state) != "None" else '')
        herd_text += "</days-in-initial-state>\n"

        herd_text += "    <days-left-in-initial-state>"
        herd_text += (str(unit.days_left_in_initial_state) if str(unit.days_left_in_initial_state) != "None" else '')
        herd_text += "</days-left-in-initial-state>\n"

        herd_text += "  </herd>"
        return herd_text

    def __export_csv(self):
        csv_order = ["id", "productiontype", "unitsize", "lat", "lon", "initial_state", "daysinstate", "daysleftinstate"]
        file = open(self.save_location + "pop_" + scenario_filename().replace(" ", "") + ".csv", "w")
        for key in csv_order:
            file.write(key + ",")
        file.write("\n")
        for unit in self.population.all():
            file.write(str(unit.id) + "," +
                       str(unit.production_type) + "," +
                       str(unit.initial_size) + "," +
                       str(unit.latitude) + "," +
                       str(unit.longitude) + "," +
                       str(unit.initial_state) + "," +
                       (str(unit.days_in_initial_state) if str(unit.days_in_initial_state) != "None" else '') + "," +
                       (str(unit.days_left_in_initial_state) if str(unit.days_left_in_initial_state) != "None" else '') + ",")
            file.write("\n")
        file.close()
        return
