from django.db import models

# Create your models here.
class Competitor(models.Model):
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    number = models.IntegerField()
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    def __str__(self):
        return f"#{self.number}, {self.name}, {self.school} ({self.event})"
    
class Throw(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    distance = models.FloatField()

    def __str__(self):
        return f"{self.competitor.name} - {self.distance}m"
    
class Event(models.Model):
    GRADE_CHOICES = [
        ('A', 'A Grade'),
        ('B', 'B Grade'),
        ('C', 'C Grade'),
    ]
    GENDER_CHOICES = [
        ('Boys', 'Boys'),
        ('Girls', 'Girls'),
    ]
    EVENT_CHOICES = [
        ('High Jump', 'High Jump'),
        ('Shot Put', 'Shot Put'),
        ('Javelin', 'Javelin'),
        ('Triple Jump', 'Triple Jump'),
        ('Long Jump', 'Long Jump'),
        ('Discus', 'Discus'),
    ]
    
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    event_name = models.CharField(max_length=100, choices=EVENT_CHOICES, null=True, blank=True)
    group = models.IntegerField(null=True, blank=True)

    qualifying_distance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.gender} {self.grade} Grade {self.event_name} Group {self.group if self.group else ''}"