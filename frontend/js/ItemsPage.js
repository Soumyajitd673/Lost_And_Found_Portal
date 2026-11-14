document.addEventListener("DOMContentLoaded", () => {

    const categorySelect = document.getElementById("category");

    categorySelect.addEventListener("change", () => {

        const category = categorySelect.value;

        const currentPage = window.location.pathname;

        let endpoint = "";

        if (currentPage.includes("/item/lost")) {
            endpoint = "/item/lost";
        }
        else if (currentPage.includes("/item/found")) {
            endpoint = "/item/found";
        }

        if (endpoint !== "") {
            window.location.href = `${endpoint}/{category}`
        }

        fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch items");
            }
            return response.text();
        })
        .catch(error => {
            console.error(error);
        });



    });

});







let btnreport = document.querySelector(".btn-report");
btnreport.addEventListener("click", function(){
    const reporDescription = document.querySelector(".report_form_container")
    confirm("Confirm report")
    btnreport.textContent = "Reported";
    btnreport.classList.remove("btn-report");
    btnreport.classList.add("reported");
})
