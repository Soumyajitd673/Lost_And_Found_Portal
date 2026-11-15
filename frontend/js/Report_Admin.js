const reportButtons = document.querySelectorAll(".report_to_admin_btn");

reportButtons.forEach(button => {
    const tdCell = button.closest("td");
    const formContainer = tdCell.querySelector(".report_form_container");
    const descriptionInput = tdCell.querySelector(".report_description");
    const submitBtn = tdCell.querySelector(".submit_report_btn");
    const cancelBtn = tdCell.querySelector(".cancel_report_btn");

    const itemId = button.getAttribute("data-item-id");
    const reporterEmail = button.getAttribute("data-reporter-email");

    // Click "Report to Admin" -> Show text box
    button.addEventListener("click", () => {
        formContainer.style.display = "block";
        button.style.display = "none";
        descriptionInput.focus();
    });

    // Cancel action -> Reset
    cancelBtn.addEventListener("click", () => {
        formContainer.style.display = "none";
        button.style.display = "inline-block";
        descriptionInput.value = "";
    });

    // Click Submit -> Validate text -> Ask for confirmation
    submitBtn.addEventListener("click", () => {
        const description = descriptionInput.value.trim();

        if (!description) {
            alert("Please enter a description before submitting.");
            return;
        }

        const isConfirmed = confirm("Are you sure you want to send this report to the admin?");

        if (isConfirmed) {
            fetch('/report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    reported_user_email: reporterEmail,
                    report_description: description
                })
            })
            .then(response => {
                if (!response.ok) throw new Error("Failed to submit report");

                return response.json();
            })
            .then(data => {

                if (data === true) {
                    alert("Report submitted successfully!");
                    formContainer.style.display = "none";
                    button.style.display = "inline-block";
                    descriptionInput.value = "";
                } else {
                    alert("Something went wrong.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred while submitting the report.");
            });
        }
    });
});