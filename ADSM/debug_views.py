def handler400(request):
    pass


def handler403(request):
    pass


def handler404(request):
    pass


def handler500(request):
    from django.views.debug import technical_500_response
    import sys
    print("Caught the error")
    # return render(request, '500.html', {})
    return technical_500_response(request, *sys.exc_info(), status_code=500)
    #return render_to_response('../templates/error/500.html', {'exception': ex}, context_instance=RequestContext(request), status=404)