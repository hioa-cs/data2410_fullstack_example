CREATE DATABASE all_the_things;
USE all_the_things;

CREATE TABLE lonely_heroes (
    id             INT unsigned NOT NULL AUTO_INCREMENT, 
    name           VARCHAR(150) NOT NULL,
    has_ponycopter BOOLEAN NOT NULL default FALSE,
    PRIMARY KEY     (id)
);
 
# Not needed but nice for debug output
DESCRIBE lonely_heroes;

INSERT INTO lonely_heroes (name, has_ponycopter) VALUES
('Superman', TRUE),
('Batman', FALSE),
('Chuck', TRUE),
('Pinky Pie', TRUE);



# Not needed but nice for debug output
SELECT * FROM lonely_heroes;

# A user with read-only access to a single table
CREATE USER 'anonymous' IDENTIFIED BY 'PiWaC!23CyZzkAYYpi&2S';
GRANT SELECT ON lonely_heroes TO 'anonymous';
