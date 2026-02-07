from flask import Flask, render_template, redirect, url_for, flash, request, send_file, abort
from contact import RsvpForm
import csv
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "r5924hfrkfdswdwj"


file_path = 'rsvp_form.csv'
file_exists = os.path.isfile(file_path)

@app.route("/", methods=["GET","POST"])
def home():
    form = RsvpForm()
    if form.validate_on_submit():
        print(form.data['name'], form.data['email'])
        headers = ["NAME", "EMAIL", "PHONE", "ATTEND", "MEMBER", "MESSAGE"]
        with open ('rsvp_form.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            if not file_exists:
                print("csv file is not found")
                writer.writerow(headers)
            writer.writerow([form.data["name"],form.data["email"],form.data["phone"],
                             form.data["attend"],form.data["member"],form.data["message"]])
            flash("Registration has been submitted!")
            return redirect(url_for("home"))
    return render_template("index.html", form=form)

@app.route("/menexcel_form")
def download_csv():
    # Replace 'MySecret123' with your own strong secret
    secret_key = request.args.get("key")
    if secret_key != "BondMen_@1234":
        abort(403)  # Forbidden if key is wrong
    return send_file("rsvp_form.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)