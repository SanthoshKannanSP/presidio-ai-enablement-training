## Prompt
Create a simple expense tracker web application following the coding standards provided below.
Application Requirements:

Add new expenses with description, amount, and category
Display a list of all expenses
Show the total amount spent
Allow users to delete individual expenses
Include at least 3 expense categories (e.g., Food, Transport, Entertainment)

You can use vanilla JavaScript, HTML, and CSS. The application should work in a web browser.
Coding Standards & Best Practices Guide:
1. Code Organization

Separate concerns: Keep HTML structure, CSS styling, and JavaScript logic in separate sections
Use meaningful file/section names that describe their purpose
Group related functions together with clear comments

2. Naming Conventions

Use camelCase for JavaScript variables and functions (e.g., addExpense, totalAmount)
Use kebab-case for CSS classes (e.g., expense-item, delete-btn)
Use descriptive names that indicate purpose (e.g., calculateTotal() instead of calc())
Constants should be in UPPER_SNAKE_CASE (e.g., MAX_DESCRIPTION_LENGTH)

3. JavaScript Best Practices

Use const for values that don't change, let for variables that do
Avoid using var
Use arrow functions for callbacks and short functions
Add event listeners properly (don't use inline onclick)
Use template literals for string concatenation
Validate all user inputs before processing

4. Error Handling & Validation

Validate that amount is a positive number
Validate that description is not empty
Validate that a category is selected
Show user-friendly error messages
Prevent form submission with invalid data

5. CSS Styling Guidelines

Use a consistent spacing system (e.g., multiples of 4px or 8px)
Ensure sufficient color contrast for readability
Make interactive elements clearly clickable (cursor: pointer)
Provide visual feedback on user actions (hover states, disabled states)
Use a simple, clean layout with proper spacing

6. Code Documentation

Add comments for complex logic or non-obvious code
Include a brief comment at the top explaining the application
Document function parameters and return values for key functions

7. User Experience

Show clear feedback when expenses are added or deleted
Display a message when the expense list is empty
Format currency values consistently (e.g., $10.00)
Make the delete action obvious but not accidental

Please implement the expense tracker following these standards

## Improvements with larger context input
- All validations were now implemented
- The UI was better looking and the UI design style was consistent
- The generated code was better formatted