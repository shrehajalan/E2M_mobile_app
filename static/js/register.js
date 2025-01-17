function validateForm() {
    var userName = document.getElementById("userName").value;
    var emailId = document.getElementById("emailId").value;
    var mobileNumber = document.getElementById("mobileNumber").value;
    var firmName = document.getElementById("firmName").value;
    var location = document.getElementById("location").value;
    var password = document.getElementById("password").value;
    var state = document.getElementById("state").value;
    var country = document.getElementById("country").value;

    if (userName === "" || emailId === "" || mobileNumber === "" || firmName === "" || location === "" || password === "" || state === "" || country === "") {
        alert("All fields must be filled out");
        return false;
    }

    if (mobileNumber.length !== 10) {
        alert("Mobile number must be 10 digits long");
        return false;
    }

    if (password.length < 10) {
        alert("Password must be at least 10 characters long");
        return false;
    }

    return true;
}

async function handleFormSubmit(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    if (!validateForm()) {
        return; // Stop form submission if validation fails
    }

    var formData = {
        userName: document.getElementById("userName").value,
        emailId: document.getElementById("emailId").value,
        mobileNumber: document.getElementById("mobileNumber").value,
        firmName: document.getElementById("firmName").value,
        location: document.getElementById("location").value,
        password: document.getElementById("password").value,
        state: document.getElementById("state").value,
        country: document.getElementById("country").value
    };

    try {
        const response = await fetch('/registerSubmit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Success:', result);
            // Handle success (e.g., redirect, display message)
        } else {
            console.error('Error:', response.statusText);
            // Handle error
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('registrationForm').addEventListener('submit', handleFormSubmit);
});