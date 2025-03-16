document.getElementById("signup-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent standard form submission

    const firstName = document.getElementById("name").value.trim();
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm-password").value.trim();

    const errorMessage = document.getElementById("error-message");

    // Clear previous errors
    errorMessage.innerText = "";

    let errors = [];
    if (!firstName) errors.push("Name is required.");
    if (!username) errors.push("Username is required.");
    if (!email) errors.push("Email is required.");
    if (!password) errors.push("Password is required.");
    if (password.length < 8) errors.push("Password must be at least 8 characters.");
    if (password !== confirmPassword) errors.push("Passwords do not match.");

    if (errors.length > 0) {
        errorMessage.innerText = errors.join(" ");
        return;
    }

    try {
        console.log("Sending request...");

        const response = await fetch("/sign_up", {
            method: "POST",
            headers: {
                "Content-Type": "application/json", // ✅ Ensure JSON content type
            },
            body: JSON.stringify({
                name: firstName,
                username: username,
                email: email,
                password: password,
                confirm_password: confirmPassword
            })
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message);
            if (result.redirect) {
                window.location.href = result.redirect;
            }
        } else {
            errorMessage.innerText = result.message || "An error occurred. Please try again.";
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        errorMessage.innerText = "Failed to connect to the server. Please try again later.";
    }
});
