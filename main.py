from config import *
from helpers import translate


@app.context_processor
def userid():
    try:
        user = Listing(table="users", condition={
                       "id": session['id']}, single=True)
        return {'user': user}

    except:
        return {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/disease-details/<int:id>/', methods=['GET'])
def diseaseDetails(id):
    disease = Listing(table="diseases", condition={"id": id}, single=True)
    doctors = Listing(table="doctors", condition={
                      "disease_id": id}, order={"id": "DESC"})
    return render_template('disease-details.html', disease=disease, doctors=doctors)


@app.route('/diseases/', methods=['GET'])
def diseases():
    search = request.args.get("disease")
    if search:
        search = translate(search)
        diseases = Listing(table="diseases", condition={
            "name": search}, order={"id": "DESC"})
    else:
        diseases = Listing(table="diseases", order={"id": "DESC"})
    return render_template('diseases.html', diseases=diseases)


@app.route('/disease-insert/', methods=["POST", "GET"])
def InsertDisease():
    if request.method == "GET":
        return render_template('disease-insert.html')
    elif request.method == "POST":
        name = request.form["name"]

        try:
            data = fetchDisease(name)
            disease_id = Create(table="diseases", columns={
                "name": data["name"],
                "description": data["description"],
                "summary": data["summary"],
                "symptoms": data["symptoms"],
                "treatment": data["treatment"],
                "risk": data["risk"],
                "prevention": data["prevention"],
            })

            for doctor in data["doctors"]:
                Create(table="doctors", columns={
                    "name": doctor["name"],
                    "image": doctor["image"],
                    "link": doctor["link"],
                    "disease_id": disease_id
                })
            flash("Disease added successfully!", "success")
        except:
            flash("Invalid response found!", "danger")
    return render_template('disease-insert.html')


@app.route('/disease-delete/<int:id>/', methods=["GET"])
def DeleteDisease(id):
    Delete(table="diseases", condition={"id": id})
    Delete(table="doctors", condition={"disease_id": id})
    flash("1 record deleted successfully!", "success")
    return redirect(url_for('diseases'))


@app.route('/about-us/', methods=['GET'])
def AboutUs():
    return render_template('about-us.html')


@app.route('/contact-us/', methods=['GET', "POST"])
def ContactUs():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST':
        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        msg = Message('Uhrs customer query email',
                      sender='support@uhrs.com', recipients=[email])
        body = f'Hi! there, \n its <b> {fullname} </b> \n {message} \n <b>Phone :</b> {phone} \n Thanks \n Regards \n {fullname}.'
        msg.body = body
        mail.send(msg)
        flash("Email sent successfully!", "success")
    return render_template('contact.html')


@app.route('/terms-and-conditions/', methods=['GET'])
def TermsAndConditions():
    return render_template('terms-and-conditions.html')


@app.route('/privacy-policy/', methods=['GET'])
def PrivacyPolicy():
    return render_template('privacy-policy.html')


@app.route('/help-center/', methods=['GET'])
def HelpCenter():
    return render_template('help-center.html')


@app.route('/admin/', methods=['GET', 'POST'])
def login():
    if "id" in session:
        return redirect(url_for('InsertDisease'))
    else:
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            email = request.form["email"]
            password = request.form["password"]
            user_data = Listing(table="users", condition={
                "email": email, "password": password}, single=True)

            if user_data:
                session['id'] = user_data["id"]
                flash("Login successfully!", "success")
                return redirect(url_for('InsertDisease'))
            else:
                flash(f"Incorrect credentials!", "danger")
                return render_template('login.html')


@ app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.pop('id', None)
    flash("Logout successfully!", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    # This is the secrect key of our project
    app.secret_key = "@@dasa@@/$"

    app.run(debug=True, port=5000)
