from flask import Flask, render_template, redirect, url_for, flash, request, send_file, abort
from contact import RsvpForm
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "r5924hfrkfdswdwj"

@app.route("/", methods=["GET","POST"])
def home():
    form = RsvpForm()
    if form.validate_on_submit():
        print(form.data['name'], form.data['email'])
        headers = ["NAME", "EMAIL", "PHONE", "ATTEND", "MEMBER", "MESSAGE", "DATE_FILLED"]

        file_path = 'rsvp_form.csv'
        file_exists = os.path.isfile(file_path)

        with open (file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            
            if not file_exists:
                print("csv file is not found...writing headers")
                writer.writerow(headers)
            writer.writerow([form.data["name"],form.data["email"],form.data["phone"],
                             form.data["attend"],form.data["member"],form.data["message"], datetime.now().strftime("%Y-%m-%d")])
            flash(f"Thank you {form.name.data}.\nYou have been registered.")
            return redirect(url_for("home"))
    return render_template("index.html", form=form)

@app.route("/menexcel_form")
def download_csv():
    # Replace 'MySecret123' with your own strong secret
    file_path = 'rsvp_form.csv'
    if not os.path.isfile(file_path):
        flash("No submissions yet!")
        return redirect("/")

    secret_key = request.args.get("key")
    if secret_key != "BondMen_@1234":
        abort(403)  # Forbidden if key is wrong
    return send_file("rsvp_form.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)