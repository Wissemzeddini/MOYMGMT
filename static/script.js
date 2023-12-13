const body = document.querySelector('body'),
      sidebar = body.querySelector('nav'),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");


toggle.addEventListener("click" , () =>{
    sidebar.classList.toggle("close");
})

searchBtn.addEventListener("click" , () =>{
    sidebar.classList.remove("close");
})

modeSwitch.addEventListener("click" , () =>{
    body.classList.toggle("dark");
    
    if(body.classList.contains("dark")){
        modeText.innerText = "Light mode";
    }else{
        modeText.innerText = "Dark mode";
        
    }
});

function legand(id){
    elm = document.getElementById(id);
    var hasLegend = elm.querySelector("legend") !== null;
    if (! hasLegend) {
        elm.innerHTML += "<legend>"+id+"</legend>";
        if (id=="Username"){
            document.getElementById("user").placeholder = "";
            document.getElementById("user").focus();
        }
        else{
            document.getElementById("pass").placeholder = "";
            document.getElementById("pass").focus();
        }
    }   
}
function showPass(){
    const icon = document.getElementById("showPass");
    const pass = document.getElementById("pass");
    const label = document.getElementById("labelpass");
    if(pass.type =="password"){
        pass.type = "text";
        icon.className = "fa-solid fa-circle-check";
        label.innerHTML = "Hide Password"
    }else{
        pass.type = "password";
        icon.className = "fa-regular fa-circle-check";
        label.innerHTML = "Show Password"
    }
}