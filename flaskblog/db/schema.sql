DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    -- id INTEGER NOT NULL, 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) UNIQUE NOT NULL, 
    email VARCHAR(120) UNIQUE NOT NULL, 
    password VARCHAR(60) NOT NULL, 
    image_file VARCHAR(20) NOT NULL, 
    PRIMARY KEY (id), 
    -- UNIQUE (username), 
    -- UNIQUE (email)
);

CREATE TABLE post (
    -- id INTEGER NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    -- body TEXT NOT NULL,
    content TEXT NOT NULL,
    -- created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    -- PRIMARY KEY (id),
    -- FOREIGN KEY (author_id) REFERENCES user (id)
    FOREIGN KEY(user_id) REFERENCES user (id)
);
