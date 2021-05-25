const deleteDepartment = departmentId => {
    const isConfirmed = confirm(`Are you sure you want to delete a department with ID: ${departmentId}`);
    if (!isConfirmed) {
        return;
    }
    fetch(`/api/departments/${departmentId}`, {method: "DELETE"})
        .then(response => {
            if (response.status !== 204) {
                return Promise.reject();
            }
            location.reload();
        });
};

const deleteEmployee = (employeeId, LastName, FirstName, departmentId) => {
    const isConfirmed = confirm(`Are you sure you want to delete ${FirstName} ${LastName} with ID: ${employeeId} who works in the ${departmentId} department`);
    if (!isConfirmed) {
        return;
    }
    fetch(`/api/employees/${employeeId}/${departmentId}`, {method: "DELETE"})
        .then(response => {
            if (response.status !== 204) {
                return Promise.reject();
            }
            location.reload();
        });
};

const newDepartment = () => {
    const departmentName = document.querySelector("#new-department-name").value.trim();
    if (departmentName === "") {
        alert("Name can't consist of whitespaces or be blank");
        return;
    }
    const departmentCountry = document.querySelector("#new-department-country").value.trim();
    if (departmentCountry === "") {
        alert("Country can't consist of whitespaces or be blank");
        return;
    }
    const departmentCity = document.querySelector("#new-department-city").value.trim();
    if (departmentCity === "") {
        alert("City can't consist of whitespaces or be blank");
        return;
    }
    const departmentAddress = document.querySelector("#new-department-address").value.trim();
    if (departmentAddress === "") {
        alert("Address can't consist of whitespaces or be blank");
        return;
    }
    const departmentManager = document.querySelector("#new-department-manager").value.trim();
    if (departmentManager === "") {
        alert("Manager can't consist of whitespaces or be blank");
        return;
    }
    fetch(
        `/api/departments/new-department`,
        {
            method: "POST",
            body: [
                departmentName,
                departmentCountry,
                departmentCity,
                departmentAddress,
                departmentManager
            ]})
        .then(response => {
            if (response.status !== 204) {
                return Promise.reject();
            }
            location.reload();
        });
};

const newEmployee = () => {
    const departmentId = document.querySelector("#new-employee-department-id").value.trim()
    if (departmentId === "") {
        alert("Department id can not be unchosen");
        return;
    }
    const firstName = document.querySelector("#new-employee-name").value.trim()
    if (firstName === "") {
        alert("First name can not consist of whitespaces or be blank");
        return;
    }
    const lastName = document.querySelector("#new-employee-surname").value.trim()
    if (lastName === "") {
        alert("Last name can not consist of whitespaces or be blank");
        return;
    }
    const gender = document.querySelector("#new-employee-gender").value.trim()
    if (gender === "") {
        alert("Gender can not be unchosen");
        return;
    }
    const age = document.querySelector("#new-employee-age").value.trim()
    if (age === "") {
        alert("Age can not consist of whitespaces or be blank");
        return;
    }
    if (age < 18) {
        alert("Age cannot be lover than 18")
    }
    const position = document.querySelector("#new-employee-position").value.trim()
    if (position === "") {
        alert("Position can not consist of whitespaces or be blank");
        return;
    }
    const salary = document.querySelector("#new-employee-salary").value.trim()
    if (salary === "") {
        alert("Salary can not consist of whitespaces or be blank");
        return;
    }
    if (salary <= 0) {
        alert("Salary cannot be negative or equal to zero");
        return;
    }
    fetch(
        `/api/employees/new-employee`,
        {
            method: "POST",
            body: [
                departmentId,
                firstName,
                lastName,
                gender,
                age,
                position,
                salary
            ]})
        .then(response => {
            if (response.status !== 204) {
                return Promise.reject();
            }
            location.reload();
        });
}

const searchDepartment = () => {
    const searchQuery = document.querySelector("#search-department-by-name").value.trim();
    if (searchQuery === "") {
        alert("Search query can't consist of whitespaces or be blank");
        return;
    }
    fetch(`/departments/search?q=${searchQuery}`, {method: "GET"})
        .then(response => {
            if (response.status === 418) {
                alert("No results");
                return;
            }
            if (response.status !== 200) {
                return Promise.reject();
            }
            location.href = `/departments/search?q=${searchQuery}`;
        });
};

