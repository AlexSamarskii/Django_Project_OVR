from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.contrib.auth.models import User

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
    
def services(request):
    services_list = [
    'Организация мероприятий',
    'Аренда оборудования',
    'Кейтеринг',
    'Развлекательные программы',
    ]
    return render(request, 'events/services.html', {'services':
services_list})

def team(request):
    team_members = [
    {'name': 'Иван Иванов', 'position': 'Директор'},
    {'name': 'Петр Петров', 'position': 'Менеджер проектов'},
    {'name': 'Светлана Смирнова', 'position': 'Координатор мероприятий'},
    ]
    return render(request, 'events/team.html', {'team': team_members})

def contact_us(request):
    return render(request, 'events/contact_us.html')

class GalleryView(TemplateView):
    template_name = 'events/gallery.html'
    
class UserListView(ListView):
    model = User
    template_name = 'events/user_list.html'
    context_object_name = 'users'
    