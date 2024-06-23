
from django.contrib import admin
from .models import Child, AdoptionRequest, User
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin

class MyAdminSite(AdminSite):
    site_header = 'Adoption App Administration'
    site_title = 'Adoption Admin Portal'
    index_title = 'Welcome to the Adoption Admin Portal'

admin_site = MyAdminSite(name='myadmin')


class ChildAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'is_adopted')
    search_fields = ('name',)

# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email' , 'first_name' , 'last_name')
#     search_fields = ('username', 'email' , 'first_name' , 'last_name')

class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'child', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'child__name')
    ordering = ('-created_at',)
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for request in queryset:
            request.status = 'approved'
            request.save()
        self.message_user(request, f"{queryset.count()} requests have been approved.")
    approve_requests.short_description = 'Approve selected requests'

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} requests have been rejected.")
    reject_requests.short_description = 'Reject selected requests'



# admin_site.register(User , UsersAdmin)
admin_site.register(Child , ChildAdmin)
admin_site.register(AdoptionRequest, AdoptionRequestAdmin)
admin_site.register(User, UserAdmin)

