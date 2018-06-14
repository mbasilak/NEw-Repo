from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse
from .models import InputForm
from dss1.compute import compute

def index(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            return present_output(form)
    else:
        form = InputForm()

    return render(request,'dss1.html',
            {'form': form})

def present_output(form):
    total_rakes = form.total_rakes
    demand = form.demand
    initial_stock_level = form.initial_stock_level
    storage_capacity = form.storage_capacity
    terminal_capacity = form.terminal_capacity
    max_allotment = form.max_allotment
    weekly_penalty = form.weekly_penalty
    comb_matrix = form.comb_matrix
    final_weekly_distribution,final_total_penalty = compute(total_rakes,demand,initial_stock_level,storage_capacity,terminal_capacity,max_allotment,weekly_penalty,comb_matrix)
    return HttpResponse('%s<br>%s<br>%s<br>%s<br>%s<br>%s<br>%s<br>%s<br>%s' % (final_weekly_distribution[0],final_weekly_distribution[1],final_weekly_distribution[2],final_weekly_distribution[3],final_weekly_distribution[4],final_weekly_distribution[5],final_weekly_distribution[6],final_weekly_distribution[7],final_total_penalty))
