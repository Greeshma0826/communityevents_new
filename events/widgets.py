# widgets.py

from django import forms # type: ignore

class StarRatingWidget(forms.RadioSelect):
    template_name = 'widgets/star_rating.html'
