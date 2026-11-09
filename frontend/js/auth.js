
document.addEventListener("DOMContentLoaded", () => {

    // STUDENT REGISTRATION
    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const full_name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const student_id = document.getElementById("studentId").value.trim();
            const department = document.getElementById("department").value.trim();
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirmPassword").value;

            if (password !== confirmPassword) {
                alert("Passwords do not match!");
                return;
            }

            if (password.length < 8) {
                alert("Password must contain at least 8 characters.");
                return;
            }

            try {
                const response = await fetch(
                    "/api/auth/register",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            full_name,
                            email,
                            student_id,
                            department,
                            password
                        })
                    }
                );

                const result = await response.json();

                if (response.ok) {
                    alert("Registration successful! Please login.");
                    window.location.href = "login.html";
                } else {
                    alert(result.message || "Registration failed.");
                }

            } catch (error) {
                console.error("Registration error:", error);
                alert("Unable to connect to server.");
            }
        });
    }


    // STUDENT AND ADMIN LOGIN
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value;

            try {
                const response = await fetch(
                    "/api/auth/login",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            email,
                            password
                        })
                    }
                );

                const result = await response.json();

                if (response.ok) {
                    alert("Login successful!");

                    // Redirect based on user role
                    if (result.user.role === "admin") {
                        window.location.href = "admin.html";
                    } else {
                        window.location.href = "dashboard.html";
                    }

                } else {
                    alert(result.message || "Login failed.");
                }

            } catch (error) {
                console.error("Login error:", error);
                alert("Unable to connect to server.");
            }
        });
    }

});
