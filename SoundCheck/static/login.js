//Allows log in submission
document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting to a server

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (username === credentials.username && password === credentials.password) {
        alert("Login successful!");
    } else {
        alert("Invalid username or password. Please try again.");
    }
});
