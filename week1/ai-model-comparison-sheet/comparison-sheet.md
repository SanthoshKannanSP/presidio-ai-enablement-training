# AI Comparison Sheet
| Model | Code | SQL | Infra | Ease of Use | Speed/Latency |
|-------|------------------------|----------------------------|---------------------|-------------------|----------------------------------|
| ChatGPT | Good | Excellent | Okay | Excellent | Excellent |
| Claude Sonnet | Excellent | Excellent | Excellent | Excellent | Good |
| Gemini Flash | Good | Good | Good | Excellent | Excellent |
| Deepseek 7B | Basic | Good | Good | Good | Excellent |

## Code Prompt
Create a simple expense tracker web application with the following features:

Add new expenses with description, amount, and category
Display a list of all expenses
Show the total amount spent
Allow users to delete individual expenses
Include at least 3 expense categories (e.g., Food, Transport, Entertainment)

You can should use vanilla JavaScript. The application should work in a web browser

### Comments

Claude Sonnet had the best output of all the models. It had followed a specific UI styling (Neo-Brutalism) and all validations were done.

Both the Gemini Flash and ChatGPT models didn't account for few validations. Further, the UI was simple and generic looking.

The code given by DeepSeek was broken. There were no validation messages for any input fields. The UI was simple and had inconsistent styling.

## SQL Prompt
You have an e-commerce database with the following schema:
```sql
customers (customer_id, name, email, registration_date, country)
orders (order_id, customer_id, order_date, total_amount, status)
order_items (item_id, order_id, product_id, quantity, unit_price)
products (product_id, name, category, supplier_id, cost_price)
suppliers (supplier_id, name, country)
```
Write a SQL query to:
Find the top 5 product categories by profit margin in Q1 2024, but only include categories where:

- At least 3 different suppliers provide products in that category
- The category has had orders from customers in at least 10 different countries
- The total quantity sold exceeds 100 units

For each qualifying category, return:

- Category name
- Total revenue (sum of unit_price × quantity)
- Total cost (sum of cost_price × quantity)
- Profit margin percentage
- Number of unique suppliers
- Number of unique customer countries
- Total units sold

Order results by profit margin (highest first).

### Comments
Claude Sonnet used a CTE approach whereas other models used just a SELECT Query.

Gemini Flash and DeepSeek didn't account for the status of the order for filtering the data whereas the other models did.

## Infra script Prompt
Write a Bash script that monitors a web application and performs basic recovery.
Services to Monitor:
* Nginx web server (port 80)
* PostgreSQL database (port 5432)
* Application API (port 3000)
Requirements:
1. Health Checks - Check every 60 seconds:
   * Is the service process running?
   * Is the port accepting connections?
   * For PostgreSQL: Are active connections below 50?
2. Auto-Recovery:
   * If a service is down, restart it using systemctl
   * If restart fails, wait 10 seconds and try once more
   * If database connections exceed 50, log a warning (no action needed)
3. Logging:
   * Write all events to `/var/log/monitor.log` with timestamps
   * Log format: `[TIMESTAMP] [SERVICE] [STATUS] message`
   * If any service fails both restart attempts, print error to console
4. Basic Features:
   * Run continuously until stopped (Ctrl+C)
   * Accept a `--dry-run` flag that checks but doesn't restart services
   * Clean exit on Ctrl+C

### Comments
Claude's script had the best error handling and was more extensive in terms of logging.

ChatGPT's script had the least error handling.

## Ease of Use and Latency Comments
Claude was generating several documentations for the tasks. Although these documentations are really useful, for simple tasks, this much extensive documentation is not required. Also the time it took to generate these documentations for simple tasks was significant, where a simple paragraph with the usage instructions would have sufficed.

The output formatting of Deepseek was broken most of the time.