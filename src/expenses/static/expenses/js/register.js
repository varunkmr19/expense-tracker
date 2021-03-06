const submitButton = document.querySelector(".submit-btn");

const usernameField = document.querySelector("#username");
const usernameFeedback = document.querySelector("#username-feedback");

const emailField = document.querySelector("#email");

emailField.addEventListener("keyup", (e) => {
  // remove existing classes
  emailField.classList.remove("is-invalid"); // red border
  emailField.classList.remove("is-valid"); // green border

  // get email
  const email = e.target.value;

  // make API call
  if (email.length > 0) {
    fetch("/auth/validate_email", {
      body: JSON.stringify({ email: email }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          submitButton.disabled = true;
          emailField.classList.add("is-invalid");
        } else {
          submitButton.removeAttribute("disabled");
          emailField.classList.add("is-valid");
        }
      });
  }
});

usernameField.addEventListener("keyup", (e) => {
  usernameField.classList.remove("is-invalid");
  usernameField.classList.remove("is-valid");
  usernameFeedback.classList.remove("invalid-feedback");
  usernameFeedback.classList.remove("valid-feedback");
  usernameFeedback.style.display = "none";
  // get username
  const username = e.target.value;
  // make API call
  if (username.length > 0) {
    fetch("/auth/validate_username", {
      body: JSON.stringify({ username: username }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.error) {
          submitButton.disabled = true;
          usernameField.classList.add("is-invalid");
          usernameFeedback.style.display = "block";
          usernameFeedback.classList.add("invalid-feedback");
          usernameFeedback.innerHTML = `<p>${data.error}</p>`;
        } else {
          submitButton.removeAttribute("disabled");
          usernameFeedback.innerHTML = `<p>${username} is avaliable.</p>`;
          usernameFeedback.style.display = "block";
          usernameFeedback.classList.add("valid-feedback");
          usernameField.classList.add("is-valid");
        }
      });
  }
});

// show password toggle
const showPasswordCheckBox = document.querySelector("#show-password-toggle");

showPasswordCheckBox.addEventListener("click", () => {
  // get password field
  const passwordField = document.querySelector("#password");
  if (passwordField.type === "password") {
    passwordField.type = "text";
  } else {
    passwordField.type = "password";
  }
});
