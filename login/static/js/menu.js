const btn_menu = document.querySelector(".btn-menu"),
      menu_options = document.querySelector(".menu-options"),
      conocenosBoton = document.querySelector(".conocenos"),
      conocenos = document.getElementById("main");

btn_menu.onclick = () => {
    menu_options.classList.toggle("active");
}

conocenosBoton.onclick = () => {
    conocenos.scrollIntoView();
}
