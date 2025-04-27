let list = document.querySelectorAll('.navigation li');

function activeLink(){
    list.forEach((item) => item.classList.remove('hovered'));
    this.classList.add('hovered');
}

list.forEach((item) => item.addEventListener('mouseover', activeLink));

let toggle = document.querySelector('.toggle');
let navigation = document.querySelector('.navigation');
let main = document.querySelector('.main');


toggle.onclick = function(){
    navigation.classList.toggle('active');
    main.classList.toggle('active');
}


document.addEventListener("DOMContentLoaded", function() {
    const parametresBtn = document.querySelector(".parametres");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    parametresBtn.addEventListener("click", function() {
        parametresBtn.classList.toggle("active");
    });

    // Ferme le menu si on clique ailleurs
    document.addEventListener("click", function(event) {
        if (!parametresBtn.contains(event.target)) {
            parametresBtn.classList.remove("active");
        }
    });
});
