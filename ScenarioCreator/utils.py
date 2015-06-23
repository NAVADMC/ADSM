from django.db.models import Q

from ScenarioCreator.models import ProductionType, DiseaseProgressionAssignment, DiseaseSpreadAssignment, Disease, Unit


__author__ = 'Josiah'


def whole_scenario_validation():
    warnings = []
    for pt in ProductionType.objects.all():
        if not DiseaseProgressionAssignment.objects.filter(production_type=pt, progression__isnull=False).count():
            warnings.append(pt.name + " has no Disease Progression assigned and so is a non-participant in the simulation.")
        if not DiseaseSpreadAssignment.objects.filter(source_production_type=pt,
                                                      destination_production_type=pt,
                                                      direct_contact_spread__isnull=False).count():
            warnings.append(
                pt.name + " cannot spread disease from one animal to another, because Direct Spread %s -> %s has not been assigned." % (pt.name, pt.name))
    if not Disease.objects.get().include_direct_contact_spread:
        warnings.append("Direct Spread is not enabled in this Simulation.")
    if not Unit.objects.filter(~Q(initial_state='S')).count():
        warnings.append("There are no infected units in the Population.  Please set at least one unit to 'Latent' in the Population screen.")

    return warnings
