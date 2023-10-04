//MODO OSCURO DEL INICIO
const swith = document.querySelector(".switch");

swith.addEventListener("click", e=>{  /*Accedemos a la variable swith en la lista de clase cada que demos click se agregara o quitara la clase*/ 
   swith.classList.toggle("active");
   document.body.classList.toggle("active");
})

