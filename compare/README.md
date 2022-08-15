# Comparisons
## Comparison Modes
We compare the nlp's annotation with the manual baseline annotations to evaluate the accuracy of each nlp tool's ability to annotate the stories. There were three modes of comparisons that we used to evaluate the accuracy

1. Strict Comparison: comparing annotations to be **EXACTLY** the same as the baseline annotations.

   | Baseline Annotation     | NLP Tool Annotation | Comparison Results|
   | ----------------------- | ------------------- | ----------------- |
   | dataset                 | datasets            | FALSE             |
   | many datasets           | datasets            | FALSE             |
   | user's dataset          | [user, datasets]    | FALSE             |
   | dataset                 | dataset             | TRUE              |

2. Inclusion Comparison: comparing annotations to check if the baseline annotations are included in what the nlp annotates

   | Baseline Annotation     | NLP Tool Annotation | Comparison Results|
   | ----------------------- | ------------------- | ----------------- |
   | dataset                 | datasets            | TRUE              |
   | many datasets           | datasets            | FALSE             |
   | user's dataset          | [user, datasets]    | FALSE             |
   | dataset                 | dataset             | TRUE              |

3. Relaxed Comparison: comparing annotations where qualifiers and descriptors of an annotation are ignored when comparing with the baseline annotations.

   | Baseline Annotation     | NLP Tool Annotation | Comparison Results|
   | ----------------------- | ------------------- | ----------------- |
   | dataset                 | datasets            | FALSE             |
   | many datasets           | datasets            | TRUE              |
   | user's dataset          | [user, datasets]    | FALSE             |
   | dataset                 | dataset             | TRUE              |

*The first row is false because baseline determines the word as singular, while the nlp tool determines the word as plural. Thus, they are not the same in context*
<br />*The second row is true because `many` is a qualifier. When ignoring `many`, both the baseline and nlp annotation are the same (`datasets`)*

<br />*Note: The relaxed comparison may ignore qualifiers that can alter the context of the annotation. For example, the relaxed comparison will see `without updating` as just `updating` after removing the qualifier, `without`. `without updating` and `updating` have opposite meanings, and this can impact the overall comparison. This occurs at a minimal level to words with POS of `SCONJ` (ex: without, that).*

## Running Comparison Scripts
### Main Scripts
1. run_comparison.py: Runs all the comparison files for the group data
   > python compare\run_comparison.py `{BKLG, CAT, GLO}` `--with_crf_intersection`
     - outputs: `Graphs of nlp results` `Graphs of individual group results` `Graphs of Average grouping results`
     
2. combine_final_results.py: Combines all final data into one graph
   > python compare\combine_final_results.py `saving name` `graph title` `--with_crf_intersection` `--primary`
     - outputs: `Graph of combined final results` `csv file of combined final results`
     
3. compare_crf_results.py: Compares the different CRF groupings' final results
   > python compare\compare_crf_results.py `saving name` `graph title` `--primary`
     - outputs: `Graph of CRF groupings' final results` 
     
### Sub-Scripts
1. compare_nlp.py: Compares NLP's results against the baseline
   > python compare\compare_nlp.py `path to json file with baseline results` `path to json file with NLP's results` `saving name` `{STRICT, INCLU, RELAX}` `{VN, ECMFA, SIMPLE, CRF}` `{BKLG, CAT, GLO}` `--with_crf`
     - outputs: `Graphs of comparison results for persona, entity, action` `txt file with missing stories` 

2. compare_individual_nlp_total.py: Compares the NLP's final results for a specific data grouping type
   > python compare\compare_individual_nlp_total.py `path to csv file with primary results` `path to csv file with all the results` `{VN, ECMFA, SIMPLE, CRF}` `{BKLG, CAT, GLO}` `--with_crf_intersection`
     - outputs: `Graphs of the NLP's final results` `csv file of average results`
     
3. compare_nlps_total_results.py: Compares all the NLP's final results with each other for a specific data grouping type
   > python compare\compare_nlps_total_results.py `path to Simple NLP's final result's csv file` `path to ECMFA-VN final result's csv file` `path to Visual Narrator final result's csv file` `saving name` `{BKLG, CAT, GLO}` `--load_crf_path`  
     - outputs: `Graphs of all NLPs' final results`
     
4. compare_nlps_average_results.py: Compares all the NLP's final averages with each other for a specific data grouping type
   > python compare\compare_nlps_average_results.py `path to Simple NLP's average result's csv file` `path to ECMFA-VN average result's csv file` `path to Visual Narrator average result's csv file` `saving name` `{BKLG, CAT, GLO}` `--load_crf_path` 
     - outputs: `Graphs of all NLPs' average results` 
     
 #### Terms    
- `BKLG`: Individual Backlog grouping
- `CAT`: Categories grouping
- `GLO`: Global grouping 
- `STRCT`: Strict comparison mode
- `INCLU`: Inclusion comparison mode
- `RELAX`: Relaxed comparison mode
- `VN` : Visual Narrator
- `ECMFA` : ECMFA-VN
- `SIMPLE` : Simple NLP
- `CRF` : CRF NLP
