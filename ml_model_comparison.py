"""
Machine Learning Model Comparison Module for Travel Genie AI.

Generates a synthetic travel dataset, trains multiple ML models,
evaluates their performance, and identifies the best model.
"""

import numpy as np
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def generate_synthetic_dataset(n_samples=2000):
    """
    Generate a synthetic travel preference dataset.
    Features: age, budget, duration, group_size, travel_style, preferred_climate
    Target: destination_category (beach, mountain, city, countryside, island)
    """
    np.random.seed(42)

    age = np.random.randint(18, 70, n_samples)
    budget = np.random.uniform(500, 15000, n_samples)
    duration = np.random.randint(1, 30, n_samples)
    group_size = np.random.randint(1, 8, n_samples)
    travel_style = np.random.randint(0, 4, n_samples)  # 0=adventure, 1=relaxation, 2=cultural, 3=family
    preferred_climate = np.random.randint(0, 4, n_samples)  # 0=tropical, 1=temperate, 2=cold, 3=desert

    # Create destination categories based on realistic rules
    destination_category = []
    for i in range(n_samples):
        score_beach = (preferred_climate[i] == 0) * 3 + (travel_style[i] == 1) * 2 + (budget[i] > 3000) * 1
        score_mountain = (preferred_climate[i] == 2) * 3 + (travel_style[i] == 0) * 2 + (duration[i] > 5) * 1
        score_city = (travel_style[i] == 2) * 3 + (age[i] > 25) * 1 + (budget[i] > 5000) * 1
        score_countryside = (travel_style[i] == 3) * 3 + (group_size[i] > 3) * 2 + (preferred_climate[i] == 1) * 1
        score_island = (preferred_climate[i] == 0) * 2 + (budget[i] > 7000) * 2 + (travel_style[i] == 1) * 1

        scores = {
            'beach': score_beach + np.random.normal(0, 0.5),
            'mountain': score_mountain + np.random.normal(0, 0.5),
            'city': score_city + np.random.normal(0, 0.5),
            'countryside': score_countryside + np.random.normal(0, 0.5),
            'island': score_island + np.random.normal(0, 0.5),
        }
        destination_category.append(max(scores, key=scores.get))

    df = pd.DataFrame({
        'age': age,
        'budget': budget,
        'duration': duration,
        'group_size': group_size,
        'travel_style': travel_style,
        'preferred_climate': preferred_climate,
        'destination_category': destination_category
    })

    return df


def train_and_compare_models(df=None):
    """
    Train multiple ML models on the travel dataset and compare performance.
    Returns a list of model results sorted by F1 score.
    """
    if df is None:
        df = generate_synthetic_dataset()

    # Prepare features and target
    X = df[['age', 'budget', 'duration', 'group_size', 'travel_style', 'preferred_climate']]
    le = LabelEncoder()
    y = le.fit_transform(df['destination_category'])

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define models to compare
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'SVM (RBF Kernel)': SVC(kernel='rbf', random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
    }

    results = []

    for name, model in models.items():
        # Train
        start_time = time.time()
        model.fit(X_train_scaled, y_train)
        training_time = (time.time() - start_time) * 1000  # ms

        # Predict
        y_pred = model.predict(X_test_scaled)

        # Evaluate
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        results.append({
            'model_name': name,
            'accuracy': round(acc, 4),
            'precision_score': round(prec, 4),
            'recall': round(rec, 4),
            'f1_score': round(f1, 4),
            'training_time_ms': round(training_time, 2),
        })

    # Sort by F1 score descending
    results.sort(key=lambda x: x['f1_score'], reverse=True)
    return results, scaler, le, models[results[0]['model_name']]


def predict_destination(user_features, scaler, label_encoder, best_model):
    """
    Predict the best destination category for a user based on their preferences.
    user_features: dict with keys age, budget, duration, group_size, travel_style, preferred_climate
    """
    style_map = {'adventure': 0, 'relaxation': 1, 'cultural': 2, 'family': 3}
    climate_map = {'tropical': 0, 'temperate': 1, 'cold': 2, 'desert': 3}

    features = np.array([[
        user_features.get('age', 30),
        user_features.get('budget', 5000),
        user_features.get('duration', 7),
        user_features.get('group_size', 2),
        style_map.get(user_features.get('travel_style', 'adventure'), 0),
        climate_map.get(user_features.get('preferred_climate', 'tropical'), 0),
    ]])

    features_scaled = scaler.transform(features)
    prediction = best_model.predict(features_scaled)
    category = label_encoder.inverse_transform(prediction)[0]

    return category


if __name__ == "__main__":
    print("Generating synthetic travel dataset...")
    dataset = generate_synthetic_dataset()
    print(f"Dataset shape: {dataset.shape}")
    print(f"Class distribution:\n{dataset['destination_category'].value_counts()}")
    print("\nTraining and comparing models...")
    results, _, _, _ = train_and_compare_models(dataset)
    print("\n--- Model Comparison Results ---")
    for r in results:
        print(f"{r['model_name']:25s} | Accuracy: {r['accuracy']:.4f} | F1: {r['f1_score']:.4f} | Time: {r['training_time_ms']:.1f}ms")
    print(f"\nBest Model: {results[0]['model_name']}")
