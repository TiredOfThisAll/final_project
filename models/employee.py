class Employee:
    def __init__(
            self,
            id,
            department_id,
            first_name,
            last_name,
            gender,
            age,
            position,
            salary
    ):
        self.id = id
        self.department_id = department_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age
        self.position = position
        self.salary = salary

    def from_tuple(employee_tuple):
        return Employee(*employee_tuple)

    def __str__(self):
        return "Employee: " \
               + f"id = {self.id}, " \
               + f"department_id = {self.department_id}, " \
               + f"first_name = {self.first_name}" \
               + f"last_name = {self.last_name}" \
               + f"gender = {self.gender}, " \
               + f"age = {self.age}, " \
               + f"position = {self.position}" \
               + f"salary = {self.salary}"
