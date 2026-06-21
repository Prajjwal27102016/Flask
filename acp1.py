from flask import Flask, render_template, request


app = Flask(__name__, template_folder="20-6-26/templates")


@app.route("/", methods=["GET", "POST"])
def index():
    # Initial state when the user first loads the page
    name = None
    goal = None
    consumed = None
    progress_percentage = 0
    status_message = ""

    if request.method == "POST":
        # Extract data from the form
        name = request.form.get("name")

        # Convert numbers securely with defaults to avoid errors
        try:
            goal = float(request.form.get("goal", 0))
            consumed = float(request.form.get("consumed", 0))
        except ValueError:
            goal, consumed = 0, 0

        # Calculate progress metric
        if goal > 0:
            progress_percentage = min(
                int((consumed / goal) * 100), 100
            )  # Cap at 100%

            if consumed >= goal:
                status_message = f"Amazing job, {name}! You reached your daily water goal! 🎉"
            else:
                remaining = goal - consumed
                status_message = f"Keep going, {name}! You need {remaining:.1f} more glasses to hit your goal."

    # Send variables over to the Jinja2 template
    return render_template(
        "acp1.html",
        name=name,
        goal=goal,
        consumed=consumed,
        progress=progress_percentage,
        message=status_message,
    )


if __name__ == "__main__":
    app.run(debug=True)
