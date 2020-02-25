SELECT genus, species, species_code, num_isolates, length, width, height,
percent_pale, percent_bleached, bleach_code, part_mort_new, part_mort_trans,
part_mort_old, disease, extra_bleach, extra_mort, comments, point_count_l,
point_count_p, point_count_bl, point_count_nm, point_count_tm, point_count_om,
point_count_other
FROM data
WHERE doc_title='AGRRA Coral Data Entry - Aquarium.xlsx'
AND transect_num=1;

