from django.urls import path
from .views import (
    RegisterView, LoginView, UserView, LogoutView, MuscleGroupView, ExerciseView, 
    NutritionRecommendationView, NutritionDetailByMealView, WorkoutRecommendationView, MealRecommendationView, ExercisesByMuscleGroupView, ExerciseByNameView, TrainerListView, TrainerDetailView, ReviewListCreateView, TrainerReviewListView, UserProfileUpdateView, PasswordResetRequestView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView, AddReviewOnWebsiteView, EditReviewOnWebsiteView, ReviewsOnWebsiteListView, AllReviewsOnWebsiteListView, csrf_token,
    bmi_calculator_view, bmr_calculator_view, calorie_needs_view, body_fat_calculator_view, whr_calculator_view
)
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('user/update/', UserProfileUpdateView.as_view(), name='user-update'),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('csrf-token/', csrf_token),
    #path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    #path('password-reset/done/', PasswordResetDoneView.as_view(), name='password-reset-done'),
    #path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    #path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('password-reset/', 
        PasswordResetRequestView.as_view(), 
        name='password_reset'
    ),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ), 
        name='password_reset_done'
    ),
    path('password-reset-confirm/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'
    ),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ), 
        name='password_reset_complete'
    ),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password-change-done'),
    path('muscle-groups/', MuscleGroupView.as_view()),
    path('exercises/', ExerciseView.as_view()),
    #path('workout-programs/', WorkoutProgramView.as_view()),
    path('nutrition-recommendations/', NutritionRecommendationView.as_view()),
    path('nutrition-recommendation/<str:meal>/', NutritionDetailByMealView.as_view(), name='nutrition-recommendation-detail'),
    path('workout-recommendations/', WorkoutRecommendationView.as_view()),
    path('bmi-calculator/', bmi_calculator_view),
    path('bmr-calculator/', bmr_calculator_view),
    path('calorie-needs/', calorie_needs_view),
    path('body-fat-calculator/', body_fat_calculator_view),
    path('whr-calculator/', whr_calculator_view),
    path('meal-recommendations/', MealRecommendationView.as_view()),
    path('exercises/muscle-group/<str:muscle_group>/', ExercisesByMuscleGroupView.as_view(), name='exercises-by-muscle-group'),
    path('exercises/name/<str:name>/', ExerciseByNameView.as_view(), name='exercise-by-name'),
    path('trainers/', TrainerListView.as_view(), name='trainer-list'),
    path('trainers/<int:pk>/', TrainerDetailView.as_view(), name='trainer-detail'),
    path('reviews/trainers', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/trainer/<int:trainer_id>/', TrainerReviewListView.as_view(), name='trainer-review-list'),
    path('reviews/website', AddReviewOnWebsiteView.as_view(), name='add_review'),
    path('reviews/website/edit/<int:review_id>/', EditReviewOnWebsiteView.as_view(), name='edit_review'),
    path('reviews/website/list', ReviewsOnWebsiteListView.as_view(), name='review-list'),
    path('reviews/website/list/all', AllReviewsOnWebsiteListView.as_view(), name='review-list-all'),
]