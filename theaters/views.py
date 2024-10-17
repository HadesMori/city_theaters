from pyexpat.errors import messages
from django.views.generic import ListView, View, DetailView
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm

from theaters.forms import ReviewForm
from .models import Performance, Theater, Address, Seat, Ticket, User

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
        'username': set_user(request),
        'performances': performances,
        'addresses': addresses,
    }
    return render(request, 'theaters/performance_list.html', context)

class PerformanceDetailView(DetailView):
    model = Performance
    template_name = 'theaters/performance_detail.html'
    context_object_name = 'performance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = set_user(self.request)
        context['reviews'] = self.object.reviews.all()  # Додати всі відгуки
        context['form'] = ReviewForm()  # Додати форму для нового відгуку
        return context

    def post(self, request, *args, **kwargs):
        performance = self.get_object()
        
        user_id = request.session.get('user_id')  # Отримати id користувача з сесії
        if user_id:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.performance = performance  # Прив'язати відгук до вистави
                review.user = User.objects.get(user_id=user_id)  # Отримати користувача з вашої моделі
                review.date = timezone.now()  # Додати дату
                review.save()
                return redirect('performance_detail', pk=performance.pk)  # Перенаправити назад до деталей вистави
        else:
            # Якщо користувач не автентифікований, можна перенаправити його на сторінку входу
            return redirect('login')  # або показати повідомлення

        return self.get(request, *args, **kwargs)  # Якщо форма не дійсна, повернутися до відображення

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

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST.get('name', '')

        # Перевірка наявності користувача з таким же username або email
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Користувач з таким іменем вже існує.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Користувач з таким email вже існує.')
            return redirect('register')

        user = User(
            username=username,
            email=email,
            name=name,
            password=password, 
            registration_date=timezone.now()
        )
        user.save()

        messages.success(request, 'Реєстрація пройшла успішно. Тепер ви можете увійти.')
        return redirect('login')

    return render(request, 'theaters/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.password == password:  # Ви повинні хешувати пароль для реального проекту
                request.session['user_id'] = user.user_id  # Зберігаємо id користувача в сесії
                messages.success(request, 'Увійшли успішно!')
                return redirect('performance_list')  # Перенаправлення на домашню сторінку
            else:
                messages.error(request, 'Неправильний пароль.')
        except User.DoesNotExist:
            messages.error(request, 'Користувача не знайдено.')
    return render(request, 'theaters/login.html')
    
def logout_view(request):
    request.session.flush()  # Очищення всієї сесії
    messages.success(request, 'Ви вийшли з акаунту.')
    return redirect('login')

def set_user(request):
    user_id = request.session.get('user_id')  # Отримати id користувача з сесії
    username = None
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)  # Знайти користувача за id
            username = user.username
            return username
        except User.DoesNotExist:
            pass