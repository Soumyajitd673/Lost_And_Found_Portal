const otpEmailInput = document.querySelector("#inputEmail");
const sendOtpButton = document.querySelector("#sendOtpBtn");
const emailStatusMessage = document.querySelector("#emailStatus");

const otpSection = document.querySelector("#otpSection");
const otpCodeInput = document.querySelector("#inputOtp");
const verifyOtpButton = document.querySelector("#verifyOtpBtn");
const otpStatusMessage = document.querySelector("#otpStatus");

const registerButton = document.querySelector("#registerBtn");


sendOtpButton.addEventListener("click", async function () {
    const email = otpEmailInput.value.trim();

    if (!otpEmailInput.checkValidity()) {
        emailStatusMessage.textContent = "Enter a valid email address.";
        return;
    }

    if (!email.toLowerCase().endsWith("@iitbhilai.ac.in")) {
        emailStatusMessage.textContent = "Use your college email address.";
        return;
    }

    emailStatusMessage.textContent = "Sending OTP...";

    try {
        const response = await fetch("/otp/request", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email: email })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Could not send OTP.");
        }

        emailStatusMessage.textContent = result.message;
        otpSection.style.display = "block";
    } catch (error) {
        emailStatusMessage.textContent = error.message || "Could not connect to the server.";
    }
});


verifyOtpButton.addEventListener("click", async function () {
    const email = otpEmailInput.value.trim();
    const otp = otpCodeInput.value.trim();

    if (!/^[0-9]{6}$/.test(otp)) {
        otpStatusMessage.textContent = "Enter the 6-digit OTP.";
        return;
    }

    otpStatusMessage.textContent = "Checking OTP...";

    try {
        const response = await fetch("/otp/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                otp: otp
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "OTP verification failed.");
        }

        otpStatusMessage.textContent = result.message;
        otpEmailInput.disabled = true;
        otpCodeInput.disabled = true;
        sendOtpButton.disabled = true;
        verifyOtpButton.disabled = true;
        registerButton.disabled = false;
    } catch (error) {
        otpStatusMessage.textContent = error.message || "Could not connect to the server.";
    }
});
