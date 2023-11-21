
    document.addEventListener("DOMContentLoaded", function () {
    const statusElements = document.querySelectorAll(".status");
  
    statusElements.forEach((status) => {
      status.addEventListener("click", function () {
        // Toggle status values
        switch (status.textContent.trim().toLowerCase()) {
          case "aceptada":
            status.textContent = "Rechazada";
            status.classList.remove("aceptada");
            status.classList.add("rechazada");
            break;
          case "rechazada":
            status.textContent = "Sin revisar";
            status.classList.remove("rechazada");
            status.classList.add("shipped");
            break;
          case "sin revisar":
            status.textContent = "Aceptada";
            status.classList.remove("shipped");
            status.classList.add("aceptada");
            break;
          // Add more cases if needed
        }
      });
    });
  });
