from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, EventForm, FeedbackForm, UserProfileForm
from .models import Event, UserProfile
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile, CustomUser
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from .models import EventRegistration
from .utils import nlp_search
from django.contrib import messages

# Home view
def home(request):
    return render(request, 'home.html')

# Registration view using class-based view
class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/login/' 

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_mail(
            'Welcome!',
            'Thank you for registering.',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

# Event detail view
@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})

# View for user's registered events
@login_required
def my_registrations(request):
    registrations = EventRegistration.objects.filter(user=request.user)
    return render(request, 'my_registrations.html', {'registrations': registrations})

# Event recommendation view
@login_required
def event_recommendations(request):
    try:
        # Assuming request.user is a CustomUser instance
        user = request.user

        # Ensure user is a CustomUser instance, if not, fetch it
        if not isinstance(user, CustomUser):
            user = CustomUser.objects.get(username=user.username)

        # Fetch the UserProfile for the user
        user_profile = UserProfile.objects.get(user=user)
        
        # Your logic here
        
    except ObjectDoesNotExist:
        # Handle the case where UserProfile does not exist for the user
        user_profile = None
        
    return render(request, 'event_recommendations.html', {'user_profile': user_profile})


# Feedback view
@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # You can save the feedback data to the database manually or send an email
            # Example: Feedback.objects.create(name=name, email=email, message=message)
            
            # Redirect to a success page
            return render(request, 'thank_you.html')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback.html', {'form': form})

# Thank you page for feedback
@login_required
class FeedbackThankYouView(TemplateView):
    template_name = 'thank_you.html'

# Admin management view
@login_required
def admin_manage(request):
    return render(request, 'admin_manage.html')

# Event dashboard view
@login_required
def event_dashboard_view(request):
    events = Event.objects.all()  # Adjust this query based on your needs
    context = {'events': events}
    return render(request, 'event_dashboard.html', context)

# View for user-created events
@login_required
def my_events_view(request):
    events = Event.objects.filter(creator=request.user)
    return render(request, 'events/my_events.html', {'events': events})

# Update profile view
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Adjust the redirect URL as needed
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'form': form})

# Thank you page view for feedback submission
@login_required
def feedback_thank_you(request):
    return render(request, 'feedback/thank_you.html')

# Custom event creation view
@login_required
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('event_list')  # Redirect to the event list page
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})
    
class EventDashboardView(TemplateView):
    template_name = 'event_dashboard.html'

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')
    
    def get(self, request):
        logout(request)
        return redirect('login')
    
def event_list(request):
    print("Event List View Called")  # This should print in your terminal when the view is accessed
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events}) 

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)  # Don't save to the database yet
            event.creator = request.user  # Assign the logged-in user as the creator
            event.save()  # Now save the event with the creator assigned
            return redirect('event_dashboard')  # Redirect to your desired page
    else:
        form = EventForm()

    return render(request, 'events/event_create.html', {'form': form})

def search_events(request):
    query = request.GET.get('query', '')
    sort = request.GET.get('sort', 'date')

    events = []
    if query:
        events = nlp_search(query)  # Use your NLP function to get relevant events

        if sort == 'start_time':
            events = events.order_by('start_time')
        elif sort == 'location':
            events = events.order_by('location')
        elif sort == 'title':
            events = events.order_by('title')

    context = {
        'query': query,
        'events': events,
        'sort': sort,
    }

    return render(request, 'search_results.html', {'events': events})

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the user has already registered for this event
    if EventRegistration.objects.filter(user=request.user, event=event).exists():
        messages.error(request, "You have already registered for this event.")
        return redirect('event_detail', pk=event.id)
    
    # Register the user for the event
    EventRegistration.objects.create(user=request.user, event=event)
    messages.success(request, f"Successfully registered for {event.title}!")

    return redirect('event_detail', pk=event.id)
