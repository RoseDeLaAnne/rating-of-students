from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _


from .models import *




class UserAdmin(UserAdmin):
    search_fields = (
        'username',
        'email',
        'phone_number',
        'last_name',
        'first_name',
        'middle_name',
    )

    ordering = (
        '-date_joined',
    )

    list_display = (
        'username',
        'email',
        'phone_number',
        'last_name',
        'first_name',
        'middle_name',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
    )
    
    fieldsets = (
        (None, {
            'fields': (
                'avatar',
            ),
        }),
        (None, {
            'fields': (
                'password',
            ),
        }),
        (_('Персональная информация'), {
            'fields': (
                'username',
                'email',
                'phone_number',
                'last_name',
                'first_name',
                'middle_name',
            ),
        }),
        (_('Права доступа'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
        (_('Важные даты'), {
            'fields': (
                'last_login',
                'date_joined',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'avatar',
            ),
        }),
        (None, {
            'fields': (
                'password1',
                'password2',
            ),
        }),
        (_('Персональная информация'), {
            'fields': (
                'username',
                'email',
                'phone_number',
                'last_name',
                'first_name',
                'middle_name',
            ),
        }),
        (_('Права доступа'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
        (_('Важные даты'), {
            'fields': (
                'date_joined',
            ),
        }),
    )

class StudentAdmin(admin.ModelAdmin):
    search_fields = (
        'user__username',
        'user__email',
        'user__phone_number',
        'user__last_name',
        'user__first_name',
        'user__middle_name',
    )

    ordering = (
        '-user__date_joined',
    )

    list_display = (
        'student_code',
        # 'department',
        'speciality',
        'course',
        'rating',
    )

    list_filter = (
        # 'department',
        'speciality',
        'course',
        'user__is_active',
        'user__is_staff',
        'user__is_superuser',
    )
    
    fieldsets = (
        (None, {
            'fields': (
                'user',
            ),
        }),
        (None, {
            'fields': (
                'student_code',
            ),
        }),
        (_('Персональная информация'), {
            'fields': (
                # 'department',
                'speciality',
                'course',
            ),
        }),
        (_('Рейтинг'), {
            'fields': (
                'rating',
                'rating_study',
                'rating_science',
                'rating_innovations',
                'rating_culture',
                'rating_sport',
                'rating_work',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'user',
            ),
        }),
        (None, {
            'fields': (
                'student_code',
            ),
        }),
        (_('Персональная информация'), {
            'fields': (
                # 'department',
                'speciality',
                'course',
            ),
        }),
        (_('Рейтинг'), {
            'fields': (
                'rating',
                'rating_study',
                'rating_science',
                'rating_innovations',
                'rating_culture',
                'rating_sport',
                'rating_work',
            ),
        }),
    )

class ProfessorAdmin(admin.ModelAdmin):
    search_fields = (
        'user__username',
        'user__email',
        'user__phone_number',
        'user__last_name',
        'user__first_name',
        'user__middle_name',
    )

    ordering = (
        '-user__date_joined',
    )

    list_display = (
        'user',
    )

    list_filter = (
        'user__is_active',
        'user__is_staff',
        'user__is_superuser',
    )
    
    fieldsets = (
        (None, {
            'fields': (
                'user',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'user',
            ),
        }),
    )


class ApplicationAdmin(admin.ModelAdmin):
    search_fields = (
        'event',
        'role',
        'status',
    )

    ordering = (
        '-date_sended',
    )

    list_display = (
        'event',
        'sender',
        'recipient',
        'role',
        'status',
        'date_sended',
    )

    list_filter = (
        'role',
        'status',
    )

    fieldsets = (
        (None, {
            'fields': (
                'event',
            ),
        }),
        (None, {
            'fields': (
                'sender',
                'recipient',
            ),
        }),
        (None, {
            'fields': (
                'role',
                'status',
            ),
        }),
        (_('Важные даты'), {
            'fields': (
                'date_sended',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'event',
            ),
        }),
        (None, {
            'fields': (
                'sender',
                'recipient',
            ),
        }),
        (None, {
            'fields': (
                'role',
                'status',
            ),
        }),
        (_('Важные даты'), {
            'fields': (
                'date_sended',
            ),
        }),
    )

    # def delete(self, *args, **kwargs):
    #     print('delete / applications (admin.py)')
    #     super(Application, self).delete(*args, **kwargs)

    #     self.recipient.save()

    def delete_queryset(self, *args, **kwargs):
        print('delete many / applications (admin.py)')
        for obj in args[1]:
            super(Application, obj).delete()

        args[1][0].recipient.save()

class EventAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )

    ordering = (
        '-date_start',
        '-date_end',
    )

    list_display = (
        'name',
        'creator',
        'category',
        'status',
        'date_start',
        'date_end',
    )

    list_filter = (
        'category',
        'status',
    )

    fieldsets = (
        (None, {
            'fields': (
                'image',
            ),
        }),
        (None, {
            'fields': (
                'creator',
            ),
        }),
        (None, {
            'fields': (
                'name',
            ),
        }),
        (None, {
            'fields': (
                'category',
            ),
        }),
        (None, {
            'fields': (
                'status',
            ),
        }),
        (_('Важные даты'), {
            'fields': (
                'date_start',
                'date_end',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'image',
            ),
        }),
        (None, {
            'fields': (
                'creator',
            ),
        }),
        (None, {
            'fields': (
                'name',
            ),
        }),
        (None, {
            'fields': (
                'category',
            ),
        }),
        (None, {
            'fields': (
                'status',
            ),
        }),
        (_('Важные даты'), {
            'fields': (
                'date_start',
                'date_end',
            ),
        }),
    )


    def delete_queryset(one, second, third):
        print('delete many / events (admin.py)')
        for i in third:
            for y in i.application_set.all():
                y.delete()
            super(Event, i).delete()

class SpecialityAdmin(admin.ModelAdmin):
    search_fields = (
        'speciality',
    )

    ordering = (
        'speciality',
    )

    list_display = (
        'speciality',
        'department',
    )

    fieldsets = (
        (None, {
            'fields': (
                'speciality',
            ),
        }),
        (None, {
            'fields': (
                'department',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'speciality',
            ),
        }),
        (None, {
            'fields': (
                'department',
            ),
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    search_fields = (
        'category',
    )

    ordering = (
        'category',
    )

    list_display = (
        'category',
    )

    fieldsets = (
        (None, {
            'fields': (
                'category',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'category',
            ),
        }),
    )

class RoleAdmin(admin.ModelAdmin):
    search_fields = (
        'role',
    )

    ordering = (
        'role',
    )

    list_display = (
        'role',
        'points',
    )

    fieldsets = (
        (None, {
            'fields': (
                'role',
            ),
        }),
        (None, {
            'fields': (
                'points',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'role',
            ),
        }),
        (None, {
            'fields': (
                'points',
            ),
        }),
    )

class DepartmentAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )

    list_display = (
        'name',
        'head',
    )

    fieldsets = (
        (None, {
            'fields': (
                'name',
            ),
        }),
        (None, {
            'fields': (
                'head',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'name',
            ),
        }),
        (None, {
            'fields': (
                'head',
            ),
        }),
    )

class ThemeAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )

    list_display = (
        'name',
    )

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'theme',
            ),
        }),
        (None, {
            'fields': (
                'users',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'name',
                'theme',
            ),
        }),
        (None, {
            'fields': (
                'users',
            ),
        }),
    )

class CustomizationAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
        'value',
    )

    ordering = (
        'name',
    )

    list_display = (
        'name',
        'value',
    )

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'value',
            ),
        }),
        (None, {
            'fields': (
                'users',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'name',
                'value',
            ),
        }),
        (None, {
            'fields': (
                'users',
            ),
        }),
    )

class FeedbackAdmin(admin.ModelAdmin):
    search_fields = (
        'comment',
        'points',
    )

    ordering = (
        '-date_sended',
    )

    list_display = (
        'user',
        'rating',
        'comment',
        'points',
        'status',
        'date_sended',
    )

    list_filter = (
        'rating',
        'status',
    )

    fieldsets = (
        (None, {
            'fields': (
                'user',
            ),
        }),
        (None, {
            'fields': (
                'rating',
                'comment',
                'points',
            ),
        }),
        (None, {
            'fields': (
                'status',
            ),
        }),
        (_('Важные даты'), {
            'fields': (
                'date_sended',
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'user',
            ),
        }),
        (None, {
            'fields': (
                'rating',
                'comment',
                'points',
            ),
        }),
        (None, {
            'fields': (
                'status',
            ),
        }),
        (_('Важные даты'), {
            'fields': (
                'date_sended',
            ),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)
# admin.site.register(Theme, ThemeAdmin)
# admin.site.register(Customization, CustomizationAdmin)
# admin.site.register(Feedback, FeedbackAdmin)

admin.site.unregister(Group)
