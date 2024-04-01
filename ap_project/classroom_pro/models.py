from django.db import models

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)
    Role = models.CharField(max_length=30)
    Department = models.CharField(max_length=100, blank=True, null=True)  # Only for faculty
    user_password = models.CharField(max_length=100)


    def __str__(self):
        return self.Name

class Room(models.Model):
    RoomID = models.AutoField(primary_key=True)
    RoomName = models.CharField(max_length=100)
    Facilities = models.CharField(max_length=255)
    Capacity = models.IntegerField()
    Location = models.CharField(max_length=100)

    def __str__(self):
        return self.RoomName

class RoomAvailability(models.Model):
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Date = models.DateField()
    TimeSlot = models.CharField(max_length=100)
    AvailabilityStatus = models.CharField(max_length=20, choices=[('available', 'Available'), ('booked', 'Booked')])

    class Meta:
        unique_together = ('Room', 'Date', 'TimeSlot')

class Booking(models.Model):
    BookingID = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Date = models.DateField()
    TimeSlot = models.CharField(max_length=100)

    def __str__(self):
        return f"Booking {self.BookingID}"

class Approval(models.Model):
    ApprovalID = models.AutoField(primary_key=True)
    Booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    ApprovedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    ApprovalStatus = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

    def __str__(self):
        return f"Approval {self.ApprovalID}"

