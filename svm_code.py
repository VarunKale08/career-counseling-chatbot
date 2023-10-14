# Step 2: Prepare Data
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Read the CSV Data
df = pd.read_csv('/dataset.csv')

# Drop any duplicate rows, if any
df = df.drop_duplicates()

# Remove leading and trailing spaces from column names
df.columns = df.columns.str.strip()

# Check for missing values
print(df.isna().sum())

# Output:
# Name                 0
# Mathematics          0
# Science              0
# Social_Studies       0
# English              0
# Optional_subject     0
# Interested_field     0
# dtype: int64

# There are no missing values, so no further handling is needed.

# Scale Numerical Values (Mathematics, Science, Social_Studies, English)
scaler = MinMaxScaler()
numerical_columns = ['Mathematics', 'Science', 'Social_Studies', 'English']
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# Inspect the Preprocessed Data
print(df.head())

# Step 3: Train and Save the Model
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import joblib

# Split Data into Training and Testing Sets
X = df[['Mathematics', 'Science', 'Social_Studies', 'English']]  # Features
y = df['Interested_field']  # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and Train the SVM Model
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# Evaluate Model Performance
accuracy = svm_model.score(X_test, y_test)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Save the Trained Model
joblib.dump(svm_model, 'career_counseling_model.joblib')
