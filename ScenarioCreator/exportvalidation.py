from ScenarioCreator.models import RelationalFunction, RelationalPoint

__author__ = 'JSeaman'


def order_relational_points():
    for func in RelationalFunction.objects.all():
        point_list = func.relationalpoint_set.all()
        for index, point in enumerate(sorted(point_list, key=lambda point: point.x)):
            RelationalPoint.objects.get(id=point.id)._point_order = index




def db_validation_before_export():
    """Automatically fills in hidden fields based on the values of other things set in the Database"""
    order_relational_points()
