from django.views.generic import ListView, View, DetailView
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .models import Performance, Theater, Address, Seat, Ticket

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

def select_seat(request, performance_id):
    performance = get_object_or_404(Performance, pk=performance_id)
    seats = Seat.objects.filter(performance=performance).prefetch_related('tickets')

    # Отримуємо унікальні номери рядів
    row_numbers = seats.values_list('row', flat=True).distinct()

    context = {
        'performance': performance,
        'seats': seats,
        'row_numbers': row_numbers,
    }
    return render(request, 'theaters/select_seat.html', context)

class TicketConfirmationView(View):
    def get(self, request, seat_id):
        # Отримуємо місце за ID
        seat = get_object_or_404(Seat, seat_id=seat_id)
        
        # Отримуємо інформацію про квиток
        ticket = Ticket.objects.filter(seat=seat).first()  # Логіка для отримання квитка

        context = {
            'seat': seat,
            'ticket': ticket,
        }
        return render(request, 'theaters/ticket_confirmation.html', context)

    def post(self, request, seat_id):
        # Отримуємо місце за ID
        seat = get_object_or_404(Seat, seat_id=seat_id)
        
        # Отримуємо квиток (може бути ваша логіка)
        ticket = Ticket.objects.filter(seat=seat).first()  

        # Обробка логіки покупки (зміна статусу квитка на 'sold', тощо)
        if ticket:
            ticket.status = 'sold'
            ticket.save()
        
        # Отримуємо performance_id для редиректу
        performance_id = seat.performance.performance_id  # Припустимо, що у вас є зв'язок між Seat і Performance

        # Повертаємося на сторінку вибору місця з performance_id
        return redirect('select_seat', performance_id=performance_id)  # Замініть на ваш URL для вибору місця
