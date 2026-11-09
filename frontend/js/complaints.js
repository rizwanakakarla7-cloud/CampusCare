
document.addEventListener("DOMContentLoaded", () => {

    const complaintForm = document.getElementById("complaintForm");
    const complaintsList = document.getElementById("complaintsList");

    // Submit Complaint
    if (complaintForm) {
        complaintForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const title = document.getElementById("title").value.trim();
            const category = document.getElementById("category").value;
            const description = document.getElementById("description").value.trim();
            const location = document.getElementById("location").value.trim();

            try {
                const response = await fetch("/api/complaints", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        title,
                        category,
                        description,
                        location
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    alert("Complaint submitted successfully!");

                    complaintForm.reset();
                    loadComplaints();
                } else {
                    alert(result.message || "Complaint submission failed.");
                }

            } catch (error) {
                console.error("Complaint error:", error);
                alert("Unable to connect to server.");
            }
        });
    }

    // Display My Complaints
    async function loadComplaints() {
        if (!complaintsList) return;

        try {
            const response = await fetch("/api/complaints");
            const result = await response.json();

            if (!response.ok) {
                complaintsList.textContent =
                    result.message || "Please login to view complaints.";
                return;
            }

            complaintsList.replaceChildren();

            if (result.complaints.length === 0) {
                complaintsList.textContent = "No complaints submitted yet.";
                return;
            }

            result.complaints.forEach((complaint) => {
                const card = document.createElement("div");
                card.className = "card";

                const heading = document.createElement("h3");
                heading.textContent = complaint.title;

                const category = document.createElement("p");
                category.textContent = "Category: " + complaint.category;

                const description = document.createElement("p");
                description.textContent = complaint.description;

                const location = document.createElement("p");
                location.textContent =
                    "Location: " + (complaint.location || "Not specified");

                const status = document.createElement("p");
                status.textContent = "Status: " + complaint.status;

                card.append(
                    heading,
                    category,
                    description,
                    location,
                    status
                );

                complaintsList.appendChild(card);
            });

        } catch (error) {
            console.error("Loading complaints error:", error);
            complaintsList.textContent = "Unable to load complaints.";
        }
    }

    loadComplaints();

});
