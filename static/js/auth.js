function togglePassword(){
    const password = document.getElementById("password");
    const pass_confirm = document.getElementById("pass_confirm");
    const toggleButton = document.getElementById('eye');
    if(password.type =="password"){
        password.type ="text";
        pass_confirm.type = "text";
        toggleButton.className  = 'fa-solid fa-eye-slash';

    }
    else{   
        password.type ="password";
        pass_confirm.type = "password";
        toggleButton.className = 'fa-solid fa-eye';
    }
}
function confirm_password(){
    const psw1 = document.getElementById("password");
    const psw2 = document.getElementById("pass_confirm");
    console.log(psw1.value);
    console.log(psw2.value);
    if(!(psw1.value==psw2.value)){
        alert("passwords are not similare!");
        return false;
    }
    return true;
}

function updateFileName() {
    // Get the file input element
    const fileInput = document.getElementById('file');
    // Get the file label element
    const fileLabel = document.getElementById('fileLabel');

    // Check if a file is selected
    if (fileInput.files.length > 0) {
      // Update the label text with the selected file name
      fileLabel.textContent = 'Selected file: ' + fileInput.files[0].name;
    }
  }
  function showPassRegister(){
    const icon = document.getElementById("showPass");
    const pass = document.getElementById("password");
    const confirm = document.getElementById("pass_confirm");
    const label = document.getElementById("labelpass");
    if(pass.type =="password"){
        pass.type = "text";
        confirm.type = "text";
        icon.className = "fa-solid fa-circle-check";
        label.innerHTML = "Hide Password"
    }else{
        pass.type = "password";
        confirm.type = "password";
        icon.className = "fa-regular fa-circle-check";
        label.innerHTML = "Show Password"
    }
}