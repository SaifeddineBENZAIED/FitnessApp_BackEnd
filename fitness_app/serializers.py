from rest_framework import serializers
from .models import Account, MuscleGroup, Exercise, NutritionRecommendation, Trainer, ReviewOnTrainers, ReviewOnWebsite
from django.conf import settings
from django.contrib.auth.hashers import make_password

"""class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'password', 'age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'experience_level', 'phone_number', 'country', 'profile_image', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'hide_email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            if field == 'password' and value is not None:
                instance.set_password(value)
            else:
                setattr(instance, field, value)
        instance.save()
        return instance

    def validate(self, data):
        user = self.instance
        if not user or not user.is_superuser:
            # For regular users, ensure the required fields are provided
            required_fields = ['age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'experience_level']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f'{field} is required'})
        else:
            # For superuser, set non-essential fields to None
            data['age'] = None
            data['height'] = None
            data['weight'] = None
            data['gender'] = None
            data['fitness_goal'] = None
            data['activity_level'] = None
            data['experience_level'] = None
        return data"""

"""class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'password', 'age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'experience_level', 'phone_number', 'country', 'profile_image', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'hide_email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        user = Account.objects.create_user(**validated_data)
        if profile_image:
            user.profile_image = profile_image
        user.save()
        return user"""

class AccountSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.ReadOnlyField(source='get_profile_image_url')
    
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'password', 'age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'dietary_preferences', 'medical_conditions', 'experience_level', 'phone_number', 'country', 'profile_image', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'hide_email', 'profile_image_url']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'default': True},
            'hide_email': {'default': True}
        }

    def create(self, validated_data):
        validated_data['is_active'] = validated_data.get('is_active', True)
        validated_data['hide_email'] = validated_data.get('hide_email', True)

        password = validated_data.pop('password', None)
        profile_image = validated_data.pop('profile_image', None)

        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        
        # If a profile image is provided, set it
        if profile_image:
            instance.profile_image = profile_image

        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        profile_image = validated_data.pop('profile_image', None)
        
        # Handle updating the password
        if password is not None:
            instance.set_password(password)
        
        # Handle updating other fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        # Handle updating the profile image if provided
        if profile_image:
            instance.profile_image = profile_image

        instance.save()
        return instance

    def validate(self, data):
        user = self.instance
        if not user or not user.is_superuser:
            # For regular users, ensure the required fields are provided
            required_fields = ['age', 'height', 'weight', 'gender', 'fitness_goal', 'activity_level', 'experience_level']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f'{field} is required'})
        else:
            # For superuser, set non-essential fields to None
            data['age'] = None
            data['height'] = None
            data['weight'] = None
            data['gender'] = None
            data['fitness_goal'] = None
            data['activity_level'] = None
            data['experience_level'] = None
        return data

    """def get_profile_image_url(self, obj):
        if obj.profile_image:
            return f"https://res.cloudinary.com/{settings.CLOUDINARY['cloud_name']}/{obj.profile_image}"
            
        return None"""

class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = '__all__'

class ExerciseSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField(source='get_image_url')
    muscle_groups = MuscleGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = '__all__'

"""class WorkoutProgramSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutProgram
        fields = '__all__'
"""
class NutritionRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionRecommendation
        fields = '__all__'

class TrainerSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Trainer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'specialty', 'experience_years', 'bio', 'profile_image', 'average_rating']

class ReviewOnTrainersSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Adjust if needed

    class Meta:
        model = ReviewOnTrainers
        fields = '__all__'

class ReviewOnWebsiteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Adjust if needed

    class Meta:
        model = ReviewOnWebsite
        fields = '__all__'
