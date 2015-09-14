from django.db.models import Q

from ScenarioCreator.models import ProductionType, DiseaseProgressionAssignment, DiseaseSpreadAssignment, Disease, Unit, DirectSpread, DiseaseProgression

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

    return warnings
