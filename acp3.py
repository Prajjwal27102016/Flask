import os
from flask import Flask, render_template, request

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, "27-6-26", "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)


@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    category = None
    weight = ""
    height = ""

    if request.method == "POST":
        try:
            weight = request.form.get("weight", "").strip()
            height = request.form.get("height", "").strip()

            if not weight or not height:
                raise ValueError("Please enter both values.")

            weight_value = float(weight)
            height_value = float(height)

            if height_value <= 0:
                raise ValueError("Height must be greater than zero.")

            bmi = round(weight_value / (height_value ** 2), 1)

            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
            elif 25 <= bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
        except (TypeError, ValueError):
            category = "Please enter valid numeric values."

    return render_template("acp3.html", bmi=bmi, category=category, weight=weight, height=height)


if __name__ == "__main__":
    app.run(debug=True)
