-- ============================================================================
-- RETAIL ANALYTICS DATABASE SCHEMA
-- ============================================================================

-- Drop existing tables if they exist (for cleanup)
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- ============================================================================
-- CUSTOMERS TABLE
-- ============================================================================
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_purchases DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_country (country),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- PRODUCTS TABLE
-- ============================================================================
CREATE TABLE products (
    stock_code VARCHAR(20) PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    current_price DECIMAL(10, 2),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_active (active),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TRANSACTIONS TABLE (Main Fact Table)
-- ============================================================================
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_no VARCHAR(20) NOT NULL,
    customer_id VARCHAR(10),
    stock_code VARCHAR(20),
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    invoice_date TIMESTAMP NOT NULL,
    revenue DECIMAL(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    transaction_status VARCHAR(20) DEFAULT 'COMPLETED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (stock_code) REFERENCES products(stock_code),
    
    INDEX idx_invoice_date (invoice_date),
    INDEX idx_customer_id (customer_id),
    INDEX idx_stock_code (stock_code),
    INDEX idx_invoice_no (invoice_no),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================
-- (Indexes already created above)

-- ============================================================================
-- VERIFY TABLES CREATED
-- ============================================================================
-- Run this to verify:
-- SHOW TABLES;
-- DESCRIBE customers;
-- DESCRIBE products;
-- DESCRIBE transactions;