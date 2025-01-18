import math

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return bmi

def calculate_bmr(weight_kg, height_cm, age, gender):
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    elif gender.lower() == 'female':
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    return bmr

def calculate_calorie_needs(bmr, activity_level):
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'super active': 1.9
    }
    
    if activity_level.lower() not in activity_multipliers:
        raise ValueError("Invalid activity level")
    
    return bmr * activity_multipliers[activity_level.lower()]

def calculate_body_fat_percentage(gender, waist_cm, neck_cm, height_cm, hip_cm=None):
    if gender.lower() == 'male':
        body_fat = 86.010 * math.log10(waist_cm - neck_cm) - 70.041 * math.log10(height_cm) + 36.76
    elif gender.lower() == 'female':
        if hip_cm is None:
            raise ValueError("Hip measurement is required for females")
        body_fat = 163.205 * math.log10(waist_cm + hip_cm - neck_cm) - 97.684 * math.log10(height_cm) - 78.387
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    return body_fat

def calculate_whr(waist_cm, hip_cm):
    if hip_cm == 0:
        raise ValueError("Hip measurement must be non-zero")
    whr = waist_cm / hip_cm
    return whr
