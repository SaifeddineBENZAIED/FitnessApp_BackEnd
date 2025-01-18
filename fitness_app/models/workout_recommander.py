from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import joblib
import pandas as pd

# Load your dataset
data = pd.read_csv('fitness_app/dataset/workout_prog_dataset.csv')

# Encode categorical variables
label_encoders = {
    'Gender': LabelEncoder(),
    'Fitness_Goal': LabelEncoder(),
    'Activity_Level': LabelEncoder(),
    'Dietary_Preferences': LabelEncoder(),
    'Medical_Conditions': LabelEncoder(),
    'Experience_Level': LabelEncoder()
}

# Fit the encoders and transform the data
for column, encoder in label_encoders.items():
    data[column] = encoder.fit_transform(data[column].astype(str))  # Ensure all data is string type
    joblib.dump(encoder, f'{column}_encoder.pkl')  # Save the encoder

# Feature matrix
X = data[['Age', 'Height_cm', 'Weight_kg', 'Gender', 'Fitness_Goal', 'Activity_Level', 'Dietary_Preferences', 'Medical_Conditions', 'Experience_Level']]

# Create and fit the nearest neighbors model
knn = NearestNeighbors(n_neighbors=5, algorithm='auto')
knn.fit(X)

# Save the KNN model
joblib.dump(knn, 'knn_workout_recommander_model.pkl')
