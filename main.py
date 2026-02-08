from flask import Flask, render_template, redirect, url_for, flash, request, send_file, abort
from contact import RsvpForm
from dotenv import load_dotenv
from supabase import create_client, Client
import os
import io
import csv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


@app.route("/", methods=["GET", "POST"])
def home():
    form = RsvpForm()

    if form.validate_on_submit():
        supabase.table("rsvp_submissions").insert({
            "name": form.data["name"],
            "email": form.data["email"],
            "phone": form.data["phone"],
            "attend": form.data["attend"],
            "member": form.data["member"],
            "message": form.data["message"]
        }).execute()

        flash(f"Thank you {form.name.data}. You have been registered.")
        return redirect(url_for("home"))

    return render_template("index.html", form=form)


@app.route("/menexcel_form")
def download_csv():
    if request.args.get("key") != os.getenv("DOWNLOAD_KEY"):
        abort(403)

    response = supabase.table("rsvp_submissions") \
        .select("name,email,phone,attend,member,message,date_filled") \
        .order("created_at") \
        .execute()

    rows = response.data

    if not rows:
        flash("No submissions yet!")
        return redirect("/")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["NAME", "EMAIL", "PHONE", "ATTEND", "MEMBER", "MESSAGE", "DATE_FILLED"])

    for row in rows:
        writer.writerow([
            row["name"],
            row["email"],
            row["phone"],
            row["attend"],
            row["member"],
            row["message"],
            row["date_filled"]
        ])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="rsvp_form.csv"
    )


if __name__ == "__main__":
    app.run(debug=True)
