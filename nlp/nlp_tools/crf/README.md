# CRF
## Creating Inputs
CRF needs a **training** and a **testing** set. The sets contains tuples of information for **each token** in a user story. 
<br /> Tuples contains the following format: **(word, POS tag, annotation label)**

<br /> To create these tuples, use the create_crf_input.py script:
> python nlp\nlp_tools\crf\create_crf_input.py `path to raw json file with baseline annotations from Doccano` `path to txt file with intersecting stories` `saving name` `--append_testing_set` `--amount`
  - outputs: `json file with the training set` `json file with the testing set`

*Note: A user story **does not** appear in both the training and testing set. The script checks to make sure an user story is not in both sets*

## Running CRF
[CRF](https://github.com/ace-design/ace-sklearn-crfsuite) can annotate stories once the training and testing sets are created. CRF needs input parameters (C1, C2) that can be adjusted. Running the optimization commands will optimize these parameters. If optimization is not chosen, then CRF will use the default values (C1 = 0.1, C2 = 0.1). 
> python nlp\nlp_tools\crf\crf_nlp.py `path to json file with the testing set` `--load_training_path` `model name` `{word_pos_feature, pos_feature}` `{BKLG, CAT, GLO}` `--c1` `--c2` `--random_optimize` `--grid_optimize`
  - outputs: `json file with CRF annotation results` `model data`  `txt file with learned information`  `Graphs of optimized parameters`

*Note: If the model already exists, CRF will load the model. This means that CRF will not do any new learning and just use what it had learned from before.*

 ### Abbreviations    
- `BKLG`: Individual Backlog grouping
- `CAT`: Categories grouping
- `GLO`: Global grouping 
