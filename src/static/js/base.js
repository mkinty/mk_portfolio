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
    const close = container.querySelector("#close-btn");

    if (cancel && !cancel.dataset.bound) {
        cancel.dataset.bound = "true";
        cancel.addEventListener("click", closeModal);
    }

    if (close && !close.dataset.bound) {
        close.dataset.bound = "true";
        close.addEventListener("click", closeModal);
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
//        closeModal();
      console.log("Backdrop clicked");
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


// Fermer les alerts quand on clique sur la croix
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('icon')) {
        const alert = e.target.closest('.alert');
        if (alert) {
            alert.remove();
        }
    }
});

// Navigation toggle
$('.nav-title').on('click', function() {
  const nav = $(this).closest('.nav');
  const menu = nav.find('.nav-menu');
  nav.toggleClass('active');
  menu.toggleClass('active');
  $(this).toggleClass('active')
  console.log('clicked');
});

//$('.sheet .dropdown.item')
//  .dropdown({
//    on: 'hover'
//  })
//;
//$('.menu .item')
//  .tab()
//;
//$('.ui.checkbox')
//  .checkbox()
//;

/* ----------------------------------
// to close a valide or error message
$('.ui.message .close')
  .on('click', function() {
    $(this)
      .closest('.message')
      .transition('fade')
    ;
  });
----------------------------------*/