const searchEmployee = () => {
    const searchQuery = document.querySelector("#search-employees").value.trim();
    if (searchQuery === "") {
        alert("Search query can't consist of whitespaces or be blank");
        return;
    }
    fetch(`/employees/search?q=${searchQuery}`, {method: "GET"})
        .then(response => {
            if (response.status === 418) {
                alert("No results");
                return;
            }
            if (response.status !== 200) {
                return Promise.reject();
            }
            location.href = `/employees/search?q=${searchQuery}`;
        });
};

const searchEmployeeInDepartment = (departmentId) => {
    const searchQuery = document.querySelector("#search-employee-in-department").value.trim();
    if (searchQuery === "") {
        alert("Search query can't consist of whitespaces or be blank");
        return;
    }
    fetch(`/departments/${departmentId}/search?q=${searchQuery}`, {method: "GET"})
        .then(response => {
            if (response.status === 418) {
                alert("No results");
                return;
            }
            if (response.status !== 200) {
                return Promise.reject();
            }
            location.href = `/departments/${departmentId}/search?q=${searchQuery}`;
        });
};

const renameDepartment = (id) => {
    const newName = document.querySelector("#rename-department-input").value.trim();
    if (newName === "") {
        alert("Department name can not be blank");
        return;
    }
    fetch(`/api/department/${id}/rename`, {method: "POST", body: newName})
        .then(response => {
            if (response.status === 418) {
                alert("This name is occupied");
                return;
            }
            if (response.status !== 204) {
                return Promise.reject();
            }
            location.reload();
        });
}

const editEmployee = (id) => {
    const departmentId = document.querySelector("#edit-employee-department-id").value.trim()
    if (departmentId === "") {
        alert("Department id can not be unchosen");
        return;
    }
    const firstName = document.querySelector("#edit-employee-name").value.trim()
    if (firstName === "") {
        alert("First name can not consist of whitespaces or be blank");
        return;
    }
    const lastName = document.querySelector("#edit-employee-surname").value.trim()
    if (lastName === "") {
        alert("Last name can not consist of whitespaces or be blank");
        return;
    }
    const gender = document.querySelector("#edit-employee-gender").value.trim()
    if (gender === "") {
        alert("Gender can not be unchosen");
        return;
    }
    const age = document.querySelector("#edit-employee-age").value.trim()
    if (age === "") {
        alert("Age can not consist of whitespaces or be blank");
        return;
    }
    if (age < 18) {
        alert("Age cannot be lover than 18");
        return;
    }
    const position = document.querySelector("#edit-employee-position").value.trim()
    if (position === "") {
        alert("Position can not consist of whitespaces or be blank");
        return;
    }
    const salary = document.querySelector("#edit-employee-salary").value.trim()
    if (salary === "") {
        alert("Salary can not consist of whitespaces or be blank");
        return;
    }
    if (salary <= 0) {
        alert("Salary cannot be negative or equal to zero");
        return;
    }
    fetch(
        `/api/employees/${id}/edit`,
        {
            method: "POST",
            body: [
                departmentId,
                firstName,
                lastName,
                gender,
                age,
                position,
                salary
            ]})
        .then(response => {
            if (response.status !== 204) {
                return Promise.reject();
            }
            location.reload();
        });
}

const newAdmin = () => {
    const userId = document.querySelector("#new-admin").value.trim();
    if (userId === "") {
        alert("No users were selected");
        return;
    }
    fetch(`/api/admins/add`, {method: "POST", body:userId})
        .then(response => {
            if (response.status === 418) {
                alert("This user is already admin");
                return;
            }
            if (response.status !== 204) {
                return Promise.reject();
            }
            location.reload();
        });
};

const setFormVisibility = (formID) => {
    const myForm = document.getElementById(formID);
    myForm.style.display = myForm.style.display === "none" ? "block" : "none";
};
