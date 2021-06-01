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
        self.repository.commit()

    def tearDown(self):
        self.connection.close()

    def test_add_department(self):
        # arrange
        new_department = ("Sales", "Ukraine", "Lviv", "Prospect Lenina", "Li")

        # act
        self.repository.add_department(*new_department)

        # assert
        departments = self.connection.execute("""
            SELECT *
            FROM departments
        """).fetchall()
        self.assertEqual([(1,) + new_department], departments)

    def test_delete_department(self):
        # arrange
        new_department = ("Sales", "Ukraine", "Lviv", "Prospect Lenina", "Li")
        self.repository.add_department(*new_department)

        # act
        self.repository.delete_department(1)

        # assert
        departments = self.connection.execute("""
            SELECT *
            FROM departments
        """).fetchall()
        self.assertEqual([], departments)

    def test_search_department(self):
        # arrange
        new_department = ("Sales", "Ukraine", "Lviv", "Prospect Lenina", "Li")
        self.repository.add_department(*new_department)

        # act
        department_model = self.repository.search_department_by_name("Sales")[0]

        # assert
        department = (department_model.id,
                      department_model.name,
                      department_model.country,
                      department_model.city,
                      department_model.address,
                      department_model.department_manager)
        self.assertEqual((1,) + new_department, department)

    def test_rename_department(self):
        # arrange
        new_department = ("Sales", "Ukraine", "Lviv", "Prospect Lenina", "Li")
        self.repository.add_department(*new_department)

        # act
        self.repository.rename_department(1, "Delivery")

        # assert
        departments = self.connection.execute("""
            SELECT *
            FROM departments
        """).fetchall()
        self.assertEqual([(1, "Delivery") + new_department[1:]], departments)


class TestSqliteEmployees(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.repository = Repository(self.connection)
        self.repository.create_schema()
        self.repository.commit()

    def test_add_employee(self):
        # assert
        department = ("Sales", "Ukraine", "Lviv", "Prospect Lenina", "Li")
        employee = (1, "Danil", "Danilovich", "Male", 23, "Middle dev", 2000)
        self.repository.add_department(*department)

        # act
        self.repository.add_employee(*employee)

        employees = self.connection.execute("""
            SELECT *
            FROM employees
        """).fetchall()
        self.assertEqual([(1,) + employee], employees)

    def test_delete_employee(self):
        # assert
        department = ("Sales", "Ukraine", "Lviv", "Prospect Lenina", "Li")
        employee = (1, "Danil", "Danilovich", "Male", 23, "Middle dev", 2000)
        self.repository.add_department(*department)
        self.repository.add_employee(*employee)

        # act
        self.repository.delete_employee(1, 1)

        # assert
        employees = self.connection.execute("""
            SELECT *
            FROM employees
        """).fetchall()
        self.assertEqual([], employees)

    def test_edit_employee(self):
        # assert
        department = ("Sales", "Ukraine", "Lviv", "Prospect Lenina", "Li")
        employee = (1, "Danil", "Danilovich", "Male", 23, "Middle dev", 2000)
        self.repository.add_department(*department)
        self.repository.add_employee(*employee)

        # act
        edit_employee = (
            1, 1, "Anton", "Antonovich", "Male", 19, "Junior dev", 800
        )
        self.repository.edit_employee(Employee(*edit_employee))

        # assert
        employees = self.connection.execute("""
            SELECT *
            FROM employees
        """).fetchall()
        self.assertEqual([edit_employee], employees)

    def test_search_employee(self):
        # assert
        department = ("Sales", "Ukraine", "Lviv", "Prospect Lenina", "Li")
        employee = (1, "Danil", "Danilovich", "Male", 23, "Middle dev", 2000)
        self.repository.add_department(*department)
        self.repository.add_employee(*employee)

        # act
        employee_model = self.repository.search_employees("Danil")[0]
        search_employee = (employee_model.id,
                    employee_model.department_id,
                    employee_model.first_name,
                    employee_model.last_name,
                    employee_model.gender,
                    employee_model.age,
                    employee_model.position,
                    employee_model.salary)

        # assert
        self.assertEqual((1,) + employee, search_employee)


class TestSqliteUsers(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.repository = Repository(self.connection)
        self.repository.create_schema()
        self.repository.commit()

    def test_add_user(self):
        # assert
        user = ("88005553535", "Danil", "Danil@gmail.com", "some_ref")

        # act
        self.repository.add_user(User(*user))

        # assert
        users = self.connection.execute("""
            SELECT *
            FROM users
        """).fetchall()
        self.assertEqual([user], users)

    def test_delete_user(self):
        # assert
        user = ("88005553535", "Danil", "Danil@gmail.com", "some_ref")
        self.repository.add_user(User(*user))

        # act
        self.repository.delete_user("88005553535")

        # assert
        users = self.connection.execute("""
            SELECT *
            FROM users
        """).fetchall()
        self.assertEqual([], users)


if __name__ == "__name__":
    unittest.main()
