# Setting up the Data
Before comparing and analyzing the NLP's annotations, the results needs to be setup. 

1. jsonl_to_human_readable.py: Converts Doccano annotations output into a json file that is easier to read
   > python setup_data\jsonl_to_human_readable.py `path to raw json file with baseline annotations from Doccano` `saving name` `{BKLG, CAT, GLO}`
     - outputs: `json file with baseline annotations`

2. create_pos_baseline.py: Saves POS tags for each baseline annotation
   > python setup_data\create_pos_baseline.py `path to json file with baseline annotation` `saving name` `{BKLG, CAT, GLO}`
     - outputs: `json file with baseline annotations and corresponding POS tags`

3. ecmfa_vn_restructure_output.py: Restructures ECMFA-VN's results in way that is easier to use
   > python setup_data\ecmfa_vn_restructure_output.py `path to json file with original ECMFA-VN results` `saving name` `{BKLG, CAT, GLO}`
     - outputs: `json file with restructed ECMFA-VN results`
  
4. find_stories_break_visual_narrator.py: Finds the user stories that Visual Narrator can not annotate
   > python setup_data\find_stories_break_visual_narrator.py `path to txt file with user stories` `saving name`
     - outputs: `txt file with valid stories` `txt file with invalid stories`
  
5. merge_data.py: Merges two of the same file type together (json, txt, or final average results csv files)
   > python setup_data\merge_data.py `path to file to append` `path to file that will be copied`
     - outputs: `merges the data into the first path entered into the commandline`
 
6. find_intersecting_stories.py: Finds the stories that intersect (work with) ECMFA-VN and Visual Narrator
   > python setup_data\find_intersecting_stories.py `path to txt file with all the user stories` `path to json file with ECMFA-VN results` `path to txt file with valid Visual Narrator stories` `saving name`
     - outputs: `txt file with intersecting stories` `txt file with left-out stories` `txt file with repeated stories`

7. convert_to_intersecting_stories.py: Saves NLP results that only contains stories from the intersecting stories set
   > python setup_data\convert_to_intersecting_stories.py `path to json file with NLP results` `path to txt file with intersecting stories` `saving name` `{VN, BASE, ECMFA, SIMPLE, CRF}` `{BKLG, CAT, GLO}` `--crf_intersecting_set`
     - outputs: `json file with NLP results of only stories in the intersecting set`

8. run_convert_to_intersecting_stories.py: Runs convert_to_intersecting_stories.py for the whole dataset for a specific type of data grouping
   > python setup_data\run_convert_to_intersecting_stories.py `{BKLG, CAT, GLO}` `--with_crf_intersection`
     - outputs: `json files with NLP results of only stories in the intersecting set`

 ## Abbreviations     
- `BKLG`: Individual Backlog grouping
- `CAT`: Categories grouping
- `GLO`: Global grouping 
- `BASE`: Baseline annotations
- `VN` : Visual Narrator
- `ECMFA` : ECMFA-VN
- `SIMPLE` : Simple NLP
- `CRF` : CRF NLP
