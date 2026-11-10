let btnreport = document.querySelector(".btn-report");
btnreport.addEventListener("click", function(){
    confirm("Confirm report")
    btnreport.textContent = "Reported";
    btnreport.classList.remove("btn-report");
    btnreport.classList.add("reported");
})