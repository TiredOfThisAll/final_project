from flask import Flask, render_template, g, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, \
    logout_user
import json
from oauthlib.oauth2 import WebApplicationClient
import os
import requests
from werkzeug.local import LocalProxy

from sql.repository import Repository
from sql.sqlite_connection import create_sqlite_connection
from models.employee import Employee
from models.department import Department
from models.user import User

PROJECT_PATH = os.path.abspath(os.path.join(__file__, ".."))

config_file_path = os.path.join(PROJECT_PATH, "config", "configuration.json")

with open(config_file_path) as configuration_file:
    configuration_dict = json.loads(configuration_file.read())

google_client_id_path = os.path.join(
    PROJECT_PATH,
    configuration_dict["google_client_id"]
)

if not os.path.exists(google_client_id_path):
    print(f"You need the token file at {google_client_id_path}")
    exit(1)

google_client_secret_path = os.path.join(
    PROJECT_PATH,
    configuration_dict["google_client_secret"]
)

if not os.path.exists(google_client_secret_path):
    print(f"You need the token file at {google_client_secret_path}")
    exit(1)

with open(google_client_id_path) as google_client_id_file:
    GOOGLE_CLIENT_ID = google_client_id_file.readline()
    if GOOGLE_CLIENT_ID[-1] == "\n":
        GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID[:-1]

with open(google_client_secret_path) as google_client_secret_file:
    GOOGLE_CLIENT_SECRET = google_client_secret_file.readline()
    if GOOGLE_CLIENT_SECRET[-1] == "\n":
        GOOGLE_CLIENT_SECRET = GOOGLE_CLIENT_SECRET[:-1]

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

DATABASE_NAME = configuration_dict["database"]

DATABASE_PATH = os.path.join(PROJECT_PATH, DATABASE_NAME)

COLUMNS = {"id", "department_id", "age", "salary"}

# create DB schema if it doesn't exist yet
with create_sqlite_connection(DATABASE_PATH) as connection:
    repository = Repository(connection)
    repository.create_schema()
    repository.commit()

# Flask set-up
application = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_PATH, "templates"),
    static_folder=os.path.join(PROJECT_PATH, "static")
)

application.secret_key = GOOGLE_CLIENT_SECRET
login_manager = LoginManager()
login_manager.init_app(application)

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@login_manager.user_loader
def load_user(user_id):
    return context.repository.get_admin(user_id)


@login_manager.unauthorized_handler
def unathorized():
    return redirect(url_for("login"))


class Context:
    def __init__(self):
        self.connection = create_sqlite_connection(DATABASE_PATH)
        self.repository = Repository(self.connection)

    def __enter__(self):
        self.connection.__enter()

    def __exit__(self):
        self.connection.close()


def inject_context():
    if "context" not in g:
        g.context = Context()
    return g.context


def teardown_context(exception):
    context = g.pop("context", None)
    if context is not None:
        context.__exit__()


context = LocalProxy(inject_context)


@application.route("/", endpoint="root")
@application.route("/departments", endpoint="departments")
@login_required
def departments():
    if "sort" in request.args:
        departments = context.repository.get_departments_desc()
    else:
        departments = context.repository.get_departments()
    return render_template(
        "departments.html",
        departments=departments
    )


@application.route("/login", endpoint="login")
def login():
    if request.args.get("error") == "1":
        return render_template(
            "login.html",
            error="User email not available or not verified by Google."
        )
    if request.args.get("error") == "2":
        return render_template(
            "login.html",
            error="You are not on the list of administrators"
        )
    if not request.args:
        return render_template("login.html")
    else:
        return "Smth went wrong", 400


@application.route("/authorization")
def authorization():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@application.route("/authorization/callback")
def authorization_callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return redirect(url_for("login", error="1"), 302)

    user = User(
        unique_id, users_name, users_email, picture
    )

    if context.repository.is_user_admin(user) is not True:
        error = context.repository.add_user(user)
        if not error:
            context.repository.commit()
        return redirect(url_for("login", error="2"), 302)

    login_user(user)

    return redirect(url_for("root"))


@application.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@application.route("/employees", endpoint="employees")
@login_required
def employees():
    sort = request.args.get("sort")
    direction = request.args.get("direction")
    if sort:
        if sort not in COLUMNS:
            return "Bad request", 400
        if direction == "desc":
            employees = context.repository.get_employees_desc(sort)

        else:
            employees = context.repository.get_employees(sort)
    else:
        employees = context.repository.get_employees()
    return render_template(
        "employees.html",
        employees=employees,
        departments=context.repository.get_departments()
    )


@application.route("/departments/<int:id>", endpoint="edit_department")
@login_required
def edit_department(id):
    sort = request.args.get("sort")
    direction = request.args.get("direction")
    if sort:
        if sort not in COLUMNS:
            return "Bad request", 400
        if direction == "desc":
            employees = context.repository.get_employees_by_department_id_desc(id, sort)
        else:
            employees = context.repository.get_employees_by_department_id(id, sort)
    else:
        employees = context.repository.get_employees_by_department_id(id)
    return render_template(
        "edit_department.html",
        employees=employees,
        department=context.repository.get_department_by_id(id)
    )


