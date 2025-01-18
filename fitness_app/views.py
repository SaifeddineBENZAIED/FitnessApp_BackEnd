import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.db.models import Avg
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .models import Account, MuscleGroup, Exercise, NutritionRecommendation, Trainer, ReviewOnTrainers, ReviewOnWebsite
from .serializers import AccountSerializer, MuscleGroupSerializer, ExerciseSerializer, NutritionRecommendationSerializer, TrainerSerializer, ReviewOnTrainersSerializer, ReviewOnWebsiteSerializer
from .forms import RegistrationForm, LoginForm, BMICalculatorForm, BMRCalculatorForm, CalorieNeedsForm, BodyFatCalculatorForm, WHRCalculatorForm
from .calculators import calculate_bmi, calculate_bmr, calculate_calorie_needs, calculate_body_fat_percentage, calculate_whr

import numpy as np
import joblib
import pandas as pd

from django.contrib.auth import get_user_model

@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)  # Ensure correct parsers for file uploads

    def post(self, request):
        print("Received data:", request.data)  # Log the incoming request data
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)  # Log validated data before saving
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Errors:", serializer.errors)  # Log any validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)"""

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(request, username=email, password=password)
        if user is None:
            raise AuthenticationFailed('User not found or incorrect password!')

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    
class UserProfileUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = AccountSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email:
            form = PasswordResetForm(data={'email': email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    token_generator=default_token_generator,
                    from_email=None,
                    email_template_name='password_reset_email.html',
                )
                return Response({"detail": "Password reset email has been sent."}, status=200)
            return Response(form.errors, status=400)
        return Response({"detail": "Email is required."}, status=400)"""

"""class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email:
            form = PasswordResetForm(data={'email': email})
            if form.is_valid():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                print(f'UIDB64 for {email}: {uidb64}')

                form.save(
                    request=request,
                    use_https=request.is_secure(),
                    token_generator=default_token_generator,
                    from_email=None,
                    email_template_name='password_reset_email.html',
                )
                print('Password reset link sent to ', email)
                return Response({"detail": "Password reset email has been sent."}, status=200)
            return Response(form.errors, status=400)
        return Response({"detail": "Email is required."}, status=400)"""

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email:
            form = PasswordResetForm(data={'email': email})
            if form.is_valid():
                try:
                    form.save(
                        request=request,
                        use_https=request.is_secure(),
                        token_generator=default_token_generator,
                        from_email=None,
                        email_template_name='password_reset_email.html',
                    )
                    return JsonResponse({"detail": "Password reset email has been sent."}, status=200)
                except Exception as e:
                    return JsonResponse({"error": str(e)}, status=500)
            return JsonResponse(form.errors, status=400)
        return JsonResponse({"detail": "Email is required."}, status=400)


"""class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64=None, token=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.data)
            if form.is_valid():
                form.save()
                return Response({"detail": "Password has been reset."}, status=200)
            return Response(form.errors, status=400)
        return Response({"detail": "Invalid token."}, status=400)"""

"""class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64=None, token=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            print('Decoded uid:', uid)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            print('Error decoding uidb64', e)
            user = None

        if user and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.data)
            if form.is_valid():
                form.save()
                return Response({"detail": "Password has been reset."}, status=200)
            return Response(form.errors, status=400)
        return Response({"detail": "Invalid token."}, status=400)"""

User = get_user_model()

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64=None, token=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return JsonResponse({'valid': True, 'uid': uidb64, 'token': token}, status=200)
        else:
            return JsonResponse({'valid': False, 'message': 'Invalid or expired link.'}, status=400)

    def post(self, request, uidb64=None, token=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.data)
            if form.is_valid():
                form.save()
                return JsonResponse({"detail": "Password has been reset successfully."}, status=200)
            return JsonResponse(form.errors, status=400)
        return JsonResponse({"detail": "Invalid token."}, status=400)


class PasswordChangeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        form = SetPasswordForm(user, request.data)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return Response({"detail": "Password changed successfully."}, status=200)
        return Response(form.errors, status=400)

class PasswordResetDoneView(PasswordResetDoneView):
    pass  # Use Django's built-in view

class PasswordResetCompleteView(PasswordResetCompleteView):
    pass  # Use Django's built-in view

class PasswordChangeDoneView(PasswordChangeDoneView):
    pass  # Use Django's built-in view

class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = AccountSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

class MuscleGroupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        muscle_groups = MuscleGroup.objects.all()
        serializer = MuscleGroupSerializer(muscle_groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MuscleGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExerciseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""class WorkoutProgramView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        programs = WorkoutProgram.objects.all()
        serializer = WorkoutProgramSerializer(programs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkoutProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""

class NutritionRecommendationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommendations = NutritionRecommendation.objects.all()
        serializer = NutritionRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NutritionRecommendationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NutritionDetailByMealView(generics.RetrieveAPIView):
    serializer_class = NutritionRecommendationSerializer
    lookup_field = 'meal'

    def get_queryset(self):
        meal = self.kwargs.get(self.lookup_field, '').lower()
        return NutritionRecommendation.objects.filter(meal__iexact=meal)

# Load the trained KNN model
knn_model = joblib.load('knn_workout_recommander_model.pkl')

# Load label encoders
label_encoders = {
    'Gender': joblib.load('Gender_encoder.pkl'),
    'Fitness_Goal': joblib.load('Fitness_Goal_encoder.pkl'),
    'Activity_Level': joblib.load('Activity_Level_encoder.pkl'),
    'Dietary_Preferences': joblib.load('Dietary_Preferences_encoder.pkl'),
    'Medical_Conditions': joblib.load('Medical_Conditions_encoder.pkl'),
    'Experience_Level': joblib.load('Experience_Level_encoder.pkl')
}

# Load the dataset for recommendations (same as used during training)
data = pd.read_csv('fitness_app/dataset/workout_prog_dataset.csv')

def get_recommendations(user_features, n_recommendations=5):
    user_features_df = pd.DataFrame(user_features, columns=[
        'Age', 'Height_cm', 'Weight_kg', 'Gender', 'Fitness_Goal',
        'Activity_Level', 'Dietary_Preferences', 'Medical_Conditions',
        'Experience_Level'])
    
    distances, indices = knn_model.kneighbors(user_features_df, n_neighbors=n_recommendations)
    recommendations = data.iloc[indices[0]]
    return recommendations[['Recommended_Exercise', 'Repetitions/Minutes', 'Sets;;']]

def clean_sets(sets_value):
    # Remove any characters that are not digits or single semicolon
    if pd.isna(sets_value):
        return ""
    
    # Remove unwanted characters, keep digits and semicolons
    sets_value = ''.join(c for c in sets_value if c.isdigit() or c == ';')
    
    # Remove extra semicolons
    sets_value = ';'.join(part for part in sets_value.split(';') if part)  # Remove empty parts
    
    return sets_value.strip()

class WorkoutRecommendationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form_data = {
            'age': int(request.data.get('age', 0)),
            'height_cm': int(request.data.get('height_cm', 0)),
            'weight_kg': int(request.data.get('weight_kg', 0)),
            'gender': request.data.get('gender'),
            'fitness_goal': request.data.get('fitness_goal'),
            'activity_level': request.data.get('activity_level'),
            'dietary_preferences': request.data.get('dietary_preferences'),
            'medical_conditions': request.data.get('medical_conditions'),
            'experience_level': request.data.get('experience_level')
        }

        # Ensure the data is correctly formatted into numerical values
        encoded_features = []
        for key in ['age', 'height_cm', 'weight_kg']:
            encoded_features.append(form_data[key])
        for key in ['gender', 'fitness_goal', 'activity_level', 'dietary_preferences', 'medical_conditions', 'experience_level']:
            if form_data[key] in label_encoders[key].classes_:
                encoded_value = label_encoders[key].transform([form_data[key]])[0]
            else:
                encoded_value = 0  # Default value if no data or unseen label
            encoded_features.append(encoded_value)

        encoded_features = np.array(encoded_features).reshape(1, -1)

        # Get recommendations
        try:
            recommendations = get_recommendations(encoded_features)
            recommendations_list = []
            for _, row in recommendations.iterrows():
                exercise = {
                    'name': row['Recommended_Exercise'],
                    'repetitions_minutes': row['Repetitions/Minutes'],
                    'sets': clean_sets(row['Sets;;'])  # Use the cleaned 'sets' value
                }
                recommendations_list.append(exercise)

            return Response({'recommendations': recommendations_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def bmi_calculator_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        form = BMICalculatorForm(data)
        if form.is_valid():
            weight_kg = form.cleaned_data['weight_kg']
            height_cm = form.cleaned_data['height_cm']
            bmi = calculate_bmi(weight_kg, height_cm)
            return JsonResponse({'bmi': bmi}, status=status.HTTP_200_OK)
        
        return JsonResponse({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

def bmr_calculator_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        form = BMRCalculatorForm(data)
        if form.is_valid():
            weight_kg = form.cleaned_data['weight_kg']
            height_cm = form.cleaned_data['height_cm']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            bmr = calculate_bmr(weight_kg, height_cm, age, gender)
            return JsonResponse({'bmr': bmr}, status=status.HTTP_200_OK)
        
        return JsonResponse({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

def calorie_needs_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        form = CalorieNeedsForm(data)
        if form.is_valid():
            weight_kg = form.cleaned_data['weight_kg']
            height_cm = form.cleaned_data['height_cm']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = form.cleaned_data['activity_level']
            bmr = calculate_bmr(weight_kg, height_cm, age, gender)
            calorie_needs = calculate_calorie_needs(bmr, activity_level)
            return JsonResponse({'calorie_needs': calorie_needs}, status=status.HTTP_200_OK)
        
        return JsonResponse({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

def body_fat_calculator_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        form = BodyFatCalculatorForm(data)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            waist_cm = form.cleaned_data['waist_cm']
            neck_cm = form.cleaned_data['neck_cm']
            height_cm = form.cleaned_data['height_cm']
            hip_cm = form.cleaned_data['hip_cm']
            body_fat_percentage = calculate_body_fat_percentage(gender, waist_cm, neck_cm, height_cm, hip_cm)
            return JsonResponse({'body_fat_percentage': body_fat_percentage}, status=status.HTTP_200_OK)
        
        return JsonResponse({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

def whr_calculator_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        form = WHRCalculatorForm(data)
        if form.is_valid():
            waist_cm = form.cleaned_data['waist_cm']
            hip_cm = form.cleaned_data['hip_cm']
            whr = calculate_whr(waist_cm, hip_cm)
            return JsonResponse({'whr': whr}, status=status.HTTP_200_OK)
        
        return JsonResponse({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

# Load the dataset and model
meal_data = pd.read_csv('fitness_app/dataset/meal_recommendations.csv')
knn_model_meals = joblib.load('knn_meal_recommander_model.pkl')

# Load encoders with the modified file names
label_encoders = {
    'age_range': joblib.load('Age_Range_Enc.pkl'),
    'gender': joblib.load('Gender_Enc.pkl'),
    'fitness_goal': joblib.load('Fitness_Goal_Enc.pkl'),
    'activity_level': joblib.load('Activity_Level_Enc.pkl'),
    'dietary_preferences': joblib.load('Dietary_Preferences_Enc.pkl'),
    'medical_conditions': joblib.load('Medical_Conditions_Enc.pkl'),
    'experience_level': joblib.load('Experience_Level_Enc.pkl')
}

def get_meal_recommendations(user_features, n_recommendations=5):
    distances, indices = knn_model_meals.kneighbors(user_features, n_neighbors=n_recommendations)
    recommendations = meal_data.iloc[indices[0]]
    return recommendations[['Meal Recommendation']].values

class MealRecommendationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form_data = {
            'age_range': request.data.get('age_range'),
            'gender': request.data.get('gender'),
            'fitness_goal': request.data.get('fitness_goal'),
            'activity_level': request.data.get('activity_level'),
            'dietary_preferences': request.data.get('dietary_preferences'),
            'medical_conditions': request.data.get('medical_conditions'),
            'experience_level': request.data.get('experience_level')
        }

        # Ensure the data is correctly formatted into numerical values
        encoded_features = []
        for key, value in form_data.items():
            if key in label_encoders:
                if value is not None:
                    try:
                        encoded_value = label_encoders[key].transform([value])[0]
                    except ValueError:  # Handle unseen labels
                        encoded_value = 0  # Default value if unseen
                else:
                    encoded_value = 0  # Default value if no data
                encoded_features.append(encoded_value)
            else:
                encoded_features.append(value)

        encoded_features = np.array(encoded_features, dtype=float).reshape(1, -1)

        # Get recommendations
        try:
            recommendations = get_meal_recommendations(encoded_features)
            recommendations_list = [{'meal': meal[0]} for meal in recommendations]
            return Response({'recommendations': recommendations_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ExercisesByMuscleGroupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, muscle_group):
        try:
            # Filter exercises by muscle group
            exercises = Exercise.objects.filter(muscle_groups__name=muscle_group).values()
            
            # Convert the QuerySet to a list of dictionaries
            exercises_list = list(exercises)

            return JsonResponse({'exercises': exercises_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ExerciseByNameView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, name):
        try:
            # Filter exercises by name
            exercises = Exercise.objects.filter(name__icontains=name)
            
            # Convert the QuerySet to a list of dictionaries with image URLs
            exercises_list = []
            for exercise in exercises:
                exercises_list.append({
                    'name': exercise.name,
                    'description': exercise.description,
                    'image': exercise.get_image_url(),  # Convert to URL
                    'video_url': exercise.video_url,
                    'muscle_groups': list(exercise.muscle_groups.values_list('name', flat=True)),  # Serialize muscle groups
                })

            return JsonResponse({'exercises': exercises_list}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TrainerPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class TrainerListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TrainerSerializer
    pagination_class = TrainerPagination

    def get_queryset(self):
        queryset = Trainer.objects.all().annotate(avg_rating=Avg('reviewontrainers__rating'))
        
        first_name = self.request.query_params.get('first_name', None)
        last_name = self.request.query_params.get('last_name', None)
        specialty = self.request.query_params.get('specialty', None)
        min_experience = self.request.query_params.get('min_experience', None)
        max_experience = self.request.query_params.get('max_experience', None)
        min_rating = self.request.query_params.get('min_rating', None)
        max_rating = self.request.query_params.get('max_rating', None)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if specialty:
            queryset = queryset.filter(specialty__icontains=specialty)
        if min_experience:
            queryset = queryset.filter(experience_years__gte=min_experience)
        if max_experience:
            queryset = queryset.filter(experience_years__lte=max_experience)
        if min_rating:
            try:
                min_rating = float(min_rating)
                queryset = queryset.filter(avg_rating__gte=min_rating)
            except ValueError:
                pass  # Handle invalid min_rating values gracefully
        if max_rating:
            try:
                max_rating = float(max_rating)
                queryset = queryset.filter(avg_rating__lte=max_rating)
            except ValueError:
                pass  # Handle invalid max_rating values gracefully

        return queryset

class TrainerDetailView(generics.RetrieveAPIView):
    """
    Retrieves detailed information about a specific trainer.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    """
    Lists all reviews and allows for creating new reviews.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ReviewOnTrainers.objects.all()
    serializer_class = ReviewOnTrainersSerializer

    def perform_create(self, serializer):
        # Save the review with the authenticated user as the author
        serializer.save(user=self.request.user)

class TrainerReviewListView(generics.ListAPIView):
    """
    Lists all reviews for a specific trainer.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = ReviewOnTrainersSerializer

    def get_queryset(self):
        trainer_id = self.kwargs['trainer_id']
        return ReviewOnTrainers.objects.filter(trainer_id=trainer_id)
    
class AddReviewOnWebsiteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReviewOnWebsiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditReviewOnWebsiteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, review_id):
        review = get_object_or_404(ReviewOnWebsite, id=review_id, user=request.user)
        serializer = ReviewOnWebsiteSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewsOnWebsiteListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = ReviewOnWebsite.objects.filter(user=request.user).order_by('-updated_at')
        serializer = ReviewOnWebsiteSerializer(reviews, many=True)
        return Response(serializer.data)
    
class AllReviewsOnWebsiteListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        reviews = ReviewOnWebsite.objects.all().order_by('-updated_at')
        serializer = ReviewOnWebsiteSerializer(reviews, many=True)
        return Response(serializer.data)
