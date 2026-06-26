from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    if request.method == "POST":
        date1_str = request.form.get("date1", "").strip()
        date2_str = request.form.get("date2", "").strip()
        
        if date1_str and date2_str:
            try:
                d1 = datetime.strptime(date1_str, "%d-%m-%Y")
                d2 = datetime.strptime(date2_str, "%d-%m-%Y")
                result = abs((d2 - d1).days)
            except ValueError:
                error = "Invalid date format! Please use DD-MM-YYYY (e.g., 22-6-2026)"
        else:
            error = "Please enter both dates!"
            
    return render_template("acp2.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)