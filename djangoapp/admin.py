

# Register your models here.
from django.contrib import admin
from .models import Tourpakage, Booking, UserProfile

@admin.register(Tourpakage)
class TourpakageAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'price', 'trending', 'is_active', 'is_approved')
    list_filter = ('is_active', 'is_approved', 'trending')
    search_fields = ('title', 'location', 'vendor__username')
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} package(s) approved.")
    approve_selected.short_description = "Approve selected packages"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'booking_date', 'number_of_people', 'status')
