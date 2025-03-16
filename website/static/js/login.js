document.getElementById("login-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // ✅ Prevent standard form submission

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const errorMessage = document.getElementById("error-message");

    // Clear previous errors
    errorMessage.innerText = "";
    errorMessage.style.color = "red";

    if (!email && !password) {
        errorMessage.innerText = "Please enter both email and password.";
        return;
    }
    else if(!email){
        errorMessage.innerText = "Please enter email.";
        return;
    }
    else if (!password){
        errorMessage.innerText = "Please enter password";
        return;
    }

    try {
        console.log("Sending request to /sign_in...");

        const response = await fetch("/sign_in", {
            method: "POST",
            headers: {
                "Content-Type": "application/json" // ✅ Ensure JSON content type
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const result = await response.json();
        console.log("Server Response:", result);

        if (response.ok && result.redirect) {
            // ✅ Redirect on success
            window.location.href = result.redirect;
        } else {
            // ❌ If no redirect, show the error message
            errorMessage.innerText = result.message || "Invalid email or password.";
            console.error("Sign-in failed:", result);
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        errorMessage.innerText = "Failed to connect to the server. Please try again later.";
    }
});
