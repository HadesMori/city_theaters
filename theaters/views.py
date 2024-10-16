from django.views.generic import ListView, View, DetailView
from django.utils import timezone
from django.shortcuts import render
from .models import Performance, Theater, Address

class PerformanceListView(View):
    def get(self, request):
        performances = Performance.objects.all()

        # Фільтрація за жанром
        genre_filter = request.GET.get('genre')
        if genre_filter:
            performances = performances.filter(genre__icontains=genre_filter)

        # Сортування за датою
        sort_by = request.GET.get('sort')
        if sort_by == 'date':
            performances = performances.order_by('date_time')
        elif sort_by == 'date_desc':
            performances = performances.order_by('-date_time')

        # Фільтрація за майбутніми виставами
        performances = performances.filter(date_time__gte=timezone.now())

        context = {
            'performances': performances
        }
        return render(request, 'theaters/performance_list.html', context)

def performance_list(request):
    # Отримання унікальних міст із таблиці Address
    addresses = Address.objects.values('city').distinct()

    # Отримання параметрів фільтрації з запиту
    city = request.GET.get('city')
    genre = request.GET.get('genre')
    sort = request.GET.get('sort')

    # Базовий запит для отримання всіх вистав
    performances = Performance.objects.all()

    # Фільтрація за містом
    if city:
        performances = performances.filter(theater__address__city=city)

    # Фільтрація за жанром
    if genre:
        performances = performances.filter(genre__icontains=genre)

    # Сортування
    if sort == 'date':
        performances = performances.order_by('date_time')
    elif sort == 'date_desc':
        performances = performances.order_by('-date_time')

    context = {
        'performances': performances,
        'addresses': addresses,
    }
    return render(request, 'theaters/performance_list.html', context)

class PerformanceDetailView(DetailView):
    model = Performance
    template_name = 'theaters/performance_detail.html'
    context_object_name = 'performance'

class TheaterDetailView(DetailView):
    model = Theater
    template_name = 'theaters/theater_detail.html'
    context_object_name = 'theater'

