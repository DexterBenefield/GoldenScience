fetch("http://localhost:3000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, username, password })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        alert("Registration successful!");
    } else {
        alert("Error: " + data.message);
    }
});
