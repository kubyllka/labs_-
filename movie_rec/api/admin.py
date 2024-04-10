from django.contrib import admin
from .models import Movie
from .models import Keyword
from .models import Genre

admin.site.register(Movie)
admin.site.register(Keyword)
admin.site.register(Genre)