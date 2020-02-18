CREATE TABLE doc (
	doc_id INTEGER PRIMARY KEY,
	doc_title TEXT NOT NULL
);

CREATE TABLE sheet (
	sheet_id INTEGER PRIMARY KEY,
	sheet_title TEXT NOT NULL,
	description TEXT,
	version TEXT,
	copyright TEXT,
	revision TEXT,
	surveyor TEXT,
	AGRRA_code TEXT,
	site_name TEXT,
	date TEXT,
	bottom_temp REAL,
	bottom_temp_units TEXT,
	instrument_type TEXT,
	level TEXT,
	site_comments TEXT,
	doc_id INTEGER,
	FOREIGN KEY(DOC_ID) REFERENCES doc(doc_id)
);

CREATE TABLE transect (
	transect_id INTEGER PRIMARY KEY,
	transect_num INTEGER NOT NULL,
	start_time TEXT,
	start_depth REAL,
	end_depth REAL,
	depth_units TEXT,
	area_surveyed TEXT,
	area_tallied TEXT,
	transect_comments TEXT,
	sheet_id INTEGER,
	FOREIGN KEY(sheet_id) REFERENCES sheet(sheet_id)
);

CREATE TABLE encounter (
	encounter_id INTEGER PRIMARY KEY,
	species_code TEXT NOT NULL,
	num_isolates INTEGER,
	length REAL,
	width REAL,
	height REAL,
	percent_pale REAL,
	percent_bleached REAL,
	bleach_code TEXT,
	part_mort_new REAL,
	part_mort_trans REAL,
	part_mort_old REAL,
	disease TEXT,
	extra_bleach TEXT,
	extra_mort TEXT,
	comments TEXT,
	point_count_l REAL,
	point_count_p REAL,
	point_count_bl REAL,
	point_count_nm REAL,
	point_count_tm REAL,
	point_count_om REAL,
	point_count_other REAL,
	point_count_interval REAL,
	transect_id INTEGER,
	FOREIGN KEY(transect_id) REFERENCES transect(transect_id)
);

CREATE VIEW data AS
SELECT *
FROM doc
INNER JOIN sheet ON doc.doc_id = sheet.doc_id
INNER JOIN transect ON sheet.sheet_id = transect.sheet_id
INNER JOIN encounter ON transect.transect_id = encounter.transect_id;

