# nlp-stories
## Annotation Guidelines

Each document is an isolated story.

> *#GXX# As an Applicant, I want to Submit Application, so that I can provide my  information, plans and/or documents to initiate a transaction with the County.*

You can use the following labels:

* `PID`: the _project ID_ used to remember from which project this story is extracted;
* `Persona`: the _noun_ used to name each persona involved in this story;
  * Adjectives are included in the persona `Public User` and not only `User` 
* `Action`: an action (_verb_) used by a Persona to act on an Entity;
  * Adjectives are included in the action `quickly upload` and not only `upload`
  * Sometimes a verb may be used to describe an entity. In such as case, it is not an action but a descriptor. For example, `the updated data`
* `Entity`: a _noun_ representing an element iunvolved in the system;
  * Adjectives are included in the entity: `Supporting Documentation` and not only `Documentation` 
* `Benefit`: the outcome of the action

You can use the followiong relations:

* `triggers`: a relation between a Persona and an Action;
* `targets`: a relation between an Action and an entity;
* `contains`:  relation between two Entities, indicating that one entity contains another one.
### Example
<img width="750" alt="annotation_example" src="https://user-images.githubusercontent.com/71148152/169074277-50f0b1dc-4b99-444b-bfe5-631b3edf052b.png">

* In this example, the story comes from project `GXX`. 
* The involved persona is named `Applicant`, and their associated action is to `Submit` an entity named `Application`. 
  * Thus, there is a relation between `Applicant` and `Submit` (`triggers`);
  * and another one between `submit` and `Application` (`targets`).
* The benefit is composed of all the text starting after the "_so that_" fragment;
  * it also defines several entities, and one action. Some of the entities refines what an `Application` is (e.g., information, plans), implying a `contains` relation.

### Comparisons
We compare the nlp's annotation with the manual baseline annotations to evaluate the accuracy of each nlp tool's ability to annotate the stories. There were three modes of comparisons that we used to evaluate the accuracy

1. Strict Comparison: comparing annotations to be **EXACTLY** the same as the baseline annotations.

   | Baseline Annotation     | NLP Tool Annotation | Comparison Results|
   | ----------------------- | ------------------- | ----------------- |
   | dataset                 | datasets            | FALSE             |
   | many datasets           | datasets            | FALSE             |
   | user's dataset          | [user, datasets]    | FALSE             |
   | dataset                 | dataset             | TRUE              |

2. Inlcusion Comparison: comparing annotations to check if the baseline annotations are included in what the nlp annotates

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

### Running Scripts
1. simple_nlp.py: Most basic nlp that identifies the persona, entities and actions within the story using a list of known words
   > python simple_nlp.py `path to txt file with stories`  `name of file to save`
     - outputs: `json file of annotated info for each story`

2. run_visual_narrator.py: runs visual narrator nlp and outputs a compatible json file to easily work with
   > python run_visual_narrator.py `path to txt file with stories`  `name of file to save`
     - outputs: `json file of annotated info for each story`

3. jsonl_to_human_readable.py: converts jsonl file from doccano to compatible json file to easily work with
   > python jsonl_to_human_readable.py `path to jsonl file from doccano`  `name of file to save`
     - outputs: `json file of annotated info for each story`

4. ecmfa_vn_restructed_output.py: convert ecmfa_vn's nlp results to a compatible json file to easily work with
   > python ecmfa_vn_restructed_output.py `path to json file of ecmfa_vn's results`  `name of file to save`
     - outputs: `json file of annotated info for each story`

5. find_stories_break_visual_narrator.py: indicate and saves the stories that crashes visual narrator
   > python find_stories_break_visual_narrator.py `path to txt file with stories`  `name of file to save`
     - outputs: `txt file of valid visual narrator stories` `txt file of invalid visual narrator stories`

6. find_intersecting_stories.py: indicates and saves the stories that are compatible with all nlp tools
   > python find_intersecting_stories.py `path to txt file with stories` `path to json file of ecmfa_vn's results` `path to txt file with valid visual narrator stories` `name of file to save`
     - outputs: `txt file of intersecting stories` `txt file of stories not included from each nlp`

7. create_pos_baseline.py: include POS info of all the annotations into the json file (for baseline annotations only)
   > python create_pos_baseline.py `path to baseline jsonl file`  `name of file to save`
     - outputs: `json file of annotated info with POS for each story`

8. convert_to_intersecting_stories.py: creates json file that only includes the nlp results of intersecting stories 
   > python convert_to_intersecting_stories.py `path to json file of nlp results` `path to txt file of intersecting stories` `name of file to save` `["VN", "BASE", "ecmfa_vn", "SIMPLE"]`
     - outputs: `json file of annotated info for only the intersecting stories`

9. comparison.py: compare the nlp tools annotations with the baseline annotations
    > python comparison.py `path to json file of baseline results` `path to json file of nlp results` `name of file to save` `comparison mode`
      - outputs: `png bargraphs of results for persona, entity, action for all and primary comparison` `txt file with missing stories that were not compared` `update csv files with final results` `update dataset txt file to indicate what dataset has just been compared`

10. nlp_dataset_results.py: combine all the results of each dataset annotated by one nlp tool
    > python nlp_dataset_results.py `path to csv file of primary results` `path to csv file of all results` `path to txt file of datasets that were used` `name of file to save` `number of datasets in csv files`
      - outputs: `png bargraphs for persona, entity, action for all and primary comparison of all datasets` `png scatterplot graphs for persona, entity, action for all and primary comparison of all datasets` `copy of csv files`

11. compare_all_nlp_results.py: compare the final results for each dataset among all the different nlp tools
    > python compare_all_nlp_results.py `path to simple final result's csv file` `path to ecmfa_vn final result's csv file` `path to visual narrator final result's csv file` `name of file to save` `number of datasets`
      - outputs: `png bargraph for each persona, action and entity`
      - 
12. compare_all_nlp_average.py: compare all average final results among all the different nlp tools
    > python compare_all_nlp_average.py `path to simple average result's csv file` `path to ecmfa_vn average result's csv file` `path to visual narrator average result's csv file` `name of file to save`
      - outputs: `png bargraphs for each precision, recall and f-measure`

13. create_crf_input.py: creates the input required for crf nlp tool
    > python create_crf_input.py `path to jsonl file from doccano` `name of file to save`


### Note:
In the given data set, a few projects contained stories that did not have the expected story structure.
An example, shown below, is when the persona is not directly performing the action on an entity, but rather an entity performing the main action on another entity.
**Annotation for these stories still followed the annotation guidelines**. Missing annotaions and relations will be considered when evaluating the results  
<img width="750" alt="passive" src="https://user-images.githubusercontent.com/71148152/174147148-d46c7b90-0b59-4303-95be-a34cbbcf5a4b.png">  
The expected structure of the example text above will look something like:
>#G02# As an agency user, I want to be able to submit zero and blank for loan records through the FABS validation rules.

The following projects did not follow expected sentence structure: 
* g02-federal-funding 
* g13-planningpoker
* g17-cask
* g27-culrepo
