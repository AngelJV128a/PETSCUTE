const btn_menu = document.querySelector(".btn-menu"),
      menu_options = document.querySelector(".menu-options");

btn_menu.onclick = () => {
    menu_options.classList.toggle("active");
}

function irAAncla(seccion1) {
  var ancla = document.getElementsByName(seccion1)[0];
  if (ancla) {
    window.scrollTo({
      top: ancla.offsetTop,
      behavior: 'smooth' // Para una animación de desplazamiento suave (opcional)
    });
  }
}

