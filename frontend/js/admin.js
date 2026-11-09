
document.addEventListener("DOMContentLoaded", () => {

    const table = document.getElementById("complaintsTable");

    async function loadAdminComplaints() {

        try {
            const response = await fetch("/api/admin/complaints");
            const result = await response.json();

            if (!response.ok) {
                table.textContent = result.message || "Unable to load complaints.";
                return;
            }

            document.getElementById("totalCount").textContent =
                result.counts.total;

            document.getElementById("pendingCount").textContent =
                result.counts.pending;

            document.getElementById("progressCount").textContent =
                result.counts.progress;

            document.getElementById("resolvedCount").textContent =
                result.counts.resolved;

            table.replaceChildren();

            if (result.complaints.length === 0) {
                table.textContent = "No complaints found.";
                return;
            }

            result.complaints.forEach((complaint) => {

                const row = document.createElement("tr");

                const values = [
                    complaint.id,
                    complaint.student_name,
                    complaint.category,
                    complaint.title,
                    complaint.location || "Not specified"
                ];

                values.forEach((value) => {
                    const cell = document.createElement("td");
                    cell.textContent = value;
                    row.appendChild(cell);
                });

                // Status dropdown
                const statusCell = document.createElement("td");
                const statusSelect = document.createElement("select");

                ["Pending", "In Progress", "Resolved"].forEach((status) => {
                    const option = document.createElement("option");
                    option.value = status;
                    option.textContent = status;
                    statusSelect.appendChild(option);
                });

                statusSelect.value = complaint.status;
                statusCell.appendChild(statusSelect);
                row.appendChild(statusCell);

                // Update button
                const actionCell = document.createElement("td");
                const updateButton = document.createElement("button");

                updateButton.type = "button";
                updateButton.textContent = "Update";

                updateButton.addEventListener("click", async () => {

                    alert("Update button clicked!");

                    updateButton.disabled = true;

                    try {
                        const updateResponse = await fetch(
                            `/api/admin/complaints/${complaint.id}`,
                            {
                                method: "PATCH",
                                headers: {
                                    "Content-Type": "application/json"
                                },
                                body: JSON.stringify({
                                    status: statusSelect.value,
                                    admin_remark: ""
                                })
                            }
                        );

                        const updateResult = await updateResponse.json();

                        if (updateResponse.ok) {
                            alert("Complaint status updated successfully!");
                            await loadAdminComplaints();
                        } else {
                            alert(updateResult.message || "Update failed.");
                        }

                    } catch (error) {
                        console.error("Update error:", error);
                        alert("Server connection error.");
                    } finally {
                        updateButton.disabled = false;
                    }
                });

                actionCell.appendChild(updateButton);
                row.appendChild(actionCell);

                table.appendChild(row);
            });

        } catch (error) {
            console.error("Dashboard error:", error);
            table.textContent = "Unable to load complaints.";
        }
    }

    loadAdminComplaints();

});
