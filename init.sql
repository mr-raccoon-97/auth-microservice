CREATE TABLE users (
    pk SERIAL PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL,
    user_username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE accounts (
    pk SERIAL PRIMARY KEY,
    account_id VARCHAR(255) NOT NULL,
    account_type VARCHAR(100) NOT NULL,
    account_provider VARCHAR(100) NOT NULL,
    user_pk INT,
    FOREIGN KEY (user_pk) REFERENCES users(pk) ON DELETE CASCADE, 
    CONSTRAINT unique_account UNIQUE (account_provider, account_id)
);