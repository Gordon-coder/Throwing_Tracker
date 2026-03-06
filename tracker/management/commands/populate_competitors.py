import csv
from django.core.management.base import BaseCommand
from tracker.models import Competitor, Event


class Command(BaseCommand):
    help = 'Populate Competitor records from AT D1 Competitors CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the AT D1 Competitors CSV file',
            default=r'c:\Users\gordo\Downloads\AT D1 Competitors.csv',
            nargs='?'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        created_count = 0
        skipped_count = 0
        error_count = 0

        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        comp_id = row.get('id', '').strip()
                        number = row.get('number', '').strip()
                        name = row.get('name', '').strip()
                        school = row.get('school', '').strip()
                        event_string = row.get('event', '').strip()
                        
                        if not all([number, name, school, event_string]):
                            self.stdout.write(
                                self.style.WARNING(f'Skipping incomplete row: {row}')
                            )
                            skipped_count += 1
                            continue
                        
                        # Find the matching Event
                        try:
                            # Event string format: "Gender Grade Grade Event Name"
                            # Example: "Girls C Grade High Jump"
                            parts = event_string.split()
                            
                            if len(parts) < 4:
                                self.stdout.write(
                                    self.style.WARNING(f'Invalid event format: {event_string}')
                                )
                                error_count += 1
                                continue
                            
                            gender = parts[0]  # "Girls" or "Boys"
                            grade = parts[1]   # "A", "B", or "C"
                            # parts[2] is "Grade"
                            event_name = ' '.join(parts[3:])  # "High Jump", etc.
                            
                            event = Event.objects.get(
                                gender=gender,
                                grade=grade,
                                event_name=event_name
                            )
                        except Event.DoesNotExist:
                            self.stdout.write(
                                self.style.ERROR(f'Event not found: {event_string}')
                            )
                            error_count += 1
                            continue
                        
                        # Create or get the competitor
                        competitor, created = Competitor.objects.get_or_create(
                            number=int(number),
                            name=name,
                            school=school,
                            event=event,
                        )
                        
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'Created: #{competitor.number} {competitor.name} ({competitor.school}) - {competitor.event}'
                                )
                            )
                            created_count += 1
                        else:
                            skipped_count += 1
                    
                    except ValueError as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error parsing row {row}: {str(e)}')
                        )
                        error_count += 1
                        continue
        
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'CSV file not found: {csv_file}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Completed! Created {created_count} competitors, '
                f'Skipped {skipped_count}, Errors: {error_count}'
            )
        )
