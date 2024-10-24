// document.getElementById('image').addEventListener('change', previewMeme);
// document.getElementById('text').addEventListener('input', previewMeme);

// function previewMeme() {
//     const file = document.getElementById('image').files[0];
//     const text = document.getElementById('text').value;
//     const preview = document.getElementById('preview');

//     if (file) {
//         const reader = new FileReader();
//         reader.onload = function(e) {
//             preview.src = e.target.result;
//             // Ajouter du texte sur l'image (nécessite une implémentation supplémentaire)
//         }
//         reader.readAsDataURL(file);
//     }
// }

document.getElementById('image').addEventListener('change', function(event) {
    const preview = document.getElementById('image-preview');
    preview.innerHTML = '';
    const file = event.target.files[0];

    if (file && file.type.startsWith('image/')) {
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);

        // Option 1 : Fixer les dimensions exactes (peut déformer l'image)
        img.style.width = '140px';
        img.style.height = '170px';

        // Option 2 : Adapter l'image au conteneur en conservant les proportions
        // img.style.maxWidth = '100%';
        // img.style.maxHeight = '100%';

        preview.appendChild(img);
    } else {
        preview.innerHTML = '<p style="color: red;">Veuillez sélectionner un fichier image valide.</p>';
    }
});
