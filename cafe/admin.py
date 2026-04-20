from django.contrib import admin
from .models import MenuItem, TableBooking, CafeTiming


@admin.register(CafeTiming)
class CafeTimingAdmin(admin.ModelAdmin):
    list_display = ['name', 'opening_time', 'closing_time', 'updated_at']
    fields = ['name', 'opening_time', 'closing_time']
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion if there's only one cafe timing
        if CafeTiming.objects.count() == 1:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Item Information', {
            'fields': ('name', 'category', 'price', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
    )
    list_editable = ['is_available']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'time', 'number_of_people', 'status', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('date', 'time', 'number_of_people', 'special_requests')
        }),
        ('Status & User', {
            'fields': ('status', 'user')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_editable = ['status']
    
    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} bookings marked as confirmed.')
    mark_confirmed.short_description = 'Mark selected as confirmed'
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} bookings marked as completed.')
    mark_completed.short_description = 'Mark selected as completed'
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} bookings marked as cancelled.')
    mark_cancelled.short_description = 'Mark selected as cancelled'
