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



