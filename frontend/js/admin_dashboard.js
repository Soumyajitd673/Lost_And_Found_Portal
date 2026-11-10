const userDetail = [
    {
        reported_by : "aarav sharma",
        reported : "Rahul Verma",
        reported_by_email : "aarav@iitbhilai.ac.in",
        reported_email : "Rahul@iitbhilai.ac.in",
        description : "Reported for inappropriate behaviour during an item exchange",
        resolved : true
    },
    {
        reported_by : "aarav sharma",
        reported : "Rahul Verma",
        reported_by_email : "aarav@iitbhilai.ac.in",
        reported_email : "Rahul@iitbhilai.ac.in",
        description : "Reported for inappropriate behaviour during an item exchange",
        resolved : true
    }
]
let Users = JSON.parse(localStorage.getItem("users"));
function save_data(){
    localStorage.setItem("users",JSON.stringify(userDetail));

}

function displayUsers(user_data){
    user_data.forEach(element => {
        const reportsContainer = document.querySelector(".reports");

        const reportCard = document.createElement("div");
        reportCard.classList.add("report-card");

        const reportHeader = document.createElement("div");
        reportHeader.classList.add("report-header");

        const reportTitle = document.createElement("h3");
        reportTitle.textContent = "Report #001";

        const status = document.createElement("span");
        status.classList.add("pending");
        status.textContent = "Pending";

        reportHeader.appendChild(reportTitle);
        reportHeader.appendChild(status);

        const users = document.createElement("div");
        users.classList.add("users");

        const reporter = document.createElement("div");

        const reporterLabel = document.createElement("small");
        reporterLabel.textContent = "REPORTED BY";

        const reporterName = document.createElement("h4");
        reporterName.textContent = "Aarav Sharma";

        const reporterEmail = document.createElement("p");
        reporterEmail.textContent = "aarav@iitbhilai.ac.in";

        reporter.appendChild(reporterLabel);
        reporter.appendChild(reporterName);
        reporter.appendChild(reporterEmail);

        const reportedUser = document.createElement("div");

        const reportedLabel = document.createElement("small");
        reportedLabel.textContent = "REPORTED USER";

        const reportedName = document.createElement("h4");
        reportedName.textContent = "Rahul Verma";

        const reportedEmail = document.createElement("p");
        reportedEmail.textContent = "rahul@iitbhilai.ac.in";

        reportedUser.appendChild(reportedLabel);
        reportedUser.appendChild(reportedName);
        reportedUser.appendChild(reportedEmail);

        users.appendChild(reporter);
        users.appendChild(reportedUser);

        const description = document.createElement("p");
        description.classList.add("description");
        description.textContent =
            "Reported for inappropriate behaviour during an item exchange.";

        const resolveButton = document.createElement("button");
        resolveButton.classList.add("resolve");
        resolveButton.textContent = "Resolve Issue";

        reportCard.appendChild(reportHeader);
        reportCard.appendChild(users);
        reportCard.appendChild(description);
        reportCard.appendChild(resolveButton);

        reportsContainer.appendChild(reportCard);

        
    });
}
