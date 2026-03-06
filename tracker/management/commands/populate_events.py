import csv
import re
from django.core.management.base import BaseCommand
from tracker.models import Event


class Command(BaseCommand):
    help = 'Populate Event records from AT D1 Events CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the AT D1 Events CSV file',
            default=r'c:\Users\gordo\Downloads\AT D1 Events.csv',
            nargs='?'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        created_count = 0
        error_count = 0

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    event_string = row.get('Event Name', '').strip()
                    
                    if not event_string:
                        continue
                    
                    # Parse the event string: "Gender Grade Grade Event Name"
                    # Example: "Girls C Grade High Jump"
                    parts = event_string.split()
                    
                    if len(parts) < 4:
                        self.stdout.write(
                            self.style.WARNING(f'Skipping invalid event: {event_string}')
                        )
                        error_count += 1
                        continue
                    
                    gender = parts[0]  # "Girls" or "Boys"
                    grade_letter = parts[1]  # "A", "B", or "C"
                    # parts[2] is "Grade"
                    event_name = ' '.join(parts[3:])  # "High Jump", "Shot Put", etc.
                    
                    # Validate grade
                    if grade_letter not in ['A', 'B', 'C']:
                        self.stdout.write(
                            self.style.WARNING(f'Invalid grade in: {event_string}')
                        )
                        error_count += 1
                        continue
                    
                    # Validate gender
                    if gender not in ['Boys', 'Girls']:
                        self.stdout.write(
                            self.style.WARNING(f'Invalid gender in: {event_string}')
                        )
                        error_count += 1
                        continue
                    
                    # Create or get the event
                    event, created = Event.objects.get_or_create(
                        grade=grade_letter,
                        gender=gender,
                        event_name=event_name,
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Created: {event}')
                        )
                        created_count += 1
                    else:
                        self.stdout.write(f'Already exists: {event}')
        
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'CSV file not found: {csv_file}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Completed! Created {created_count} events, {error_count} errors.'
            )
        )
