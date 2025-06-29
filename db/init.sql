-- This is a placeholder file for Phase 3: Database Design & Seeding.
-- When the database container starts for the first time, it will execute
-- the SQL commands in this file.
-- We will add table creation and data insertion scripts here later. 

-- =================================================================
--  Create the 'users' table
-- =================================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    age_bracket VARCHAR(20),
    location VARCHAR(50),
    employment_status VARCHAR(30),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =================================================================
--  Create the 'transactions' table
-- =================================================================
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- =================================================================
--  (Mock data will be inserted below in the next step)
-- ================================================================= 

-- =================================================================
--  Insert Mock Data for 'users'
-- =================================================================
INSERT INTO users (id, username, password, full_name, age_bracket, location, employment_status) VALUES
(1, 'john.doe@example.com', 'password123', 'John Doe', '25-34', 'New York', 'Employed'),
(2, 'jane.doe@example.com', 'password123', 'Jane Doe', '18-24', 'London', 'Student'),
(3, 'charlie@example.com', 'password123', 'Charlie Williams', '35-44', 'New York', 'Self-Employed');

-- =================================================================
--  Insert Mock Data for 'transactions' for John Doe (User ID: 1)
-- =================================================================
-- Practical Spender: Groceries, Utilities, Transport
INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES
(1, 75.50, 'Groceries', 'Weekly grocery run', '2025-06-20'),
(1, 50.00, 'Utilities', 'Electricity bill', '2025-06-15'),
(1, 25.00, 'Transport', 'Metro card top-up', '2025-06-10'),
(1, 80.25, 'Groceries', 'Stocking up pantry', '2025-06-05'),
(1, 120.00, 'Utilities', 'Internet bill', '2025-06-01'),
(1, 65.40, 'Groceries', 'Farmers market haul', '2025-05-25'),
(1, 30.00, 'Transport', 'Ride-share to airport', '2025-05-22'),
(1, 52.30, 'Utilities', 'Water bill', '2025-05-15'),
(1, 70.00, 'Groceries', 'Groceries for the week', '2025-05-10'),
(1, 25.00, 'Transport', 'Bus pass', '2025-05-05'),
(1, 45.10, 'Utilities', 'Gas bill', '2025-05-01'),
(1, 90.80, 'Groceries', 'Bulk buy at Costco', '2025-04-28'),
(1, 68.00, 'Groceries', 'Weekly groceries', '2025-04-21'),
(1, 25.00, 'Transport', 'Subway monthly pass', '2025-04-05'),
(1, 115.00, 'Utilities', 'Combined utilities', '2025-04-01');

-- =================================================================
--  Insert Mock Data for 'transactions' for Jane Doe (User ID: 2)
-- =================================================================
-- Social Spender: Dining, Entertainment, Transport
INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES
(2, 45.00, 'Dining', 'Dinner with friends', '2025-06-22'),
(2, 30.00, 'Entertainment', 'Movie tickets', '2025-06-18'),
(2, 15.50, 'Transport', 'Ride-share home', '2025-06-18'),
(2, 60.75, 'Dining', 'Brunch spot', '2025-06-12'),
(2, 22.00, 'Entertainment', 'Concert ticket fee', '2025-06-08'),
(2, 55.00, 'Dining', 'Takeout pizza', '2025-06-02'),
(2, 75.00, 'Entertainment', 'Video game purchase', '2025-05-28'),
(2, 35.20, 'Dining', 'Lunch meeting', '2025-05-20'),
(2, 18.00, 'Transport', 'Train ticket', '2025-05-16'),
(2, 50.00, 'Dining', 'Date night dinner', '2025-05-11'),
(2, 40.00, 'Entertainment', 'Bowling with team', '2025-05-06'),
(2, 25.80, 'Dining', 'Coffee and pastries', '2025-05-02'),
(2, 150.00, 'Entertainment', 'Music festival ticket', '2025-04-25'),
(2, 80.50, 'Dining', 'Birthday dinner celebration', '2025-04-15'),
(2, 20.00, 'Transport', 'City bike rental', '2025-04-10');

-- =================================================================
--  Insert Mock Data for 'transactions' for Charlie (User ID: 3)
-- =================================================================
-- Lifestyle Spender: Shopping, Travel, Health
INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES
(3, 150.00, 'Shopping', 'New sneakers', '2025-06-25'),
(3, 450.00, 'Travel', 'Flight to Miami', '2025-06-20'),
(3, 75.00, 'Health', 'Yoga class pack', '2025-06-15'),
(3, 85.50, 'Shopping', 'Designer shirt', '2025-06-10'),
(3, 200.00, 'Travel', 'Hotel booking', '2025-06-05'),
(3, 60.00, 'Health', 'Gym membership', '2025-06-01'),
(3, 120.75, 'Shopping', 'Skincare products', '2025-05-28'),
(3, 300.00, 'Travel', 'Weekend getaway', '2025-05-20'),
(3, 50.00, 'Health', 'Nutritionist consultation', '2025-05-15'),
(3, 250.00, 'Shopping', 'New headphones', '2025-05-10'),
(3, 800.00, 'Travel', 'International flight deposit', '2025-05-02'),
(3, 90.00, 'Health', 'Annual check-up', '2025-04-28'),
(3, 180.00, 'Shopping', 'Watch repair', '2025-04-20'),
(3, 95.20, 'Health', 'Massage therapy', '2025-04-12'),
(3, 400.00, 'Travel', 'Rental car for trip', '2025-04-05'); 