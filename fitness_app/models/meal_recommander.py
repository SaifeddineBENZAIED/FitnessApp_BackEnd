import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import joblib

# Load your dataset
df = pd.read_csv('fitness_app/dataset/meal_recommendations.csv')

# Define expected columns and their encoders
expected_columns = {
    'Age Range': LabelEncoder(),
    'Gender': LabelEncoder(),
    'Fitness Goal': LabelEncoder(),
    'Activity Level': LabelEncoder(),
    'Dietary Preferences': LabelEncoder(),
    'Medical Conditions': LabelEncoder(),
    'Experience Level': LabelEncoder()
}

# Encode categorical features
label_encoders = {}
for column, encoder in expected_columns.items():
    if column in df.columns:
        df[column] = encoder.fit_transform(df[column])
        label_encoders[column] = encoder
        joblib.dump(encoder, f'{column.replace(" ", "_")}_Enc.pkl')  # Save with modified name
    else:
        print(f"Column '{column}' not found in the dataset.")

# Separate features and target
X = df.drop("Meal Recommendation", axis=1)
y = df["Meal Recommendation"]

# Use NearestNeighbors to find similar meals
model = NearestNeighbors(n_neighbors=5, algorithm='auto')
model.fit(X)

# Save the KNN model
joblib.dump(model, 'knn_meal_recommander_model.pkl')
