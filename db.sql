CREATE TABLE Users
(
    username VARCHAR(30) PRIMARY KEY,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE Submissions
(
    username VARCHAR(30),
    submissionId CHAR(23),
    status CHAR(11) NOT NULL,
    stdout TEXT,
    stderr TEXT,
    PRIMARY KEY(username, submissionId),
    FOREIGN KEY(username) REFERENCES Users(username)
);

INSERT INTO Users(username, password) VALUES ('admin', 'top_secret_password');
