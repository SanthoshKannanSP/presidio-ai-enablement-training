# AI Comparison Sheet
| Model | Functional Completeness | Code Quality & Organization | UI/UX Implementation | Edge Case Handling | Comments |
|-------|------------------------|----------------------------|---------------------|-------------------|----------------------------------|
| ChatGPT | Excellent | Excellent | Good | Good | Amount validation didn't account for negative number. UI is simple |
| Claude Sonnet | Excellent | Excellent | Excellent | Excellent | All validation is accounted for and UI is amazing |
| Gemini Flash | Excellent | Good | Good | Good | Description validation didn't account for whitespace string. The validation messages are not informative. UI is simple. |
| Deepseek 7B | Okay | Excellent | Okay | Okay | Code was broken. No validation messages. UI was simple and inconsistent. |

## Prompt
Create a simple expense tracker web application with the following features:

Add new expenses with description, amount, and category
Display a list of all expenses
Show the total amount spent
Allow users to delete individual expenses
Include at least 3 expense categories (e.g., Food, Transport, Entertainment)

You can should use vanilla JavaScript. The application should work in a web browser