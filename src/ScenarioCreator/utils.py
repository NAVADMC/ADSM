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

        if pt.targeted_by_vaccination_ring.count(): # subject to vaccination
            if pt.protocolassignment is None or pt.protocolassignment.control_protocol is None:
                warnings.append("FATAL: You must assign a Control Protocol to "+pt.name+" so that you can describe its response to vaccination.")
            else:
                protocol = pt.protocolassignment.control_protocol
                required = ['vaccinate_detected_units',
                            'days_to_immunity',
                            'minimum_time_between_vaccinations',
                            'vaccine_immune_period',
                            'vaccination_priority',
                            #'vaccination_demand_threshold',
                            #'cost_of_vaccination_additional_per_animal',
                            ]
                for field in required:
                    if getattr(protocol, field) is None:
                        warnings.append("FATAL: The Control Protocol field '"+field+"' is required because "+pt.name+" is a target of vaccination.")

    if not Disease.objects.get().include_direct_contact_spread:
        warnings.append("Direct Spread is not enabled in this Simulation.")
    if not Unit.objects.filter(~Q(initial_state='S')).count():
        warnings.append("There are no infected units in the Population.  Please set at least one unit to 'Latent' in the Population screen.")

    return warnings
