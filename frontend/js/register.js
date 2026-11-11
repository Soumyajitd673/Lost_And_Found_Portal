const emailRegex = /^[a-zA-Z0-9._%+-]+@iitbhilai\.ac\.in$/;
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
const nameRegex = /^[a-zA-Z ]+$/;


let inputName = document.querySelector("#inputName");

let inputEmail = document.querySelector("#inputEmail");
let inputPass = document.querySelector("#inputPass");
let confirmPass = document.querySelector("#confirmPass");

let registerForm = document.querySelector("#registerForm");

registerForm.addEventListener("submit", function(event) {
    event.preventDefault();

    if (inputName.value.trim().length === 0) {
        alert("Please enter your name");
        return;
    }

    if (!nameRegex.test(inputName.value.trim())) {
        alert("Invalid name");
        return;
    }
    if (inputEmail.value.length === 0) {
        alert("Please enter your college email");
        return;
    }

    if (!emailRegex.test(inputEmail.value.trim())) {
        alert("Invalid college email");
        return;
    }

    if (inputPass.value.length === 0) {
        alert("Please enter your password");
        return;
    }

    if (!passwordRegex.test(inputPass.value.trim())) {
        alert("Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one digit and one special character");
        return;
    }

    if (confirmPass.value.length === 0) {
        alert("Please confirm your password");
        return;
    }

    if (inputPass.value !== confirmPass.value) {
        alert("Passwords do not match");
        return;
    }

    
   const userData = {
    name: inputName.value.trim(),
    email: inputEmail.value.trim(),
    password: inputPass.value
};

fetch("/user/register", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(userData)
})
.then(response => {
    if (!response.ok) {
        return response.json().then(error => {
            throw new Error(error.detail || "Registration failed");
        });
    }

    return response.json();
})
.then(data => {
    alert("Registration successful!");
    window.location.href = "/user/dashboard";
})
.catch(error => {
    alert(error.message);
    console.error(error);
});
    
});