@application.route("/departments/search", endpoint="search-departments")
@login_required
def display_department_search_result():
    sort_field = request.args.get("sort")
    search_query = request.args.get("q")
    if sort_field:
        if sort_field != "id":
            return "Bad request", 400
        departments = context.repository.search_department_by_name_desc(
            search_query)
    else:
        departments = context.repository.search_department_by_name(search_query)
    if not departments:
        return "No results", 418
    if search_query:
        return render_template(
            "departments.html",
            departments=departments,
            search_query=request.args["q"]
        )


@application.route("/departments/<int:id>/search", endpoint="search-in-department")
@login_required
def search_in_department_view(id):
    sort_field = request.args.get("sort")
    direction = request.args.get("direction")
    search_query = request.args.get("q")
    if sort_field:
        if sort_field not in COLUMNS:
            return "Bad request", 400
        if direction == "desc":
            employees = context.repository.search_employees_in_department_desc(
                id, search_query, sort_field)
        else:
            employees = context.repository.search_employees_in_department(id,
                                                                          search_query,
                                                                          sort_field)
    else:
        employees = context.repository.search_employees_in_department(id,
                                                                      search_query)
    if not employees:
        return "No results", 418
    if search_query:
        return render_template(
            "edit_department.html",
            department=context.repository.get_department_by_id(id),
            employees=employees,
            search_query=search_query
        )


@application.route("/employees/search", endpoint="search-employees")
@login_required
def display_employees_search_result():
    sort_field = request.args.get("sort")
    direction = request.args.get("direction")
    search_query = request.args.get("q")
    if sort_field:
        if sort_field not in COLUMNS:
            return "Bad request", 400
        if direction == "desc":
            employees = context.repository.search_employees_desc(search_query,
                                                                 sort_field)
        else:
            employees = context.repository.search_employees(search_query,
                                                            sort_field)
    else:
        employees = context.repository.search_employees(search_query)
    if not employees:
        return "No results", 418
    if search_query:
        return render_template(
            "employees.html",
            employees=employees,
            departments=context.repository.get_departments(),
            search_query=search_query
        )


@application.route("/employees/<int:id>", endpoint="edit_employee")
@login_required
def edit_employee(id):
    employee = context.repository.get_employee_by_id(id)
    if employee == "Incorrect data":
        return "Incorrect data", 418
    return render_template(
        "edit_employee.html",
        employee=employee,
        departments=context.repository.get_departments()
    )


@application.route("/admins", endpoint="admins")
@login_required
def admins():
    admins = context.repository.get_admins()
    users = context.repository.get_users()
    return render_template(
        "admins.html",
        admins=admins,
        users=users
    )


@application.route("/api/departments/<int:id>", methods=["DELETE"])
@login_required
def delete_department(id):
    context.repository.delete_department(id)
    context.repository.commit()
    return "", 204


@application.route("/api/employees/<int:id>/<int:department_id>", methods=["DELETE"])
@login_required
def delete_employee(id, department_id):
    context.repository.delete_employee(id, department_id)
    context.repository.commit()
    return "", 204


@application.route("/api/departments/new-department", methods=["POST"])
@login_required
def new_department():
    new_department_data = Department.from_tuple(
        tuple([0] + request.data.decode("utf-8").split(",")))
    error = context.repository.add_department(
        new_department_data.name,
        new_department_data.country,
        new_department_data.city,
        new_department_data.address,
        new_department_data.department_manager
    )
    if error == "DEPARTMENT NAME DUPLICATE":
        return "This department name is occupied", 400
    context.repository.commit()
    return "", 204


@application.route("/api/employees/new-employee", methods=["POST"])
@login_required
def new_employee():
    new_employee_data = Employee.from_tuple(
        tuple([0] + request.data.decode("utf-8").split(",")))
    error = context.repository.add_employee(
        new_employee_data.department_id,
        new_employee_data.first_name,
        new_employee_data.last_name,
        new_employee_data.gender,
        new_employee_data.age,
        new_employee_data.position,
        new_employee_data.salary
    )
    if error == "DUPLICATE MEMBERS":
        return "Duplicate members", 400
    context.repository.commit()
    return "", 204


@application.route("/api/department/<int:id>/rename", methods=["POST"])
@login_required
def rename_department(id):
    new_name = request.data.decode("utf-8")
    error = context.repository.rename_department(id, new_name)
    if error == "DUPLICATE NAMES":
        return "DUPLICATE NAMES", 418
    context.repository.commit()
    return "", 204


@application.route("/api/employees/<int:id>/edit", methods=["POST"])
@login_required
def edit_employee_api(id):
    error = context.repository.edit_employee(Employee.from_tuple(
        [id] + request.data.decode("utf-8").split(",")
    ))
    if error:
        return error, 418
    context.repository.commit()
    return "", 204


@application.route("/api/admins/add", methods=["POST"])
@login_required
def add_admin():
    id = request.data.decode("utf-8")
    user = context.repository.get_user(id)
    error = context.repository.add_admin(user)
    if error == "Duplicate admins":
        return error, 418
    context.repository.delete_user(id)
    context.repository.commit()
    return "", 204


if __name__ == "__main__":
    application.run(ssl_context="adhoc", port=443)
