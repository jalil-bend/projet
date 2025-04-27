// document.addEventListener("DOMContentLoaded", function () {
//     const generateBtn = document.getElementById("generateBtn");
//     const emailInput = document.getElementById("email");
//     const generateForm = document.getElementById("generateForm");

//     if (generateBtn && generateForm) {
//         generateBtn.addEventListener("click", function (event) {
//             event.preventDefault(); // 🔹 Empêche le rechargement immédiat

//             if (emailInput.value.trim() === "") {
//                 showNotification("error", "L'email est obligatoire.");
//                 return;
//             }

//             // generateBtn.disabled = true;
//             // generateBtn.innerHTML = "<i class='fas fa-spinner fa-spin'></i> Génération...";

//             // // 🔹 Stocker temporairement l'email pour affichage correct
//             // sessionStorage.setItem("generatedEmail", emailInput.value);

//             // setTimeout(() => {
//             //     generateForm.submit();
//             // }, 500);
//         });
//     }

//     // 🔹 Vérifier si une génération précédente a eu lieu et restaurer les données
//     // if (sessionStorage.getItem("generatedEmail")) {
//     //     emailInput.value = sessionStorage.getItem("generatedEmail");
//     //     sessionStorage.removeItem("generatedEmail");
//     // }
// });

/* 🔹 Fonction pour afficher une notification */
function showNotification(type, message) {
    const notificationContainer = document.querySelector(".notification-container");
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas ${type === "success" ? "fa-check-circle" : "fa-exclamation-triangle"}"></i>
        <span>${message}</span>
        <button class="close-btn">&times;</button>
    `;

    notificationContainer.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = "slideOut 0.5s ease forwards";
        setTimeout(() => notification.remove(), 500);
    }, 3000);

    notification.querySelector(".close-btn").addEventListener("click", () => {
        notification.style.animation = "slideOut 0.5s ease forwards";
        setTimeout(() => notification.remove(), 500);
    });
}

/* 🔹 Copier les identifiants */
function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(text).then(() => {
        showNotification("success", "Copié !");
    });
}
