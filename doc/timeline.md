# Overview of the timeline for Persona POC

* **Status:** <span style="color: #999999;">⚪ Planned</span>
* **Status:** <span style="color: #28a745;">✅ Completed</span>
* **Status:** <span style="color: #ffc107;">🟠 In Progress</span>
* **Status:** <span style="color: #dc3545;">🔴 Not Started</span>
* **Status:** <span style="color: #6c757d;">⏸️ On Hold</span>
* **Status:** <span style="color: #808080;">⚪ Not Planned</span>
* **Status:** <span style="color: #ff6600;">⚠️ Delayed</span>
* **Status:** <span style="color: #17a2b8;">➡️ Deferred</span>
* **Status:** <span style="color: #ffc107;">🟠 In Progress</span>
---

### 21-May : Getting to know
* **Status:** <span style="color: #28a745;">✅ Completed</span>
* **Description:** The service is about solving communication problems. Use cases are difficult to address communications, training for a press conference or meet, planning a pitch.
* **Task:** Exploratory : find out how such a system may work. Try figuring out architecure of such system.

### 22-May - 27-May : Explore implementation options
* **Status:** <span style="color: #ffc107;">🟠 In Progress</span>
* **Description:** Create a spec for system, formulate a development process, plan a deployment. Explore AI engg methodologies.
* **Task:** Exploratory : Current ML state. Find out atomic entities. List potential candidates for the system parts.

### 28-May : Meet the team, discuss POC specs
* **Status:** <span style="color: #28a745;">✅ Completed</span>
* **Description:** There would be three PR journalist. A pitch would be provided
* **Task:** Set up infrastucture for the app. Go through stanford paper and github repo. Setup a development environment and start work on framework (NLP, Persona identifiers).
* **Resources:** 
    * [Agent Simulation](https://github.com/joonspk-research/genagents/tree/main?tab=readme-ov-file)
    * [Big AGI - agent](https://get.big-agi.com)
    * [Synthetic users](https://www.syntheticusers.com/science)
    * [PR stats](https://www.sortlist.co.uk/datahub/reports/pr-statistics/)
    * [PR gist](https://review.firstround.com/heres-what-i-learned-from-working-with-50-pr-firms/)
    * [PR advice](https://review.firstround.com/how-new-startups-can-win-at-pr-advice-from-a-20-year-comms-career/)

### 4-May : Show the plan, initial layout
* **Status:** <span style="color: #ff6600;">⚠️ Delayed</span>
* **Description:** Show current state, plan next steps and improvements. <i>Got postponed to 5-May. Ensure better adherence to timeline</i>.
* **Task:** Request for third party softwares (OpenAI key, org github). Research on how to make personas more like real people. <b>Get response structure (parameters of evaluation, and ways of presenting them) of a journalist</b>. List ways of representing a persona (traits etc.)

### 11-May : Deploy first draft
* **Status:** <span style="color: #999999;">⚪ Planned</span>
* **Description:** Deploy three personas with some efficiency. List data sources for the personas.

### 18-May : Persona research
* **Status:** <span style="color: #999999;">⚪ Planned</span>
* **Description:** Train model with new data. Improve upon architecture to accomodate new data.

### 25-May : Review
* **Status:** <span style="color: #999999;">⚪ Planned</span>
* **Description:** Review the POC. Improve UI.

### 29-May : Review
* **Status:** <span style="color: #999999;">⚪ Planned</span>
* **Description:** Review improvements.

### 30-May : Review
* **Status:** <span style="color: #999999;">⚪ Planned</span>
* **Description:** Review the entire deployment and plan next steps.


## Modules
* Persona Management Module - Thin persona is ready. Working on enriching it.
* Pitch analysis - Currently a simple summarizer, planning on using context from persona (weighted biases, values, triggers, avoidances).
* Knowledge graph - TODO - Knowledge of a persona on a given topic.
* Response module - Currently based on a template.

## Missing
* Weighted response attributes. What attributes does persona uses to assess the pitch, how much of weight do they provide to each attribute. List of such attributes.
* Response structure. Is free flow text report generated from "weighted response attributes" assessment sufficient.

## Still in wild
* Psychology traits :  OCEAN model [personality traits](https://en.wikipedia.org/wiki/Big_Five_personality_traits)
* Cognitive biases : [biases](https://en.wikipedia.org/wiki/List_of_cognitive_biases)
* Fallacies : [fallacies](https://en.wikipedia.org/wiki/List_of_fallacies)
* Study : spaCy, Tensorflow.

## Requirements
### 4-June
* Get PR journalist sample (few names, some work)
* Discuss persona traits, traits which influence pitch asessment.
* Discuss persona response
* Github account
* OpenAI, ChatGPT, Gemini key (still unsure, will work out)
* Cloud deployment (Azure, Amazon, Google)
* Code helpers => [Copilot](https://github.com/copilot) , [text](https://jules.google) (optional for now)

## Further
* [Google AI studio](https://aistudio.google.com/welcome)
* Veo 3 => Video generation model
* [Videos using Veo 3](https://labs.google/flow/about)