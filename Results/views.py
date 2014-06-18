from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect


def back_to_inputs(request):
    return redirect('/setup/')


def population(request):
    return redirect('/setup/')
