from django import template
from ScenarioCreator.models import RelationalFunction, RelationalPoint

register = template.Library()


@register.filter()
def is_piecewise(function):

    # get all of the relational functions
    RelModel = globals()["RelationalFunction"]
    RelObjects = RelModel.objects.all()
    # we'll need this list to match the incomming function name to the function object.
    # we could do comparisons in place but creating this list here is only marginally slower and makes clearer code.
    RelObjectNames = [func.name for func in RelObjects]

    # get all of the relational points, we'll match them to the function after we've determined which one we are using.
    RelPointsModel = globals()["RelationalPoint"]
    RelPoints = RelPointsModel.objects.all()

    # curr_points will be a list of rel_points matched to the function given
    curr_points = []

    # return value, we'll change it to false if the function is invalid
    piecewise_match = True

    # don't check "-----" as we always want this to display.
    if function[0] != "":
        # for each of the relational object names
        for index, function_name in enumerate(RelObjectNames):
            # if the given function name matches the function_name from the loop
            if function[1] == function_name:
                # set the matching relational function to TestRel
                TestRel = RelObjects[index]
                # for every relational point
                for rel_point in RelPoints:
                    # if that point belongs to the current relational function
                    if rel_point.relational_function == TestRel:
                        # append it to the "matching" list
                        curr_points.append(rel_point)
                # now we check for validity
                # check that starting point's y val is 0
                if curr_points[0].y != 0:
                    piecewise_match = False
                # check that ending point's y val is 0
                if curr_points[-1].y != 0:
                    piecewise_match = False
                # check that x values are increasing
                for index in range(len(curr_points[:-1])):
                    # we use >= here so x values cannot be equal (no vertical lines)
                    if curr_points[index].x >= curr_points[index + 1].x:
                        piecewise_match = False
                # break from the loop, we've found the function we need!
                break
    # return the piecewise_match, if the function is valid it has remained unchanged and is True
    return piecewise_match
