from datetime import date, time, datetime, timedelta
from django.core.exceptions import ValidationError
from django.db import models


START_HOUR = 9
END_HOUR =  18
workingHours = END_HOUR - START_HOUR

class Vendor(models.Model):
    """
    This class defines which vendors are allowed raise tickets with our system.
    """
    vendor = models.CharField(max_length=25)

    def __str__(self):
        return self.vendor

def no_past(value):
    today = date.today()
    if value < today:
        raise ValidationError('Holiday Date cannot be in the past.')

class Holiday(models.Model):
    """
    Define the holiday or non-working days for each based on each region.
    """
    day = models.DateField(help_text="Enter the date of Holiday", validators=[no_past])
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('day',)
    def __str__(self):
        return "{}  {}".format(self.day, self.description)

class Category(models.Model):
    """
    We define the type of category to which a particular ticket belongs here.
    """
    CATEGORY_CHOICES = (
        ('Website Down', 'Website Down'),
        ('Problem with WiFi', 'Problem with WiFi'),
        ('Server Down', 'Server Down'),
        ('Cannot Login', 'Cannot Login'),
        ('Critical Bug','Critical Bug'),
        ('Problem with Billing System','Problem with Billing System'),
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category

class Ticket(models.Model):
    """
    Our ticket models objects are created here and stored in the database
    as a table with the attributes mentioned below.
    """
    SEVERITY_CHOICES = (
        (4, 1),  # severity 1 to be resolved in 4 hours
        (24, 2), # severity 2 to be resolved in 24 hours
        (72, 3), # severity 3 to be resolved in 72 hours / 3 days
        (168, 4), # severity 4 to be resolved in 168 hours / 7 days
        (720, 5), # severity 5 to be resolved in 720 hours / 30 days
        )

    STATUS_CHOICES = (
        ('Issued', 'Issued'), # ticket raised but not assigned
        ('In Process', 'In Process'), # ticket assigned
        ('Resolved', 'Resolved'), # ticket resolved
        ('Cancelled', 'Cancelled'),
    )

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    severity = models.PositiveIntegerField(choices=SEVERITY_CHOICES)
    description = models.CharField(max_length=255)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Issued')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    expiry = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Here we over-ride the default `save` method to populate the expiry field
        based on creation date, holidays and weekends.
        """
        self.expiry = findExpiryDate(self.severity)

        super().save(*args, **kwargs)  # Call the "real" save() method.


    def __str__(self):
        return "{} | {} | {} ".format(self.vendor.vendor, self.category.category, self.created_at)


def findExpiryDate(sla):
    """
    Finds the expiry date for a ticket based on
    1. Severity of the ticket
    2. Date of issue
    """
    now = datetime.now()
    flag = 1

    # if ticket is received today between 00:00 hours to Start_Hour
    # we reset the flag
    if now.hour < START_HOUR:
        flag = 0

    # if ticket is received today between office hours then
    # we simply deduct working hours left today from sla
    if START_HOUR < now.hour < END_HOUR:
        hoursLeftToday = END_HOUR - sla
        sla -= hoursLeftToday

    tomorrow = date.today() + timedelta(days=flag)
    shiftTime = time(START_HOUR,0,0)
    dt = datetime.combine(tomorrow, shiftTime)
    dt = adjust_Weekends_And_Holidays(dt) # adjust incase we hit a weekend


    # now we find the office days and office hours
    # we would need to complete the sla
    days, hours = divmod(sla, workingHours)

    dt += timedelta(hours=hours)
    dt = adjust_Weekends_And_Holidays(dt, days=days) # adjust incase we hit a weekend

    return dt

def isWeekend(dt):
    """Finds if a date lies on a weekend or not. Returns a boolean"""
    if 0 < dt.weekday() < 6:
        return False
    else:
        return True

def isHoliday(dt):
    """Finds if a date lies on a holiday or not. Returns a boolean"""
    return Holiday.objects.filter(day=dt.date()).exists()

def adjust_Weekends_And_Holidays(dt, days=0):
    """
    Adjust the datetime to a future datetime accomodating for
    1. days needed
    2. skipping Weekends
    """
    while isWeekend(dt) or isHoliday(dt):
        dt += timedelta(days=1)

    while days:
        dt += timedelta(days=1)
        if isWeekend(dt) or isHoliday(dt):
            continue
        else:
            days -= 1

    return dt
