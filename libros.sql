CREATE DATABASE IF NOT EXISTS PEPS;
USE PEPS;
CREATE TABLE libros(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(9,2) NOT NULL,
	imagen BLOB(255)
);
CREATE TABLE usuarios(
	usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL,
    estado VARCHAR(10) NOT NULL,
    numAccesosErroneos INTEGER,	
    fechaUltimoAcceso DATE
);
INSERT INTO `usuarios` (`usuario`, `clave`, `perfil`,`estado`, `numAccesosErroneos`,`fechaUltimoAcceso`) VALUES ('root', '$2b$10$JJdnLnCjYmNYpGQ8OJVUD.UmKx2jspOYnXOI9rZm5I9DX5GLYNUP6', 'admin', 'activo', 0, '2022-03-01 00:00');