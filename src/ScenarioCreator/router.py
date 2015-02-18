

def part_of_scenario(model):
    return model._meta.app_label in ['ScenarioCreator', 'Results']


def route_by_app(model):
    if part_of_scenario(model):
        return 'scenario_db'
    return None


class ScenarioRouter(object):
    """ A router to separate all database operations based on a single scenario from global persistent settings.
    """

    def db_for_read(self, model, **hints):
        return route_by_app(model)

    def db_for_write(self, model, **hints):
        return route_by_app(model)

    def allow_relation(self, obj1, obj2, **hints):
        """ Ensures ForeignKeys are All in or all out
        """
        if part_of_scenario(obj1) == part_of_scenario(obj2):
           return True
        return False

    def allow_migrate(self, db, model):
        """ Ensures Scenario tables are not created in non-scenario databases
        """
        if db == 'scenario_db':
            return part_of_scenario(model)
        else:  # but not going into the scenario Database
            return not part_of_scenario(model)
