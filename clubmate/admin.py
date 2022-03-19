from django.contrib import admin
from clubmate.models import Club, UserProfile, Rating, Event


class RatingAdmin(admin.ModelAdmin):
    ordering = ('-posted_at',)
    list_display = ('posted_at', 'title', 'club', 'author', 'rating_score', 'is_safe', 'user_commentary', 'number_of_upvotes')


admin.site.register(Rating, RatingAdmin)
admin.site.register(Club)
admin.site.register(UserProfile)
admin.site.register(Event)