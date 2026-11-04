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
    
    const userData = {
        email : inputEmail.value.trim(),
        pass : inputPass.value.trim()
    }
     fetch("http://localhost:8000/user/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    }).then(response => {
        if (!response.ok){
            throw new Error("Login request failed");
        }
        return response.json();
    }).then(data => {
        if (data.login === "successful"){
            alert("Login successful");
        }
        else{
            alert("Login Failed");
        }
    }).catch(error => {
        console.log(error);
        alert("Server Connection Failed");
    })
    

})