const emailRegex = /^[a-zA-Z0-9._%+-]+@iitbhilai\.ac\.in$/;
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
const nameRegex = /^[a-zA-Z ]+$/;

let inputName = document.querySelector("#inputName");
let role = document.querySelector("#role");
let inputEmail = document.querySelector("#inputEmail");
let inputPass = document.querySelector("#inputPass");
let confirmPass = document.querySelector("#confirmPass");

let sendOtpBtn = document.querySelector("#sendOtpBtn");
let verifyOtpBtn = document.querySelector("#verifyOtpBtn");
let otpSection = document.querySelector("#otpSection");
let inputOtp = document.querySelector("#inputOtp");
let emailStatus = document.querySelector("#emailStatus");
let otpStatus = document.querySelector("#otpStatus");
let registerBtn = document.querySelector("#registerBtn");

let registerForm = document.querySelector("#registerForm");

let otpVerified = false;
let timer = null;


// shows a message below the email or otp box
function showMessage(box, message, type) {
    box.textContent = message;
    box.className = "status " + type;
}


// stops the user from clicking Send OTP again for 30 seconds
function startTimer() {
    let seconds = 30;
    sendOtpBtn.disabled = true;
    sendOtpBtn.textContent = "Resend in " + seconds + "s";

    timer = setInterval(function() {
        seconds = seconds - 1;
        if (seconds === 0) {
            clearInterval(timer);
            sendOtpBtn.disabled = false;
            sendOtpBtn.textContent = "Resend OTP";
        }
        else {
            sendOtpBtn.textContent = "Resend in " + seconds + "s";
        }
    }, 1000);
}


// if the email is changed, the verification is cancelled
inputEmail.addEventListener("input", function() {
    otpVerified = false;
    registerBtn.disabled = true;
    otpSection.style.display = "none";
    inputOtp.value = "";
    showMessage(emailStatus, "", "");
    showMessage(otpStatus, "", "");
});


// Send OTP button
sendOtpBtn.addEventListener("click", function() {
    if (!emailRegex.test(inputEmail.value.trim())) {
        showMessage(emailStatus, "Use your college email ending in @iitbhilai.ac.in", "error");
        return;
    }

    sendOtpBtn.disabled = true;
    showMessage(emailStatus, "Sending OTP...", "");

    fetch("http://localhost:8000/user/send-otp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email: inputEmail.value.trim() })
    }).then(response => {
        return response.json();
    }).then(data => {
        if (data.error) {
            sendOtpBtn.disabled = false;
            showMessage(emailStatus, data.error, "error");
        }
        else {
            otpSection.style.display = "block";
            showMessage(emailStatus, "OTP sent to " + inputEmail.value.trim(), "ok");
            startTimer();
        }
    }).catch(error => {
        console.log(error);
        sendOtpBtn.disabled = false;
        showMessage(emailStatus, "Server Connection Failed", "error");
    })
});


// Verify button
verifyOtpBtn.addEventListener("click", function() {
    if (inputOtp.value.trim().length !== 6) {
        showMessage(otpStatus, "Enter the 6 digit OTP", "error");
        return;
    }

    verifyOtpBtn.disabled = true;
    showMessage(otpStatus, "Verifying...", "");

    fetch("http://localhost:8000/user/verify-otp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: inputEmail.value.trim(),
            otp: inputOtp.value.trim()
        })
    }).then(response => {
        return response.json();
    }).then(data => {
        if (data.error) {
            verifyOtpBtn.disabled = false;
            showMessage(otpStatus, data.error, "error");
        }
        else {
            otpVerified = true;
            registerBtn.disabled = false;
            inputEmail.readOnly = true;
            inputOtp.readOnly = true;
            clearInterval(timer);
            sendOtpBtn.disabled = true;
            sendOtpBtn.textContent = "Verified";
            showMessage(otpStatus, "Email verified", "ok");
        }
    }).catch(error => {
        console.log(error);
        verifyOtpBtn.disabled = false;
        showMessage(otpStatus, "Server Connection Failed", "error");
    })
});


// Register button
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

    if (otpVerified === false) {
        alert("Please verify your email with the OTP first");
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
        role: role.value,
        email: inputEmail.value.trim(),
        pass: inputPass.value
    }

    fetch("http://localhost:8000/user/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    }).then(response => {
        if (!response.ok) {
            throw new Error("Registration request failed");
        }
        return response.json();
    }).then(data => {
        if (data.register === "successful") {
            alert("Registration successful");
        }
        else {
            alert("Registration Failed");
        }
    }).catch(error => {
        console.log(error);
        alert("Server Connection Failed");
    })
});