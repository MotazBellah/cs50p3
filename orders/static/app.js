var menu = document.getElementById('menu')
var flash_area = document.getElementById('flashMessage')

// Hide the flash message after 4 sec
setTimeout(function() {
    flash_area.style.display = "none"
}, 4000);

// Hide the flash message if the user click on it
flash_area.addEventListener('click', () =>{
    flash_area.style.display = "none"
});

menu.addEventListener('click', (e) => {
    // Call the selectionLimit function and set the limit based on the topping
    selectionLimit(2, 'tw');
    selectionLimit(3, 'th');
    selectionLimit(2, 'two-item');
    selectionLimit(3, 'three-item');
    selectionLimit(5, 'special');

});

// Function to limit the number of topping selection
// If the user for example select topping 2, so he has only two options to select not MORE
// If the user select more than the limit, set the select value to be null and display a message
function selectionLimit(limit, id) {
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener("change", function() {
            if ($(this).val().length > limit) {
                $(this).val(null);
                alert('You can select upto ' + limit.toString() +' options only');
            }
        });
    }

}
