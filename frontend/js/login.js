const emailRegex = /^[a-zA-Z0-9._%+-]+@iitbhilai\.ac\.in$/;
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

let inputEmail = document.querySelector("#inputEmail");
let inputPass = document.querySelector("#inputPass");

let loginForm = document.querySelector("#loginForm");
loginForm.addEventListener("submit",function(event){
    event.preventDefault();
    if (inputEmail.value.length !== 0){
        if (!emailRegex.test(inputEmail.value)){
        alert("Invalid email");
        return;
    }
    }
    if (inputPass.value.length !== 0){
        if (!passwordRegex.test(inputPass.value.trim())){
        alert("Invalid password");
        return;
    }
    }
    alert("Login Successful");
    

})