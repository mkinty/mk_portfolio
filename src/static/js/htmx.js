const modal = document.getElementById("modal");
const dialog = document.getElementById("dialog");

// Quand HTMX injecte du contenu dans le modal
htmx.on("htmx:afterSwap", (e) => {
    if (e.detail.target.id === "dialog") {
        modal.classList.remove("hidden");

        // Gestion du bouton Annuler
        const cancel = e.detail.target.querySelector('#cancel');
        cancel.addEventListener('click', () => {
            modal.classList.add("hidden");
            dialog.innerHTML = "";
            console.log("Modal hidden");
        });

        // Gestion du modal
        const firstChildId = e.detail.target.firstElementChild?.id;
        dialog.classList.remove("small", "medium", "large");
        if (firstChildId) dialog.classList.add(firstChildId);

        // Initialiser Quill sur les champs présents
        const container = e.detail.target.querySelector('#quill-container');
        const textarea = e.detail.target.querySelector('textarea[name="quill-description"]');
        if (container && textarea && !container._quillInstance) {
            const quill = new Quill(container, {
                theme: 'snow',
                modules: {
                    syntax: true,
                    toolbar: [
                        [{ 'header': [1,2,3,false] }],
                        ['bold','italic','underline','strike'],
                        ['link','image','code-block'],
                        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                        [{ 'align': [] }],
                        ['clean']
                    ]
                }
            });
            quill.root.innerHTML = textarea.value;
            textarea.form.addEventListener('submit', () => {
                textarea.value = quill.root.innerHTML;
            });
            container._quillInstance = quill;
        }

    }
});

// Fermer le modal si on clique en dehors du dialogue
modal.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.classList.add("hidden");
        dialog.innerHTML = "";
    }
});