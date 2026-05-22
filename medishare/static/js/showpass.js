function showpass() {
  const passwordInput = document.getElementById("pass");

  if (!passwordInput) {
    return;
  }

  passwordInput.type = passwordInput.type === "password" ? "text" : "password";
}