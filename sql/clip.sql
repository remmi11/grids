CREATE TABLE new_lines AS SELECT lines.* FROM lines, places WHERE ST_Intersects(places.geom, lines.geom) AND places.name = 'San Mateo';

DROP TABLE IF EXISTS san_mateo_city_lines;
CREATE TABLE san_mateo_city_lines AS 

SELECT san_mateo_lines.* 

FROM san_mateo_lines, 

places 

WHERE ST_Intersects(places.geom, san_mateo_lines.geom) AND places.name = 'San Mateo';

SELECT * 
INTO san_mateo_places
FROM places WHERE name = 'San Mateo';

ALTER TABLE san_mateo_lines
 ALTER COLUMN geom TYPE geometry(MultiLineString,4326) 
  USING ST_Transform(geom,4326);

DELETE FROM san_mateo_lines WHERE geom = '';