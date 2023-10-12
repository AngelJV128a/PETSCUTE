const imgDiv = document.querySelector('.profile-pic-div');
const img = document.querySelector('#photo');
const file = document.querySelector ('#file');
const uploadBtn = document.querySelector('#uploadBtn');

imgDiv.addEventListener('mouseenter',function(){   //se activa al pasar el cursor, cambia y muestra block
    uploadBtn.style.display = "block";
});

imgDiv.addEventListener('mouseleave', function(){  //se activa al pasar el cursor del raton, entra en el. 
    uploadBtn.style.display = "none";              //Cuando sucede se muestra el elemento upload y cambia su estilo para que no se muestra none
});

file.addEventListener('change',function(){         //añade un elemento file que se activa cuando se selecciona un archivo en el input
    const choosedFile = this.files[0];              //se obtiene el archivo 

    if(choosedFile){
        const reader = new FileReader();            //se crea un objeto llamado reader, para leer el contenido del archivo 
        reader.addEventListener('load', function(){     //se activa cuando la lectura del archivo fue completada 
            img.setAttribute('src', reader.result);     //cuando se carga el archivo se actualiza la fuente 'src' de la imagen img 
        });

        reader.readAsDataURL(choosedFile);
    }
});