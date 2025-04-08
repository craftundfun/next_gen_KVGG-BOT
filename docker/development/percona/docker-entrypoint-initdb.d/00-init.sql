CREATE USER 'kvggnextgendev'@'%' IDENTIFIED BY 'kvggnextgendev';
CREATE DATABASE `kvggnextgendev` DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON hopaydev.* TO 'kvggnextgendev'@'%';
FLUSH PRIVILEGES;
