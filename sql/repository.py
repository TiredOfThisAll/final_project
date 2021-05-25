import sqlite3

from models.department import Department
from models.employee import Employee
from models.user import User


columns = {"id", "department_id", "age", "salary"}


class Repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def create_schema(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                country TEXT NOT NULL,
                city TEXT NOT NULL,
                address TEXT NOT NULL,
                department_manager TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            department_id INTEGER NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            position TEXT NOT NULL,
            salary INTEGER NOT NULL,
            FOREIGN KEY (department_id)
                REFERENCES departments (id)
                    ON DELETE CASCADE
                    ON UPDATE NO ACTION
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
            user_id text UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            profile_pic TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            profile_pic TEXT NOT NULL
            )
        """)

    def add_department(
            self,
            department_name,
            country,
            city,
            address,
            department_manager
    ):
        try:
            self.cursor.execute("""
                INSERT INTO departments(
                name,
                country,
                city,
                address,
                department_manager
                )
                VALUES (
                :name,
                :country,
                :city,
                :address,
                :department_manager
                )
            """, {
                "name": department_name,
                "country": country,
                "city": city,
                "address": address,
                "department_manager": department_manager,
            })
        except sqlite3.IntegrityError as integrity_error:
            if str(integrity_error) \
                    == "UNIQUE constraint failed: departments.name":
                return "DEPARTMENT NAME DUPLICATE"
            raise integrity_error

    def add_employee(
            self,
            department_id,
            first_name,
            last_name,
            gender,
            age,
            position,
            salary
    ):
        try:
            self.cursor.execute("""
                INSERT INTO employees (
                    department_id,
                    first_name,
                    last_name,
                    gender,
                    age,
                    position,
                    salary
                )
                VALUES (
                    :department_id,
                    :first_name,
                    :last_name,
                    :gender,
                    :age,
                    :position,
                    :salary
                )
            """, {
                "department_id": department_id,
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "age": age,
                "position": position,
                "salary": salary
            })
        except sqlite3.IntegrityError:
            return "DUPLICATE MEMBERS"

    def add_admin(self, user):
        self.cursor.execute("""
            INSERT INTO admins (user_id, name, email, profile_pic)
            VALUES (:id, :name, :email, :picture)
        """, {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "picture": user.picture
        })

    def edit_employee(self, employee):
        try:
            self.cursor.execute("""
                UPDATE employees
                SET department_id = :department_id,
                first_name = :first_name,
                last_name = :last_name,
                gender = :gender,
                age = :age,
                position = :position,
                salary = :salary
                WHERE id = :id
            """, {
                "id": employee.id,
                "department_id": employee.department_id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "gender": employee.gender,
                "age": employee.age,
                "position": employee.position,
                "salary": employee.salary
            })
        except sqlite3.Error as er:
            return er

    def get_departments(self):
        department_tuples = self.cursor.execute("""
            SELECT *
            FROM departments
            ORDER BY id
        """).fetchall()
        return list(map(Department.from_tuple, department_tuples))

    def get_departments_desc(self):
        departments_tuple = self.cursor.execute("""
            SELECT *
            FROM departments
            ORDER BY id DESC
        """).fetchall()
        return list(map(Department.from_tuple, departments_tuple))

    def get_department_by_id(self, id):
        return Department.from_tuple(self.cursor.execute("""
            SELECT *
            FROM departments
            WHERE id = ?
        """, (id,)).fetchone())

    def get_employees(self, column="id"):
        if column not in columns:
            return "Bad request"
        employee_tuples = self.cursor.execute(f"""
            SELECT *
            FROM employees
            ORDER BY {column}
        """).fetchall()
        return list(map(Employee.from_tuple, employee_tuples))

    def get_employees_desc(self, column="id"):
        if column not in columns:
            return "Bad request"
        employees_tuple = self.cursor.execute(f"""
            SELECT *
            FROM employees
            ORDER BY {column} DESC
        """).fetchall()
        return list(map(Employee.from_tuple, employees_tuple))

    def get_employees_by_department_id(self, id, column="id"):
        if column not in columns:
            return "Bad request"
        employee_tuples = self.cursor.execute(f"""
            SELECT *
            FROM employees
            WHERE department_id = ?
            ORDER BY {column}
        """, (id, )).fetchall()
        return list(map(Employee.from_tuple, employee_tuples))

    def get_employees_by_department_id_desc(self, id, column="id"):
        if column not in columns:
            return "Bad request"
        employee_tuples = self.cursor.execute(f"""
            SELECT *
            FROM employees
            WHERE department_id = ?
            ORDER BY {column} DESC
        """, (id, )).fetchall()
        return list(map(Employee.from_tuple, employee_tuples))

    def get_employee_by_id(self, id):
        employee = self.cursor.execute("""
                SELECT *
                FROM employees
                WHERE id = ?
            """, (id,)).fetchone()
        if not employee:
            return "Incorrect data"
        return Employee.from_tuple(employee)

    def get_admins(self):
        admins_tuple = self.cursor.execute("""
            SELECT *
            FROM admins
        """).fetchall()
        return list(map(User.from_tuple, admins_tuple))

    def get_admin(self, user_id):
        user = self.cursor.execute("""
            SELECT *
            FROM admins
            WHERE user_id = ?
        """, (user_id,)).fetchone()
        if not user:
            return None
        return User.from_tuple(user)

    def is_user_admin(self, user):
        user_tuple = self.cursor.execute("""
            SELECT *
            FROM admins
            WHERE user_id = ?
        """, (user.id, ))
        return user_tuple is not None

    def delete_department(self, id):
        self.cursor.execute("""
            DELETE
            FROM departments
            WHERE id = ?
        """, (id,))

    def delete_employee(self, id, department_id):
        self.cursor.execute("""
            DELETE
            FROM employees
            WHERE id = ? AND department_id = ?
        """, (id, department_id))

    def search_department_by_name(self, search_query):
        search_tuples = self.cursor.execute("""
            SELECT *
            FROM departments
            WHERE name LIKE ?
        """, ("%" + search_query + "%",)).fetchall()
        return list(map(Department.from_tuple, search_tuples))

    def search_department_by_name_desc(self, search_query):
        search_tuples = self.cursor.execute("""
            SELECT *
            FROM departments
            WHERE name LIKE ?
            ORDER BY id DESC
        """, ("%" + search_query + "%",)).fetchall()
        return list(map(Department.from_tuple, search_tuples))

    def search_employees(self, search_query, column="id"):
        if column not in columns:
            return "Bad request"
        search_query = "%" + search_query + "%"
        employees_tuple = self.cursor.execute(f"""
            SELECT *
            FROM employees
            WHERE first_name LIKE ? OR last_name LIKE ?
            ORDER BY {column}
        """, (search_query, search_query)).fetchall()
        return list(map(Employee.from_tuple, employees_tuple))

    def search_employees_desc(self, search_query, column="id"):
        if column not in columns:
            return "Bad request"
        search_query = "%" + search_query + "%"
        employees_tuple = self.cursor.execute(f"""
            SELECT *
            FROM employees
            WHERE first_name LIKE ? OR last_name LIKE ?
            ORDER BY {column} DESC
        """, (search_query, search_query)).fetchall()
        return list(map(Employee.from_tuple, employees_tuple))

    def search_employees_in_department(self, id, search_query, column="id"):
        if column not in columns:
            return "Bad request"
        search_query = "%" + search_query + "%"
        employees_tuple = self.cursor.execute(f"""
            SELECT *
            FROM employees
            WHERE (first_name LIKE ? OR last_name LIKE ?) AND department_id = ?
            ORDER BY {column}
        """, (search_query, search_query, id)).fetchall()
        return list(map(Employee.from_tuple, employees_tuple))

    def search_employees_in_department_desc(self, id, search_query, column="id"):
        if column not in columns:
            return "Bad request"
        search_query = "%" + search_query + "%"
        employees_tuple = self.cursor.execute(f"""
            SELECT *
            FROM employees
            WHERE (first_name LIKE ? OR last_name LIKE ?) AND department_id = ?
            ORDER BY {column} DESC
        """, (search_query, search_query, id)).fetchall()
        return list(map(Employee.from_tuple, employees_tuple))

    def rename_department(self, id, new_name):
        try:
            self.cursor.execute("""
                UPDATE departments
                SET name = ?
                WHERE id = ?
            """, (new_name, id))
        except sqlite3.IntegrityError:
            return "DUPLICATE NAMES"

    def commit(self):
        self.connection.commit()
