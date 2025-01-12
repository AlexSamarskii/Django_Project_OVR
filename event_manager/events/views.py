
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from django.views.generic import DeleteView
from django.urls import reverse_lazy
import csv
from django.http import HttpResponse

#events = Event.objects.all().order_by('date')

def event_list(request):
    events = Event.objects.all().order_by('date')
    print(f"Количество мероприятий: {events.count()}")
    return render(request, 'events/event_list.html', {'events': events})

def export_events_csv(request):
    events = Event.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="events.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Date', 'Location',
    'Category'])
    for event in events:
        writer.writerow([event.title, event.description, event.date,
        event.location, event.category.name])
    return response

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('events:event_list')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

def event_detail(request, event_id):
    print("event detail")
    event = get_object_or_404(Event, id=event_id)
    print("11", event)
    comments = event.comments.all().order_by('-created_at')
    return render(request, 'events/event_detail.html', {
        'event': event,
        'comments': comments
    })

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            print(type(event))
            print(event.id)
            messages.success(request, 'Мероприятие успешно добавлено.')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})
    
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Мероприятие успешно обновлено.')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form, 'event':
    event})    
    
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
    return render(request, 'events/services.html', {'services':services_list})
    
team_members = [
    {'name': 'Иван Иванов', 'position': 'Директор'},
    {'name': 'Петр Петров', 'position': 'Менеджер проектов'},
    {'name': 'Светлана Смирнова', 'position': 'Координатор мероприятий'},
    ]
    
def team(request):
    return render(request, 'events/team.html', {'team': team_members})

def contact_us(request):
    return render(request, 'events/contact_us.html')

def gallery(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/gallery.html', {'events': events})

def contact_us(request):
    return render(request, 'events/contact_us.html')

class GalleryView(TemplateView):
    template_name = 'events/gallery.html'
    
class UserListView(ListView):
    model = User
    template_name = 'events/user_list.html'
    context_object_name = 'users'


events = [
    {'id': 1, 'title': 'Концерт классической музыки', 'date':
    '12.01.2025 19:00', 'description': 'Концерт с участием известных исполнителей.', 'location': 'Концертный зал', 'organizer': 'Иван Иванов'},
    {'id': 2, 'title': 'Выставка современного искусства', 'date':
    '02.02.2025 10:00', 'description': 'Выставка работ современных художников.',
    'location': 'Галерея искусств', 'organizer': 'Петр Петров'},
    {'id': 3, 'title': 'Театральная постановка', 'date': '08.03.2025 18:30', 'description': 'Постановка классического произведения.', 'location':
    'Драматический театр', 'organizer': 'Светлана Смирнова'},
]

def home(request):
    return render(request, 'events/home.html', {'events': events})

# def event_detail(request, event_id):
#     event = next((item for item in events if item['id'] == event_id), None)
#     if event:
#         return render(request, 'events/event_detail.html', {'event': event})
#     else:
#         return render(request, 'events/event_not_found.html')
    
def about(request):
    return render(request, 'events/about.html', {'team': team_members})