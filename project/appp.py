import os
import io
import base64
import pandas as pd
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'd3b07384d113edec49eaa6238ad5ff00')

# Load and preprocess the dataset
df = pd.read_csv(r"C:\Users\Lenovo\Downloads\PancreaticProject\project\Debernardi et al 2020 data.csv")
df['sex'] = LabelEncoder().fit_transform(df['sex'])

# Fill missing values
df['plasma_CA19_9'] = df['plasma_CA19_9'].fillna(df['plasma_CA19_9'].mean())
df['REG1A'] = df['REG1A'].fillna(df['REG1A'].mean())

# Define column order (excluding stage)
column_order = [
    "age", "sex", "diagnosis",
    "plasma_CA19_9", "creatinine", "LYVE1", "REG1B", "TFF1", "REG1A"
]
df = df[column_order]

# Define features (X) and target (y)
X = df.drop("diagnosis", axis=1)
y = df["diagnosis"]

# Train Random Forest Classifier
clf = RandomForestClassifier(n_estimators=40,max_depth=6, random_state=42)
clf.fit(X, y)

# Chart generation function
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' before importing pyplot
import matplotlib.pyplot as plt
import io
import base64

def create_chart(user_data):
    # Define normal ranges
    normal_ranges = {
        "age": (20, 60),
        "sex": (0, 1),
        "plasma_CA19_9": (0, 37),
        "creatinine": (0.6, 1.2),
        "LYVE1": (10, 50),
        "REG1B": (5, 30),
        "TFF1": (5, 25),
        "REG1A": (10, 40),
    }

    # Exclude 'sex' from the user data and normal ranges for the chart
    user_data = {key: value for key, value in user_data.items() if key != 'sex'}
    normal_ranges = {key: value for key, value in normal_ranges.items() if key != 'sex'}

    # Prepare data for chart
    parameters = list(user_data.keys())
    user_values = list(user_data.values())
    normal_values = [(low + high) / 2 for low, high in normal_ranges.values()]

    # Plot the chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    indices = range(len(parameters))

    # User data bars
    ax.bar(indices, user_values, bar_width, label="User Data", color="blue")
    # Normal range (average) bars
    ax.bar([i + bar_width for i in indices], normal_values, bar_width, label="Normal Range (Avg)", color="green")

    # Add labels and title
    ax.set_xlabel("Parameters")
    ax.set_ylabel("Values")
    ax.set_title("User Data vs Normal Range")
    ax.set_xticks([i + bar_width / 2 for i in indices])
    ax.set_xticklabels(parameters, rotation=45)
    ax.legend()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image in base64
    chart_img = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)
    return chart_img

@app.route('/')
def home():
    return render_template('index.html', show_default_menu=True)

@app.route('/about')
def about():
    return render_template('about.html', show_default_menu=True)
@app.route('/faq')
def faq():
    return render_template("faq.html", show_default_menu=True) 

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    explanation = ""  # Ensure explanation is always initialized
    higher_values = []  # List to store which features are above the threshold

    if request.method == "POST":
        # Collect form data
        input_data = {
            "age": float(request.form["age"]),
            "sex": int(request.form["sex"]),
            "plasma_CA19_9": float(request.form["plasma_CA19_9"]),
            "creatinine": float(request.form["creatinine"]),
            "LYVE1": float(request.form["LYVE1"]),
            "REG1B": float(request.form["REG1B"]),
            "TFF1": float(request.form["TFF1"]),
            "REG1A": float(request.form["REG1A"]),
        }

        # Store the user data in session for analysis
        session["user_data"] = input_data

        # Convert input data to a DataFrame
        input_df = pd.DataFrame([input_data])
        input_df = input_df[X.columns]  # Align column order

        # Make prediction
        prediction = clf.predict(input_df)[0]

        # Define thresholds for higher values
        thresholds = {
            "age": 60,
            "plasma_CA19_9": 37,
            "creatinine": 1.2,
            "LYVE1": 50,
            "REG1B": 30,
            "TFF1": 25,
            "REG1A": 40,
        }

        # Identify higher-than-threshold values
        for feature, value in input_data.items():
            if feature in thresholds and value > thresholds[feature]:
                higher_values.append(f"{feature} ({value:.2f})")

        # Handle explanations based on prediction and threshold values
        if prediction == 1:
            explanation = (
                "Your test results indicate all parameters are within the normal range. "
                "There is no sign of pancreatic cancer. Maintain a healthy lifestyle!"
            )
        elif prediction == 2:
            if higher_values:
                explanation = (
                    f"Some of your test values, such as {', '.join(higher_values)}, "
                    "are slightly above the normal range. This could indicate non-cancerous pancreatitis. "
                    "Consult a doctor for further assessment if you have symptoms."
                )
            else:
                explanation = (
                    "Some of your test parameters indicate potential non-cancerous pancreatitis. "
                    "Please consult a doctor for accurate diagnosis."
                )
        elif prediction == 3:
            if higher_values:
                explanation = (
                    f"Some values like {', '.join(higher_values)} are higher than the safe range. "
                    "This may indicate a potential risk of pancreatic cancer. "
                    "Please consult a doctor for accurate diagnosis and early intervention."
                )
            else:
                explanation = (
                    "Test results suggest a potential risk of pancreatic cancer. "
                    "Please consult a doctor for further assessment."
                )
        else:
            explanation = (
                "An error occurred while analyzing the data. "
                "Please retry or consult with a medical professional."
            )

        # Map prediction to diagnosis
        diagnosis_map = {
            1: "No Cancer",
            2: "Non-Cancerous Pancreatitis",
            3: "Pancreatic Cancer"
        }
        prediction_result = diagnosis_map.get(prediction, "Unknown")

        # Calculate and display metrics
        # Let's use the same model to calculate metrics using the original dataset (X, y)
        y_pred = clf.predict(X)  # Predict on all data
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred, average='weighted', zero_division=1)
        recall = recall_score(y, y_pred, average='weighted', zero_division=1)
        f1 = f1_score(y, y_pred, average='weighted', zero_division=1)

        return render_template(
            "result.html",
            show_default_menu=False,
            prediction=prediction_result,
            explanation=explanation,
            higher_values=higher_values,
            accuracy=f"Accuracy: {accuracy*100:.2f}%",
            precision=f"Precision: {precision:.2f}",
            recall=f"Recall: {recall:.2f}",
            f1_score=f"F1-Score: {f1:.2f}",
        )

    return render_template("prediction.html", show_default_menu=False)


@app.route("/prediction/recommendations")
def recommendations():
    return render_template("recommendations.html",show_default_menu=False)

@app.route('/prediction/analyse')
def analyse():
    # Retrieve user data from session
    user_data = session.get("user_data", None)
    if not user_data:
        return redirect(url_for("prediction"))

    # Generate chart
    chart_img = create_chart(user_data)

    return render_template("analyse.html", show_default_menu=False, chart_img=chart_img)

# Now run the Flask app
if __name__ == '__main__':
    app.run(debug=True)





