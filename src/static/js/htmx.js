const modal = document.getElementById("modal");
const dialog = document.getElementById("dialog");

/* =========================================================
   CKEDITOR 5 INIT (HTMX SAFE)
========================================================= */
function initCKEditor5() {
    document.querySelectorAll(".django_ckeditor_5").forEach((el) => {

        if (el.dataset.ckeditorReady) return;

        el.dataset.ckeditorReady = "true";

        // Avoid duplicate module loading
        setTimeout(() => {
            document.dispatchEvent(new Event("DOMContentLoaded"));
        }, 0);
    });
}

/* =========================================================
   HTMX MODAL HANDLER
========================================================= */
htmx.on("htmx:afterSwap", (e) => {

    if (e.detail.target.id !== "dialog") return;

    //  IMPORTANT FIX: avoid reopening modal after submit empty response
    if (!e.detail.target.innerHTML.trim()) return;

    openModal();

    setTimeout(() => {
        initCKEditor5();
    }, 10);

    setupModalUI(e.detail.target);
});

/* =========================================================
   OPEN / CLOSE MODAL
========================================================= */
function openModal() {
    modal.classList.remove("hidden");
}

function closeModal() {
    modal.classList.add("hidden");
    dialog.innerHTML = "";
    resetCKEditorState();
}

/* =========================================================
   MODAL UI SETUP
========================================================= */
function setupModalUI(container) {

    const cancel = container.querySelector("#cancel");

    if (cancel && !cancel.dataset.bound) {
        cancel.dataset.bound = "true";
        cancel.addEventListener("click", closeModal);
    }

    const firstChildId = container.firstElementChild?.id;

    dialog.classList.remove("small", "medium", "large");

    if (firstChildId) {
        dialog.classList.add(firstChildId);
    }
}

/* =========================================================
   RESET CKEDITOR STATE
========================================================= */
function resetCKEditorState() {
    document.querySelectorAll(".django_ckeditor_5").forEach((el) => {
        el.dataset.ckeditorReady = "";
    });
}

/* =========================================================
   BACKDROP CLOSE
========================================================= */
modal.addEventListener("click", (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

/* =========================================================
   CLOSE MODAL AFTER FORM SUBMIT (HTMX EVENT)
========================================================= */
htmx.on("formSubmittedEvent", function () {
    closeModal();
});


/* Highlight code blocks after HTMX swaps */
document.body.addEventListener("htmx:afterSettle", function (e) {
    if (!window.Prism) return;

    const target = e.detail.target;

    // highlight uniquement dans le contenu injecté
    Prism.highlightAllUnder(target);
});