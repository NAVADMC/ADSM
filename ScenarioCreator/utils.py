import json
import re

from django.db.models import Q, Count

from ScenarioCreator.models import ProductionType, DiseaseProgressionAssignment, DiseaseSpreadAssignment, Disease, Unit, DirectSpread, DiseaseProgression, \
    ControlProtocol

__author__ = 'Josiah'


def whole_scenario_validation():
    warnings = []
    total_types = ProductionType.objects.all().count()
    empty_assignments = DiseaseSpreadAssignment.objects.filter(direct_contact_spread__isnull=True, indirect_contact_spread__isnull=True,
                                                               airborne_spread__isnull=True)
    for pt in ProductionType.objects.all():
        if not DiseaseProgressionAssignment.objects.filter(production_type=pt, progression__isnull=False).count():
            warnings.append(pt.name + " has no Disease Progression assigned and so is a non-participant in the simulation.")
        if empty_assignments.filter(source_production_type=pt).count() == total_types and \
                        empty_assignments.filter(destination_production_type=pt).count() == total_types:
            warnings.append(pt.name + " is not involved in any type of disease spread. This Type is a non-participant in the simulation.")

    if not Disease.objects.get().include_direct_contact_spread:
        warnings.append("Direct Spread is not enabled in this Simulation.")
    if not Unit.objects.filter(~Q(initial_state='S')).count():
        warnings.append("There are no infected units in the Population.  Please set at least one unit to 'Latent' in the Population screen.")
    if not Disease.objects.get().use_within_unit_prevalence:
        if DirectSpread.objects.filter(infection_probability__isnull=True).count():
            warnings.append("Direct Spread: Infection Probability is required if you are not using Disease Prevalence.  Please define in: ")
            for entry in DirectSpread.objects.filter(infection_probability__isnull=True):
                warnings.append(" - - - " + entry.name)
    else:
        if DiseaseProgression.objects.filter(disease_prevalence__isnull=True).count():
            warnings.append("Disease Progression: Disease Prevalence must be defined for each progression model.  Please define in: ")
            for entry in DiseaseProgression.objects.filter(disease_prevalence__isnull=True):
                warnings.append(" - - - " + entry.name)

    #Check that an invalid tab wasn't activated
    for protocol in ControlProtocol.objects.all():
        if not protocol.is_valid():
            warnings.append(protocol.name + " Protocol has a section enabled but not completely filled in.  Either disable the section or fill in the details of the invalid section.")

    # checking for unique user ids
    # create list of unit ids
    unit_ids = [unit.get_id() for unit in Unit.objects.all()]
    # create a version of the list with only one listing of each element
    set_unit_ids = list(set(unit_ids))
    # for every item in the original list
    for index in range(len(unit_ids)):
        # try catches populations that were not traditionally imported (the sample scenarios)
        try:
            # if the sorted indexes of both lists do not match, there are duplicate elements
            if sorted(unit_ids)[index] != sorted(set_unit_ids)[index]:
                # validation message provided by Missy Schoenbaum
                warnings.append("Validation indicated that your unit identifiers are not unique identifiers. Supplemental files use this identifier in creating the output. Joining output for post-processing will not be advisable.")
                # break, only one non-unique id is required for this warning.
                break
        except TypeError:
            # break for sample scenarios, it is safe to assume their user ids are unique
            break

    return warnings


def convert_user_notes_to_unit_id():
    print("Converting any existing user_notes to unit_id as needed...")
    units = Unit.objects.filter(Q(user_notes__isnull=False) | ~Q(user_notes=''), Q(unit_id__isnull=True) | Q(unit_id=''))
    updated_units = []
    for unit in units:
        unit_id_search = re.search(".*?unit_id=([0-9]+)", str(unit.user_notes))  # Note that on None user_notes, we are actually regexing "None" which is fine for now.
        if unit_id_search is not None and unit.unit_id in (None, ''):  # The unit_id being none check isn't needed with the new filter above, but we'll keep it for future safety
            unit.unit_id = unit_id_search.group(1)
            updated_units.append(unit)
    Unit.objects.bulk_update(updated_units, ['unit_id'])
