--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.4 в Пн янв 8 23:30:46 2024
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: levels
CREATE TABLE IF NOT EXISTS levels (state TEXT NOT NULL, stars INTEGER NOT NULL, time TEXT NOT NULL, attempts INTEGER NOT NULL);
INSERT INTO levels (state, stars, time, attempts) VALUES ('заблок', 0, '00:00', 0);
INSERT INTO levels (state, stars, time, attempts) VALUES ('разблок', 0, '00:00', 0);
INSERT INTO levels (state, stars, time, attempts) VALUES ('заблок', 0, '00:00', 0);
INSERT INTO levels (state, stars, time, attempts) VALUES ('заблок', 0, '00:00', 0);
INSERT INTO levels (state, stars, time, attempts) VALUES ('заблок', 0, '00:00', 0);
INSERT INTO levels (state, stars, time, attempts) VALUES ('заблок', 0, '00:00', 0);
INSERT INTO levels (state, stars, time, attempts) VALUES ('заблок', 0, '00:00', 0);
INSERT INTO levels (state, stars, time, attempts) VALUES ('заблок', 0, '00:00', 0);
INSERT INTO levels (state, stars, time, attempts) VALUES ('заблок', 0, '00:00', 0);
INSERT INTO levels (state, stars, time, attempts) VALUES ('заблок', 0, '00:00', 0);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
