DROP TABLE IF EXISTS country;
CREATE TABLE country(iso_country TEXT PRIMARY KEY, name TEXT);
INSERT INTO country(iso_country,name) values("FI", "FINLAND");
INSERT INTO country(iso_country,name) values("JP", "JAPAN");
INSERT INTO country(iso_country,name) values("FR", "FRANCE");
INSERT INTO country(iso_country,name) values("BEL", "BELGIQUE");
INSERT INTO country(iso_country,name) values("TG", "TOGO");
INSERT INTO country(iso_country,name) values("THA", "THAïLANDE");
INSERT INTO country(iso_country,name) values("KR", "KOREA");

DROP TABLE IF EXISTS airport;
CREATE TABLE airport(iata_code TEXT PRIMARY KEY,
                     name TEXT,
                     iso_country TEXT,
                     FOREIGN KEY (iso_country) REFERENCES country(iso_country)
                    );
INSERT INTO airport(iata_code,name, iso_country ) VALUES("ENF","Enontekio Airport", "FI");
