
document.getElementById("loginForm").addEventListener("submit", function(event) {
event.preventDefault(); // Prevent default form submission

var mobileNumber = document.getElementById("mobileNumber").value;
var password = document.getElementById("password").value;

// Validate form data
if (!/^\d{10}$/.test(mobileNumber)) {
    alert("Mobile number must be exactly 10 digits.");
    return;
}

if (password.length < 10) {
    alert("Password must be at least 10 characters long.");
    return;
}

// Create a JSON object from the form data
var formData = {
    mobileNumber: mobileNumber,
    password: password
};

// Send the form data as JSON
fetch("/loginSubmit", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
})
.then(response => response.json())
.then(data => {
    console.log(data); // Handle the response from the server
    // You can add code here to handle successful login or show messages
})
.catch(error => {
    console.error("Error:", error);
    // You can add code here to handle errors
});
});
