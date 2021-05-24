class Department:
    def __init__(self, id, name, country, city, address, department_manager):
        self.id = id
        self.name = name
        self.country = country
        self.city = city
        self.address = address
        self.department_manager = department_manager

    def from_tuple(department_tuple):
        return Department(*department_tuple)

    def __str__(self):
        return "Department: " \
            + f"id = {self.id}, " \
            + f"name = {self.name}, " \
            + f"country = {self.country}, " \
            + f"city = {self.city}, " \
            + f"address = {self.address}, " \
            + f"department_manager = {self.department_manager}"
