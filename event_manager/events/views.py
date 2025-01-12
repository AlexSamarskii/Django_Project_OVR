
from django.forms import ValidationError
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
from .forms import ReviewForm
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer
from .models import Event
from rest_framework import generics
from rest_framework import viewsets

#events = Event.objects.all().order_by('date')

class EventDeleteView(UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('events:event_list')
    
    def test_func(self):
        event = self.get_object()
        return self.request.user.is_authenticated and self.request.user == event.created_by
    
    def handle_no_permission(self):
        return redirect('events:login')

def is_admin(user):
    return user.is_authenticated and user.is_staff

def post_review(request, event):
    review_form = ReviewForm(request.POST, event=event)
    try:
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.event = event
            review.user = request.user 
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен.')
            return redirect('events:event_detail', event_id=event.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    except ValidationError as e:
        review_form.add_error(None, e)
    return review_form 
    
@api_view(['GET', 'POST'])
def api_event_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
@api_view(['GET', 'PUT', 'DELETE'])
def api_event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventListAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = event.reviews.all().order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('events:login')
        review_form = post_review(request, event)
    else:
        review_form = ReviewForm(event=event)
    return render(request, 'events/event_detail.html', {'event': event,
                                                        'reviews': reviews,
                                                        'review_form': review_form,
                                                        })

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
    
@permission_required('events.add_event', login_url='events:login')
@user_passes_test(is_admin)
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            event.created_by = request.user
            event.save()
            messages.success(request, 'Мероприятие успешно добавлено.')
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})
    
@user_passes_test(is_admin)
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.created_by != request.user:
        return redirect('events:event_detail', event_id=event.id)
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

# def event_detail(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     reviews = event.reviews.all().order_by('-created_at')
#     if request.method == 'POST':
#         review_form = ReviewForm(request.POST, event=event)
#         try:
#             if review_form.is_valid():
#                 review = review_form.save(commit=False)
#                 review.event = event
#                 review.save()
#                 messages.success(request, 'Ваш отзыв успешно добавлен.')
#                 return redirect('events:event_detail',
#                 event_id=event.id)
#             else:
#                 messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
#         except ValidationError as e:
#             review_form.add_error(None, e)
#     else:
#         review_form = ReviewForm(event=event)
#     return render(request, 'events/event_detail.html', {
#         'event': event,
#         'reviews': reviews,
#         'review_form': review_form,
#         })
    
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('events:home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = SignUpForm()
    return render(request, 'events/signup.html', {'form': form})