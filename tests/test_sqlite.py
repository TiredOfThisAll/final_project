import unittest
import sqlite3

from sql.repository import Repository
from models.user import User
from models.employee import Employee


class TestSqliteDepartments(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.repository = Repository(self.connection)
        self.repository.create_schema()
        self.repository.add_department("a", "a", "a", "a", "a")
        self.repository.commit()

    def test_add_department(self):
        departments = self.connection.execute("""
            SELECT *
            FROM departments
        """).fetchall()[0]
        self.assertEqual((1, "a", "a", "a", "a", "a"), departments)

    def test_delete_department(self):
        self.repository.delete_department(1)
        departments = self.connection.execute("""
            SELECT *
            FROM departments
        """).fetchall()
        self.assertEqual([], departments)

    def test_search_department(self):
        department_model = self.repository.search_department_by_name("a")[0]
        department = (department_model.id,
                      department_model.name,
                      department_model.country,
                      department_model.city,
                      department_model.address,
                      department_model.department_manager)
        self.assertEqual((1, "a", "a", "a", "a", "a"), department)

    def test_rename_department(self):
        self.repository.rename_department(1, "b")
        departments = self.connection.execute("""
            SELECT *
            FROM departments
        """).fetchall()[0]
        self.assertEqual((1, "b", "a", "a", "a", "a"), departments)


class TestSqliteEmployees(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.repository = Repository(self.connection)
        self.repository.create_schema()
        self.repository.add_department("a", "a", "a", "a", "a")
        self.repository.add_employee(1, "a", "a", "a", 1, "a", 1)
        self.repository.commit()

    def test_add_employee(self):
        employees = self.connection.execute("""
            SELECT *
            FROM employees
        """).fetchall()[0]
        self.assertEqual((1, 1, "a", "a", "a", 1, "a", 1), employees)

    def test_delete_employee(self):
        self.repository.delete_employee(1, 1)
        employees = self.connection.execute("""
            SELECT *
            FROM employees
        """).fetchall()
        self.assertEqual([], employees)

    def test_edit_employee(self):
        self.repository.edit_employee(Employee(
            1, 1, "b", "b", "b", 1, "b", 1
        ))
        employees = self.connection.execute("""
            SELECT *
            FROM employees
        """).fetchall()[0]
        self.assertEqual((1, 1, "b", "b", "b", 1, "b", 1), employees)

    def test_search_employee(self):
        employee_model = self.repository.search_employees("a")[0]
        employee = (employee_model.id,
                    employee_model.department_id,
                    employee_model.first_name,
                    employee_model.last_name,
                    employee_model.gender,
                    employee_model.age,
                    employee_model.position,
                    employee_model.salary)
        self.assertEqual((1, 1, "a", "a", "a", 1, "a", 1), employee)


class TestSqliteUsers(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.repository = Repository(self.connection)
        self.repository.create_schema()
        self.repository.add_user(User("a", "a", "a", "a"))
        self.repository.commit()

    def test_add_user(self):
        users = self.connection.execute("""
            SELECT *
            FROM users
        """).fetchall()[0]
        self.assertEqual(("a", "a", "a", "a"), users)

    def test_delete_user(self):
        self.repository.delete_user("a")
        users = self.connection.execute("""
            SELECT *
            FROM users
        """).fetchall()
        self.assertEqual([], users)


if __name__ == "__name__":
    unittest.main()
