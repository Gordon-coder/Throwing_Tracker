import csv
from django.core.management.base import BaseCommand
from tracker.models import Event, Competitor


class Command(BaseCommand):
    help = 'Populate Events and Competitors from events_data.csv and competitors_data.csv'

    def handle(self, *args, **options):
        # Import events
        events_created = 0
        try:
            with open('events_data.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 3:
                        continue
                    event_name, gender, qualifying_distance = row
                    qualifying_distance = float(qualifying_distance)
                    
                    event, created = Event.objects.get_or_create(
                        event_name=event_name,
                        gender=gender,
                        group=2,  # Assume group 1
                        defaults={
                            'qualifying_distance': qualifying_distance,
                            'grade': None
                        }
                    )
                    if created:
                        events_created += 1
                        self.stdout.write(f'Created event: {event}')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('events_data.csv not found'))
            return
        
        # Import competitors
        competitors_created = 0
        try:
            with open('competitors_data.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 6:
                        continue
                    gender, event_name, group, position, name, school = row
                    group = int(group)
                    position = int(position)
                    
                    # Find the event
                    try:
                        event = Event.objects.get(
                            event_name=event_name,
                            gender=gender,
                            group=group
                        )
                    except Event.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'Event not found for {gender} {event_name} Group {group}')
                        )
                        continue
                    
                    competitor, created = Competitor.objects.get_or_create(
                        number=position,  # Use position as number
                        event=event,
                        defaults={
                            'name': name,
                            'school': school
                        }
                    )
                    if created:
                        competitors_created += 1
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('competitors_data.csv not found'))
            return
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {events_created} events and {competitors_created} competitors')
        )