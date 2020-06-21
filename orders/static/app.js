var menu = document.getElementById('menu')
var total = 0;
var topping = [];
var items = '';
// alert('HH')

$('#flashMessage').click(function functionName() {
    $('#flashMessage').slideDown(1000).delay(3000).slideUp(1000);
})

menu.addEventListener('click', (e) => {
    // Call the selectionLimit function and set the limit based on the topping
    selectionLimit(2, 'tw');
    selectionLimit(3, 'th');
    selectionLimit(2, 'two-item');
    selectionLimit(3, 'three-item');
    selectionLimit(5, 'special');

    // If the input is hitted, use DOM traverse to get the price, food, typeID and toppings
    // and submit the form with AJAX
    // if (e.target.tagName === 'INPUT') {
    //     const form = e.target.parentNode.parentNode.id
    //     const price = e.target.value
    //     const food = e.target.parentNode.parentNode.childNodes[3].value
    //     const typeID = e.target.parentNode.parentNode.childNodes[3].id
    //     const select1 = e.target.parentNode.parentNode.childNodes[5]
    //     const check = true
    //     const id = "#" + form
    //
    //     console.log(e.target);
    //
    //
    //
    //     // If the user select topping, then
    //     // Create list with all selected options
    //     let selected1 = []
    //     if (select1) {
    //         for (let i = 0; i < select1.length; i++) {
    //         if (select1.options[i].selected) {
    //             selected1.push(select1.options[i].value);
    //         }
    //     }
    //
    //     }
    //
    //     console.log(form);
    //     console.log(price);
    //     console.log(food);
    //     console.log(typeID);
    //     console.log(selected1);
    //
    //     $(document).on('submit', id, function(event) {
    //         // preventDefault, do not allow to write the parameter on the url
    //         event.preventDefault();
    //         // Make sure the number of selected topping equal to the selected food
    //         // For ex. if the user select 2 toppings then the user has two options to select not LESS
    //         // If user select less than the selected topping, informe the user
    //         if (check) {
    //             if ((food=='2 toppings'||food=='2 items') && selected1.length < 2) {
    //                 alert("Please select 2 toppings")
    //                 check = false;
    //                 return
    //             }
    //             if ((food=='3 toppings'||food=='3 items') && selected1.length < 3) {
    //                 alert("Please select 3 toppings")
    //                 check = false;
    //                 return
    //             }
    //             if (food=='Special' && selected1.length < 4) {
    //                 alert("Please select 4 or 5 toppings")
    //                 check = false;
    //                 return
    //             }
    //             console.log(form);
    //             console.log(e.target.value);
    //             console.log(food);
    //             console.log(typeID);
    //             console.log(selected1);
    //             // Created AJAX request to send the info about the selected food to the server
    //             $.ajax({
    //                 type: 'post',
    //                 url: '/addFood',
    //                 data: {
    //                     food: food,
    //                     price: price,
    //                     topping1: selected1.toString(),
    //                     id: typeID,
    //                     csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    //                 },
    //                 success: function () {
    //                     alert('Added to your carts')
    //
    //                 }
    //
    //             });
    //             check = false;
    //
    //         }
    //
    //     });
    //
    // }

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
