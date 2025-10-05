

# 🧬 Pancreatic Cancer Detection

A **Flask-based Machine Learning web application** for detecting the likelihood of pancreatic cancer using patient data and trained predictive models.  
This project integrates **data preprocessing, model prediction, and result visualization** in an easy-to-use web interface.

---

## 🚀 Features

- Machine Learning model for pancreatic cancer prediction  
- Flask web application for interactive prediction  
- Environment-based configuration using `.env`  
- Visualization of prediction metrics using `matplotlib`  
- Modular structure for easy customization and deployment  

---

## 🗂️ Project Structure

```

PancreaticProject/
│
├── env/                   # Virtual environment (ignored in .gitignore)
├── project/
│   ├── appp.py             # Main Flask application
│   ├── templates/          # HTML templates for the frontend
│   ├── static/             # CSS, JS, or image assets
│   ├── model.pkl           # Trained ML model (example)
│   └── ... (other scripts or utilities)
│
├── requirements.txt        # All Python dependencies (optional)
└── README.md               # Project documentation

````

---

## 🧩 Prerequisites

Make sure you have **Python 3.8+** installed on your system.  
You can check by running:
```bash
python --version
````

---

## ⚙️ Installation & Setup (Windows)

Open **PowerShell** and run these commands step-by-step 👇

```bash
# 1️⃣ Clone the repository
git clone https://github.com/KarunyaBhat12/PancreaticCancerDetection.git
cd PancreaticCancerDetection

# 2️⃣ Create a virtual environment
py -m venv env

# 3️⃣ Activate the environment
.\env\Scripts\Activate

# 4️⃣ Navigate to project folder
cd project

# 5️⃣ Install dependencies
pip install pandas
pip install flask
pip install python-dotenv
pip install scikit-learn
pip install matplotlib
```

> 💡 Alternatively, you can install all dependencies at once if you have `requirements.txt`:
>
> ```bash
> pip install -r requirements.txt
> ```

---

## ▶️ Running the Application

Once everything is installed, start the Flask app:

```bash
python appp.py
```

You should see something like:

```
 * Serving Flask app 'appp'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Then, open your browser and visit:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧠 Technologies Used

* **Python**
* **Flask**
* **Pandas**
* **Scikit-learn**
* **Matplotlib**
* **dotenv**

---

## 📈 Future Enhancements

* Add user-friendly form validation
* Integrate model retraining pipeline
* Deploy using AWS / Render / Heroku
* Add result visualization dashboard

---

