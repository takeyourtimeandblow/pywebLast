from flask import Flask, redirect, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from db_session import create_session, global_init
from forms.department import DepartmentForm
from forms.jobs import JobForm
from forms.login import LoginForm
from forms.user import RegisterForm
from models.department import Department
from models.jobs import Jobs
from models.user import User

from jobs_api import jobs_api
from user_api import user_api
import requests
from flask import abort



def can_edit(job):
    return current_user.id == 1 or job.team_leader == current_user.id


app = Flask(__name__)
app.config["SECRET_KEY"] = "mars_secret_key"
app.config['JSON_AS_ASCII'] = False
app.config['TESTING'] = True

global_init("mars_explorer.db")

app.register_blueprint(jobs_api)
app.register_blueprint(user_api)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.get(User, int(user_id))


@app.route("/")
def index():
    session = create_session()
    jobs = session.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = create_session()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            hashed_password=generate_password_hash(form.password.data),
        )
        session.add(user)
        session.commit()
        login_user(user)
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/add_job", methods=["GET", "POST"])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        session = create_session()
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
        )
        session.add(job)
        session.commit()
        return redirect("/")
    return render_template("add_job.html", h2_str="Добавление работы", form=form)


@app.route("/edit_job/<int:id>", methods=["GET", "POST"])
@login_required
def edit_job(id):
    session = create_session()
    job = session.get(Jobs, id)

    if not can_edit(job):
        return redirect("/")

    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.populate_obj(job)
        session.commit()
        return redirect("/")
    return render_template("add_job.html", h2_str="Изменение Работы", form=form)


@app.route("/delete_job/<int:id>")
@login_required
def delete_job(id):
    session = create_session()
    job = session.get(Jobs, id)

    if can_edit(job):
        session.delete(job)
        session.commit()

    return redirect("/")


@app.route("/add_department", methods=["GET", "POST"])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = create_session()
        dep = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data,
        )
        session.add(dep)
        session.commit()
        return redirect("/")
    return render_template(
        "add_department.html", h2_str="Добавление департамента", form=form
    )


@app.route("/edit_department/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):
    session = create_session()
    job = session.get(Department, id)

    if not can_edit(job):
        return redirect("/")

    form = DepartmentForm(obj=job)
    if form.validate_on_submit():
        form.populate_obj(job)
        session.commit()
        return redirect("/")
    return render_template(
        "add_department.html", h2_str="Изменение департамента", form=form
    )


@app.route("/departments")
def departments():
    session = create_session()
    return render_template(
        "departments.html", departments=session.query(Department).all()
    )

@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    # Используем API, а не БД!
    response = requests.get(f'http://localhost:5000/api/users/{user_id}')

    if response.status_code != 200:
        abort(404)

    user = response.json()['user']

    if not user.get('city_from'):
        abort(404)

    return render_template(
        'users_show.html',
        user=user
    )



if __name__ == "__main__":
    app.run(debug=True)
