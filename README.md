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

### Note:
In the given data set, a few projects contained stories that did not have the expected story structure.
An example, shown below, is when the persona is not directly performing the action on an entity, but rather an entity performing the main action on another entity.
**Annotation for these stories still followed the annotation guidelines**. Missing annotaions and relations will be considered when evaluating the results  
<img width="750" alt="annotation_of_unexpected_structure_example" src="https://user-images.githubusercontent.com/71148152/169082188-d4b526a1-4707-4c98-a5e0-76190e86be95.png">  
The expected structure of the example text above will look something like:
>#G02# As an agency user, I want to be able to submit zero and blank for loan records through the FABS validation rules.

The following projects did not follow expected sentence structure: 
* g02-federal-funding 
* g08-frictionless
