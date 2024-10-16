from django.db import models

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100, db_collation='Ukrainian_CI_AS')
    street = models.CharField(max_length=255, db_collation='Ukrainian_CI_AS', blank=True, null=True)
    building = models.CharField(max_length=10, db_collation='Ukrainian_CI_AS', blank=True, null=True)
    country = models.CharField(max_length=100, db_collation='Ukrainian_CI_AS')

    class Meta:
        db_table = 'Address'

    def __str__(self):
        return f"{self.street} {self.building}, {self.city}, {self.country}"


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50, db_collation='Ukrainian_CI_AS')
    name = models.CharField(max_length=100, db_collation='Ukrainian_CI_AS', blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, db_collation='Ukrainian_CI_AS')
    password = models.CharField(max_length=255, db_collation='Ukrainian_CI_AS')
    registration_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'User'

    def __str__(self):
        return f"{self.username} ({self.name})"


class Theater(models.Model):
    theater_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_collation='Ukrainian_CI_AS')
    address = models.ForeignKey(Address, models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=15, db_collation='Ukrainian_CI_AS', blank=True, null=True)
    email = models.CharField(max_length=255, db_collation='Ukrainian_CI_AS', blank=True, null=True)
    website = models.CharField(max_length=255, db_collation='Ukrainian_CI_AS', blank=True, null=True)
    description = models.TextField(db_collation='Ukrainian_CI_AS', blank=True, null=True)

    class Meta:
        db_table = 'Theater'

    def __str__(self):
        return self.name


class Performance(models.Model):
    performance_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_collation='Ukrainian_CI_AS')
    genre = models.CharField(max_length=100, db_collation='Ukrainian_CI_AS', blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    description = models.TextField(db_collation='Ukrainian_CI_AS', blank=True, null=True)
    date_time = models.DateTimeField()
    theater = models.ForeignKey(Theater, models.CASCADE, blank=True, null=True, related_name='performances')
    picture = models.CharField(max_length=255, db_collation='Ukrainian_CI_AS', blank=True, null=True)

    class Meta:
        db_table = 'Performance'

    def __str__(self):
        return f"{self.name} at {self.theater.name} on {self.date_time}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
    performance = models.ForeignKey(Performance, models.CASCADE, blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    comment = models.TextField(db_collation='Ukrainian_CI_AS', blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Review'

    def __str__(self):
        return f"Review by {self.user.username} for {self.performance.name}"


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'Seat'

    def __str__(self):
        return f"Seat {self.seat} in row {self.row} for {self.performance.name}"


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, db_collation='Ukrainian_CI_AS', blank=True, null=True)
    seat = models.ForeignKey(Seat, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'Ticket'

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.status} - {self.seat}"