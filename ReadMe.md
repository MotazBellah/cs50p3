# Pizza
an web application for handling a pizza restaurant’s online orders. Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed.

- https://online-pizza-order.herokuapp.com/
- The menu model comes from Pinocchio's Pizza & Subs located in Cambridge, MA.
- This is project 3 for CS50 Web Development with Python and JavaScript from Harvard University

## Code
- This project is written in python 3 and Django 3 framework.
- Use Bootstrap, CSS and JS in front-end

## Application Features
- Menu: The web application support all of the available menu items for Pinnochio’s Pizza & Subs (a popular pizza place in Cambridge).
- Adding Items: Using Django Admin, site administrators (restaurant owners) will be able to add, update, and remove items on the menu. Added all of the items from the Pinnochio’s menu into the database using the Admin UI.
- Registration, Login, Logout: Site users (customers) will be able to register for your web application with a username, password, and email address. Customers should then be able to log in and log out of your website and using the Facebook authentication users can use their account to login.
- Shopping Cart: Once logged in, users will see a representation of the restaurant’s menu, where they can add items (along with toppings or extras, if appropriate) to their “shopping cart.” The contents of the shopping will be saved even if a user closes the window, or logs out and logs back in again.
- Placing an Order: Once there is at least one item in a user’s shopping cart, they can place an order, whereby the user is asked to confirm the items in the shopping cart, and the total and integrating with the Stripe API to allow users to actually use a credit card to make a purchase during checkout.
- Email: Application will send an email after a successful payment with list of items and the total price

## Test Stripe integration

| NUMBER                | DESCRIPTION                                               |
| --------------------- |:---------------------------------------------------------:|
| 4242 4242 4242 4242   | Succeeds and immediately processes the payment.           |
| 4000 0000 0000 9995   | Always fails with a decline code of `insufficient_funds`. |

- For more information, please visit  https://stripe.com/docs/testing
