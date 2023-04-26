/**
 * Nothing here yet. Add some stuff?
 */
// let navBtns = document.querySelectorAll('.nav-btn');

// Add an event handler for all nav-btns to enable the dropdown functionality
// navBtns.forEach(function (ele) {
//     ele.addEventListener('click', function() {
//         // Get the dropdown-menu associated with this nav button (insert the id of your menu)
//         let dropDownMenu = document.getElementById('MENU_ID_HERE');
//
//         // Toggle the nav-btn and the dropdown menu
//         ele.classList.toggle('active');
//         dropDownMenu.classList.toggle('active');
//     });
// });

$('.has-sub').on('click', function(e) { // Get all dropdown menu toggles
    $('.dropdown-menu').not($(this).children('.dropdown-menu')).removeClass('dropdown-shown'); // Hide all other dropdown menus
    $('.has-sub').not($(this)).removeClass('active'); // Remove the active selector from the other dropdown toggles
    $(this).children('.dropdown-menu').toggleClass('dropdown-shown'); // Show/hide the dropdown menu associated with the toggle being clicked
    $(this).toggleClass('active'); // Toggle the active selector on the nav-item
});

// Show dropdown when clicked
$('#header-btn').on('click', function(e) {
    $('#MENU_ID_HERE').toggleClass('active');
    $('.nav-btn').toggleClass('active');
});

// Hide menu after clicking menu item
$('.dropdown-menu li').on('click', function(e) {
     $('#MENU_ID_HERE').removeClass('active');
     $('.nav-btn').removeClass('active');
});

// $('.tab-container ul').on('click', function(e) {
//      // $('#tet').toggleClass('selected');
//      $('li').toggleClass('selected');
// });

$(function() {
    $( "#tab-1" ).tabs({
        heightStyle:"fill",
        collapsible:true,
        hide:"slideUp"
    });
});

