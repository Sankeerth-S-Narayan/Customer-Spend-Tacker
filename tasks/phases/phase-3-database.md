# 🗄️ Phase 3: Database Design & Seeding - Detailed Tasks

This document outlines the steps to define our database schema and populate it with realistic mock data.

---

### Task 3.1: Design and Implement the Database Schema
- [x] **Define `users` Table:** Write the SQL `CREATE TABLE` statement for the `users` table, including the `id`, `username`, `password`, `full_name`, `age_bracket`, `location`, `employment_status`, and `created_at` columns.
- [x] **Define `transactions` Table:** Write the SQL `CREATE TABLE` statement for the `transactions` table, including `id`, `user_id`, `amount`, `category`, `description`, `transaction_date`, and `created_at`. Ensure the `user_id` is a foreign key linked to the `users` table.
- [x] **Update `db/init.sql`:** Replace the placeholder content in `db/init.sql` with the new `CREATE TABLE` statements.
> **Summary:** The database schema has been designed and implemented. The `db/init.sql` file was updated with `CREATE TABLE` statements for a `users` table with rich demographic attributes for analytics, and a `transactions` table with detailed columns for spending analysis. A foreign key constraint was established between the tables to ensure data integrity. This completes the structural definition of our database.

---

### Task 3.2: Generate and Insert Mock Data
- [x] **Create User Data:** Write `INSERT` statements to create three distinct users (Alice, Bob, Charlie) with different profiles as discussed.
- [x] **Create Transaction Data:** For each user, write approximately 20-30 `INSERT` statements for transactions. The data should be spread across the last 3-4 months and reflect each user's spending profile (e.g., Alice buys groceries, Bob dines out).
- [x] **Add to `db/init.sql`:** Append all the `INSERT` statements to the `db/init.sql` file after the `CREATE TABLE` statements.
> **Summary:** The `db/init.sql` file was populated with a comprehensive set of mock data. This includes `INSERT` statements for three users with different demographic profiles and a corresponding set of 45 transactions spread across various categories and dates. This rich dataset will be crucial for developing and testing the analytics features.

---

### Task 3.3: Test Database Initialization
- [x] **Rebuild the Database:** Run `docker-compose down -v` to remove the old database container and volume, followed by `docker-compose up --build -d db`. We will only start the `db` service in a detached (`-d`) mode for this test.
- [x] **Verify Table Creation:** Connect to the database and run a command to list the tables to ensure `users` and `transactions` were created.
- [x] **Verify Data Insertion:** Run `SELECT` queries on both tables to confirm that the mock data has been populated correctly.
> **Summary:** The database initialization process was successfully tested. The database container was rebuilt to run the new `init.sql` script. Using `docker exec`, we connected to the running container and verified that both the `users` and `transactions` tables were created correctly. A `SELECT` query confirmed that all mock data was inserted as expected, validating the entire database setup. 