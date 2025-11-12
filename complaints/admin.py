from django.contrib import admin
from .models import Complaint, ElectricityBill


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'created_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    
    fieldsets = (
        ('Complaint Information', {
            'fields': ('user', 'title', 'description', 'category')
        }),
        ('Status Information', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )


@admin.register(ElectricityBill)
class ElectricityBillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'user', 'consumer_name', 'amount', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'due_date', 'created_at')
    search_fields = ('bill_number', 'consumer_name', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    
    fieldsets = (
        ('Bill Information', {
            'fields': ('user', 'bill_number', 'consumer_name', 'address', 'amount', 'due_date')
        }),
        ('Status Information', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )