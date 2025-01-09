from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect

def home(request):
    return render(request, 'events/home.html')


def event_list(request):                                                                          
    return render(request, 'events/event_list.html')


def event_detail(request, event_id):
    return render(request, 'events/event_detail.html', {'event_id':
event_id})
    
def delete_event(request, event_id):
    if request.method == 'POST':
        return redirect('events:event_list')
    return render(request, 'events/delete_event.html', {'event_id':
    event_id})