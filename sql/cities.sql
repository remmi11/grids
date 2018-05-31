ALTER TABLE belmont DROP COLUMN objectid;
ALTER TABLE belmont DROP COLUMN shape_leng;
ALTER TABLE belmont DROP COLUMN shape_area;
ALTER TABLE belmont ADD COLUMN name text;
ALTER TABLE belmont RENAME COLUMN gid TO objectid;

ALTER TABLE foster_city DROP COLUMN objectid;
ALTER TABLE foster_city DROP COLUMN shape_leng;
ALTER TABLE foster_city DROP COLUMN shape_area;
ALTER TABLE foster_city ADD COLUMN name text;

ALTER TABLE fremont DROP COLUMN objectid;
ALTER TABLE fremont DROP COLUMN shape_leng;
ALTER TABLE fremont DROP COLUMN shape_area;
ALTER TABLE fremont ADD COLUMN name text;

ALTER TABLE san_carlos DROP COLUMN objectid;
ALTER TABLE san_carlos DROP COLUMN shape_leng;
ALTER TABLE san_carlos DROP COLUMN shape_area;
ALTER TABLE san_carlos ADD COLUMN name text;

ALTER TABLE san_mateo DROP COLUMN objectid;
ALTER TABLE san_mateo DROP COLUMN shape_leng;
ALTER TABLE san_mateo DROP COLUMN shape_area;
ALTER TABLE san_mateo ADD COLUMN name text;