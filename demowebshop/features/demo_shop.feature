Feature: Test Cases for Demo Web Shop
    As a user of the demo web shop
    I want to test various functionalities
    So that I can ensure the website works as expected

    Scenario: User Registration with Edge Validation
        Given I am on the Register page
        When I enter an invalid email format
        And I enter mismatched passwords
        And I submit the form
        Then I should see error messages for invalid email and password mismatch

    Scenario: Add Out-of-Stock Item to Cart
        Given I navigate to an out-of-stock product
        When I attempt to add it to the cart
        Then I should see an error or the add to cart button should be disabled

    Scenario: Checkout Without Login
        Given I have added a product to the cart
        When I go to the checkout page without logging in
        Then I should be prompted to log in or register

    Scenario: Search Function – Case and Symbol Sensitivity
        Given I enter "COMPutEr!!!" in the search bar
        When I perform the search
        Then I should see relevant results for "computer"

    Scenario: Cart Persistence After Logout/Login
        Given I am logged in and have added items to the cart
        When I log out and log back in
        Then My cart should retain the previously added items

    Scenario: Newsletter Subscription – Duplicate Email
        Given I enter an email in the newsletter subscription box
        When I submit the same email again
        Then I should receive a message indicating duplicate subscription

    Scenario: Rapid Add-to-Cart Clicks
        Given I am on a product page
        When I click the "Add to Cart" button rapidly multiple times
        Then The cart should handle the requests properly without duplication 