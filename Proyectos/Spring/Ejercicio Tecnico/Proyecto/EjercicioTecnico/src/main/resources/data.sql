-- ADMINS
-- Usuario ADMIN (Contraseña: 'admin123')
INSERT INTO T_USER (username, password, role, blocked, created_at) 
VALUES ('admin', 'admin123', 'ADMIN', false, CURRENT_TIMESTAMP);
-- Usuario ADMIN (Contraseña: 'admin123')
INSERT INTO T_USER (username, password, role, blocked, created_at) 
VALUES ('adminBloqueado', 'admin123', 'ADMIN', true, CURRENT_TIMESTAMP);

-- NOADMINS
-- Usuario NORMAL (Contraseña: 'user123')
INSERT INTO T_USER (username, password, role, blocked, created_at) 
VALUES ('usuario1', 'user123', 'USER', false, CURRENT_TIMESTAMP);
-- USUARIO NO ADMIN (Contraseña: 'user123')
INSERT INTO T_USER (username, password, role, blocked, created_at) 
VALUES ('noEsAdmin', 'admin123', 'USER', false, CURRENT_TIMESTAMP);
-- Usuario NORMAL (Contraseña: 'user123')
INSERT INTO T_USER (username, password, role, blocked, created_at) 
VALUES ('usuarioBloqueado', 'user123', 'USER', false, CURRENT_TIMESTAMP);
