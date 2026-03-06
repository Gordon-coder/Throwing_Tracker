from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Max
from .models import Competitor, Throw, Event


# Create your views here.
def index(request):
    # Get all events
    all_events = Event.objects.all().order_by('gender','event_name','grade')
    
    # Get selected event from GET or POST parameters
    selected_event_id = request.GET.get('event') or request.POST.get('event')
    if not selected_event_id:
        selected_event_id = 9
    selected_event = None
    
    if selected_event_id:
        try:
            selected_event = Event.objects.get(pk=int(selected_event_id))
        except (Event.DoesNotExist, ValueError):
            selected_event = Event.objects.get(pk=9)
    
    # Handle form submission to record a new throw or delete an existing one
    if request.method == 'POST':
        # Deleting a throw (each delete button posts 'delete_throw' with the throw id)
        if 'delete_throw' in request.POST:
            throw_id = request.POST.get('delete_throw')
            try:
                t = Throw.objects.get(pk=int(throw_id))
                t.delete()
                messages.success(request, f'Deleted throw {throw_id}.')
                if selected_event:
                    return redirect(f'/?event={selected_event.id}')
                return redirect('index')
            except (Throw.DoesNotExist, ValueError):
                messages.error(request, 'Throw not found.')

        # Otherwise assume creating a new throw
        competitor_id = request.POST.get('competitor')
        distance = request.POST.get('distance')

        if not competitor_id or not distance:
            messages.error(request, 'Please select a competitor and enter a distance.')
        else:
            try:
                competitor = Competitor.objects.get(pk=int(competitor_id))
                distance_val = float(distance)
                Throw.objects.create(competitor=competitor, distance=distance_val)
                messages.success(request, f'Recorded {distance_val}m for {competitor.name}.')
                # Redirect with the same event filter
                if selected_event:
                    return redirect(f'/?event={selected_event.id}')
                return redirect('index')
            except Competitor.DoesNotExist:
                messages.error(request, 'Selected competitor not found.')
            except ValueError:
                messages.error(request, 'Distance must be a number.')

    # Filter competitors by selected event and prefetch throws for display
    if selected_event:
        base_qs = Competitor.objects.filter(event=selected_event).prefetch_related('throw_set').order_by('number')
    else:
        base_qs = Competitor.objects.all().prefetch_related('throw_set').order_by('number')

    competitors = base_qs
    rankings = base_qs.annotate(best=Max('throw__distance')).order_by('-best', 'number')

    # Evaluate rankings and attach ordered throws to each competitor to avoid N+1 queries in template
    rankings = list(rankings)
    for person in rankings:
        # order throws by distance descending, then by id (most recent first for ties)
        person.throws = person.throw_set.order_by('-distance', '-id')

    return render(request, 'tracker/index.html', {
        'competitors': competitors,
        'rankings': rankings,
        'all_events': all_events,
        'selected_event': selected_event,
    })