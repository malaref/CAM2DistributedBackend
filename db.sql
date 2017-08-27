CREATE TABLE Users
(
    username VARCHAR(30) PRIMARY KEY,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE Submissions
(
    username VARCHAR(30),
    application_id CHAR(23),
    log TEXT,
    PRIMARY KEY(username, application_id),
    FOREIGN KEY(username) REFERENCES Users(username)
);

INSERT INTO Users(username, password) VALUES ('admin', 'top_secret_password');
