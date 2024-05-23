import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Load the CSV file
file_path = './games.csv'
games_df = pd.read_csv(file_path)

# Preprocess the data
games_df = games_df.dropna(subset=['winner', 'white_rating', 'black_rating', 'moves'])

# Encode the target variable
label_encoder = LabelEncoder()
games_df['winner_encoded'] = label_encoder.fit_transform(games_df['winner'])

# Basic feature extraction
X = games_df[['white_rating', 'black_rating', 'turns']]
y = games_df['winner_encoded']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(report)
