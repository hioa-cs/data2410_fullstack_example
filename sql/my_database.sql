CREATE DATABASE all_the_things;
USE all_the_things;

CREATE TABLE lonely_heroes (
    id             INT unsigned NOT NULL AUTO_INCREMENT,     
    name           VARCHAR(150) NOT NULL,
    email          VARCHAR(150),
    has_ponycopter BOOLEAN NOT NULL default FALSE,
    access_level   INT unsigned NOT NULL default 0, #NOTE: This means anyone who can read can see the access levels.
    image          VARCHAR(1024) default "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/The_Jolly_Nero.jpg/1024px-The_Jolly_Nero.jpg",
    PRIMARY KEY     (id)
);
 
# Not needed but nice for debug output
DESCRIBE lonely_heroes;

# Add your own gmail user here!
INSERT INTO lonely_heroes (name, email, has_ponycopter, access_level, image) VALUES
('Superman', NULL, TRUE, 0, "https://i.pinimg.com/originals/14/86/36/1486361592bfd0866cd900572833db0f.jpg"),
('Batman', NULL, FALSE, 0, "https://i.ytimg.com/vi/RDhfnPSTqmk/maxresdefault.jpg"),
('Chuck', NULL, TRUE, 100, DEFAULT),
('Derek B.','derek.bipartisan@gmail.com',TRUE, 10, DEFAULT),
('Alfred','alfred.bratterud@gmail.com',FALSE, 100, DEFAULT),
('Pinky Pie',NULL,TRUE, 1000, "https://static.wikia.nocookie.net/mlp/images/b/b2/Pinkie_Pie_ID_S4E11.png");

# Not needed but nice for debug output
SELECT * FROM lonely_heroes;

# A user with read-only access to a single table
CREATE USER 'anonymous' IDENTIFIED BY 'PiWaC!23CyZzkAYYpi&2S';
GRANT SELECT ON lonely_heroes TO 'anonymous';
