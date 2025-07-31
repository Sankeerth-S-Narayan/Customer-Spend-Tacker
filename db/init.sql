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

-- =================================================================
--  Additional Mock Data with Higher Spending and New Categories
-- =================================================================

-- Additional transactions for John Doe (User ID: 1) - Adding Technology and Education categories
INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES
(1, 1299.99, 'Technology', 'New MacBook Pro', '2025-06-28'),
(1, 199.99, 'Education', 'Online Python course', '2025-06-25'),
(1, 899.00, 'Technology', 'iPhone 15 Pro', '2025-06-22'),
(1, 125.00, 'Groceries', 'Premium organic groceries', '2025-06-18'),
(1, 89.99, 'Technology', 'Wireless earbuds', '2025-06-12'),
(1, 299.00, 'Education', 'Data Science certification', '2025-06-08'),
(1, 150.00, 'Utilities', 'High-speed internet upgrade', '2025-06-03'),
(1, 2499.99, 'Technology', 'Gaming desktop setup', '2025-05-30'),
(1, 75.50, 'Transport', 'Premium car service', '2025-05-26'),
(1, 450.00, 'Education', 'AWS certification prep', '2025-05-20'),
(1, 180.00, 'Groceries', 'Gourmet food shopping', '2025-05-15'),
(1, 599.00, 'Technology', '4K Monitor', '2025-05-08'),
(1, 200.00, 'Utilities', 'Smart home devices', '2025-05-02'),
(1, 350.00, 'Education', 'Machine learning workshop', '2025-04-25'),
(1, 95.00, 'Transport', 'Premium ride to conference', '2025-04-18');

-- Additional transactions for Jane Doe (User ID: 2) - Adding Technology and Education categories
INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES
(2, 799.00, 'Technology', 'iPad Pro with accessories', '2025-06-30'),
(2, 159.99, 'Education', 'Graphic design course', '2025-06-26'),
(2, 220.00, 'Dining', 'Fine dining experience', '2025-06-23'),
(2, 1299.99, 'Technology', 'MacBook Air for studies', '2025-06-19'),
(2, 89.99, 'Entertainment', 'Premium streaming subscriptions', '2025-06-16'),
(2, 299.00, 'Education', 'Photography masterclass', '2025-06-11'),
(2, 450.00, 'Technology', 'Professional camera lens', '2025-06-07'),
(2, 180.00, 'Dining', 'Michelin star restaurant', '2025-06-04'),
(2, 125.99, 'Entertainment', 'VIP concert tickets', '2025-05-29'),
(2, 199.99, 'Education', 'Language learning app premium', '2025-05-24'),
(2, 899.00, 'Technology', 'High-end smartphone', '2025-05-18'),
(2, 95.50, 'Transport', 'Luxury airport transfer', '2025-05-14'),
(2, 349.00, 'Entertainment', 'Theater season tickets', '2025-05-09'),
(2, 250.00, 'Education', 'Creative writing workshop', '2025-05-03'),
(2, 75.00, 'Dining', 'Wine tasting event', '2025-04-28');

-- Additional transactions for Charlie (User ID: 3) - Adding Technology and Education categories
INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES
(3, 3499.99, 'Technology', 'High-end gaming laptop', '2025-06-29'),
(3, 599.00, 'Education', 'Business leadership program', '2025-06-24'),
(3, 1250.00, 'Shopping', 'Designer suit collection', '2025-06-21'),
(3, 899.99, 'Technology', 'Professional drone', '2025-06-17'),
(3, 1200.00, 'Travel', 'Luxury hotel suite', '2025-06-13'),
(3, 450.00, 'Education', 'Investment strategy course', '2025-06-09'),
(3, 2200.00, 'Technology', 'Home theater system', '2025-06-06'),
(3, 180.00, 'Health', 'Premium spa treatment', '2025-06-02'),
(3, 750.00, 'Shopping', 'Luxury watch', '2025-05-27'),
(3, 399.99, 'Education', 'Real estate investment course', '2025-05-22'),
(3, 1500.00, 'Travel', 'First-class flight upgrade', '2025-05-17'),
(3, 999.00, 'Technology', 'Smart home automation', '2025-05-12'),
(3, 275.00, 'Health', 'Personal trainer sessions', '2025-05-07'),
(3, 850.00, 'Shopping', 'Premium luggage set', '2025-05-01'),
(3, 650.00, 'Education', 'Executive MBA module', '2025-04-26'),
(3, 320.00, 'Health', 'Advanced health screening', '2025-04-19'),
(3, 1899.99, 'Technology', 'Professional camera equipment', '2025-04-14'),
(3, 2500.00, 'Travel', 'Luxury cruise booking', '2025-04-08');

-- =================================================================
--  Extra diverse transactions across all users for richer analytics
-- =================================================================

-- More varied spending patterns for John Doe (practical but upgrading lifestyle)
INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES
(1, 45.99, 'Technology', 'Software subscription', '2025-07-01'),
(1, 299.99, 'Education', 'Professional certification', '2025-07-03'),
(1, 150.00, 'Groceries', 'Weekly premium groceries', '2025-07-05'),
(1, 85.00, 'Transport', 'Monthly transit premium', '2025-07-07'),
(1, 199.99, 'Technology', 'Smart fitness tracker', '2025-07-10');

-- More entertainment and tech for Jane Doe (student upgrading gear)
INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES
(2, 49.99, 'Technology', 'Cloud storage upgrade', '2025-07-02'),
(2, 125.00, 'Education', 'Online certification course', '2025-07-04'),
(2, 89.99, 'Entertainment', 'Gaming subscription bundle', '2025-07-06'),
(2, 250.00, 'Dining', 'Graduation celebration dinner', '2025-07-08'),
(2, 399.99, 'Technology', 'Tablet for digital art', '2025-07-11');

-- More luxury and business expenses for Charlie (high earner)
INSERT INTO transactions (user_id, amount, category, description, transaction_date) VALUES
(3, 299.99, 'Technology', 'Premium business software', '2025-07-01'),
(3, 1500.00, 'Education', 'Executive coaching session', '2025-07-03'),
(3, 450.00, 'Health', 'Concierge medical service', '2025-07-05'),
(3, 2200.00, 'Shopping', 'Custom tailored wardrobe', '2025-07-07'),
(3, 3500.00, 'Travel', 'Private jet charter', '2025-07-09'),
(3, 899.99, 'Technology', 'Latest smartphone pro max', '2025-07-12'); 