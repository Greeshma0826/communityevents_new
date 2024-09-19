from .models import Event
import re
from datetime import datetime
from django.db.models import Q

def get_recommended_events(user_profile):
    # Update this filter according to the actual fields in UserProfile
    recommended_events = Event.objects.filter(category=user_profile.some_other_field)
    return recommended_events

def nlp_search(query):
    """
    Process the natural language query to search for relevant events.

    Args:
        query (str): The search query entered by the user.

    Returns:
        QuerySet: A Django QuerySet of Event objects that match the search criteria.
    """

    # Preprocess the query (e.g., remove extra spaces, convert to lowercase)
    query = query.strip().lower()

    # Initialize query parameters
    title_keywords = []
    location_keywords = []
    date_range = None
    category = None

    # Extract keywords and possible categories or dates from the query
    if "category:" in query:
        category = re.search(r"category:(\w+)", query).group(1)

    if "date:" in query:
        date_str = re.search(r"date:(\d{4}-\d{2}-\d{2})", query)
        if date_str:
            try:
                date_range = datetime.strptime(date_str.group(1), "%Y-%m-%d").date()
            except ValueError:
                date_range = None

    # Split the query into keywords
    words = re.split(r'\s+', query)
    for word in words:
        if word not in ["category:", "date:"]:
            if "location" in word:
                location_keywords.append(word)
            else:
                title_keywords.append(word)

    # Build the search query
    search_query = Q()
    if title_keywords:
        search_query &= Q(title__icontains=' '.join(title_keywords))

    if location_keywords:
        search_query &= Q(location__icontains=' '.join(location_keywords))

    if date_range:
        search_query &= Q(date=date_range)

    if category:
        search_query &= Q(category=category)

    # Execute the search query
    events = Event.objects.filter(search_query)

    return events