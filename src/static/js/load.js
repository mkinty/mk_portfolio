  // Navigation toggle
$('.nav-title').on('click', function() {
  const nav = $(this).closest('.nav');
  const menu = nav.find('.nav-menu');
  nav.toggleClass('active');
  menu.toggleClass('active');
  $(this).toggleClass('active')
  console.log('clicked');
});

// Aside menu toggle
$('.aside-menu-icon').on('click', function() {
  $('.project-detail-aside').toggleClass('active');
  $('.project-detail-main').toggleClass('active');
  console.log('clicked');
});
