from django.contrib import admin
from .models import Address, User, Theater, Performance, Review, Seat, Ticket

from django.contrib import admin
from .models import Address, User, Theater, Performance, Review, Seat, Ticket

class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'city', 'street', 'building', 'country')
    search_fields = ('city', 'street', 'building', 'country')

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'name', 'email', 'registration_date')
    search_fields = ('username', 'email', 'name')

class TheaterAdmin(admin.ModelAdmin):
    list_display = ('theater_id', 'name', 'phone_number', 'email', 'website')
    search_fields = ('name', 'phone_number', 'email', 'website')

class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('performance_id', 'name', 'genre', 'duration', 'date_time')
    search_fields = ('name', 'genre', 'description')
    list_filter = ('theater',)  # Only use 'theater' if it's a ForeignKey

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'user', 'performance', 'rating', 'date')
    search_fields = ('user', 'performance', 'comment')
    list_filter = ('performance',)

class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_id', 'row', 'seat', 'performance')
    search_fields = ('row', 'seat')
    list_filter = ('performance',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'price', 'status', 'seat')
    search_fields = ('price', 'status')
    list_filter = ('status',)

# Реєстрація моделей з адміністративними класами
admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Theater, TheaterAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Ticket, TicketAdmin)