# nlp-stories
In Agile software development, there is a problem where the story backlog gets piled with user stories [1]. In an attempt to effectively and efficiently go through all the stories in the backlog, a proposed method suggest using NLP tools to extract valuable information from these stories [1]. The extracted information will help summarize and categorize similar feedback to shorten the loop. Ultimately, this leads to efficient software development where more feedback is being considered at once [1]. However, accurate NLP tools are necessary before reaching that stage. This repository compares NLP tools' annotations to a benchmark. The benchmark is a set of manually annotated user stories shown in the next section. 

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


### Note:
In the given data set, a few projects contains stories that did not have the expected story structure.
An example, shown below, is when the persona is not directly performing the action on an entity, but rather an entity performing the main action on another entity.
**Annotation for these stories will still follow the annotation guidelines**. Missing annotaions and relations will be considered when evaluating the results  
<img width="750" alt="passive" src="https://user-images.githubusercontent.com/71148152/174147148-d46c7b90-0b59-4303-95be-a34cbbcf5a4b.png">  
The expected structure of the example text above will look something like:
>#G02# As an agency user, I want to be able to submit zero and blank for loan records through the FABS validation rules.

The following projects did not follow expected sentence structure: 
* g02-federal-funding 
* g13-planningpoker
* g17-cask
* g27-culrepo

## NLP Annotaion JSON format
{ \
"Text": "...",\
"Persona": [ "..." ],\
"Action": {"Primary Action": [ "...", ... ], "Secondary Action": ["..."], ... },\
"Entity": { "Primary Entity": [ "...", ... ], "Secondary Entity": [ "...", ...] },\
"Benefit": "...",\
"Triggers": [ [ "...", "..." ] ],\
"Targets": [ [ "...", "..." ], ... ],\
"Contains": [ [ "...", "..." ], ... ]\
}

## References 
![image](https://user-images.githubusercontent.com/71148152/185634777-6674829b-058b-4a3e-ae75-123751e8ba11.png)

