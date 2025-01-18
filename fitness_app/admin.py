"""from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, MuscleGroup, Exercise, NutritionRecommendation

# Custom UserAdmin for the Account model
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'experience_level', 'dietary_preferences', 'medical_conditions', 'phone_number', 'country', 'password1', 'password2', 'is_admin', 'is_staff'),
        }),
    )

# Registering the models with the custom admin
admin.site.register(Account, AccountAdmin)
admin.site.register(MuscleGroup)
admin.site.register(Exercise)
#admin.site.register(WorkoutProgram)
admin.site.register(NutritionRecommendation)
"""

from django.contrib import admin
from .models import (
    Account, 
    MuscleGroup, 
    Exercise, 
    NutritionRecommendation, 
    Trainer, 
    ReviewOnTrainers, 
    ReviewOnWebsite
)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active', 'gender', 'fitness_goal', 'activity_level', 'experience_level')
    search_fields = ('email', 'username', 'gender', 'fitness_goal', 'activity_level', 'experience_level')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)

    filter_horizontal = ()
    list_per_page = 25

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'experience_level', 'phone_number', 'country', 'dietary_preferences', 'medical_conditions', 'profile_image')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin'),
        }),
    )


class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('muscle_groups',)
    list_filter = ('muscle_groups',)


class NutritionRecommendationAdmin(admin.ModelAdmin):
    list_display = ('meal', 'ingredients', 'instructions')
    search_fields = ('meal',)


class TrainerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'specialty', 'experience_years')
    search_fields = ('first_name', 'last_name', 'email', 'specialty')
    list_filter = ('specialty', 'experience_years')


class ReviewOnTrainersAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'user', 'rating', 'created_at')
    search_fields = ('trainer__first_name', 'trainer__last_name', 'user__username')
    list_filter = ('rating', 'created_at')


class ReviewOnWebsiteAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('rating', 'created_at')


admin.site.register(Account, AccountAdmin)
admin.site.register(MuscleGroup, MuscleGroupAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(NutritionRecommendation, NutritionRecommendationAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(ReviewOnTrainers, ReviewOnTrainersAdmin)
admin.site.register(ReviewOnWebsite, ReviewOnWebsiteAdmin)
