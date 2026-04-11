## Alignment Phases (idea to plan)

**pa-scout** == check-in what the agent should know about 
- I want you to show me how should I use remote functions in this codebase
- obsidian ; sdc
   Peux-tu me montrer toutes les notes en lien avec ce dossier?

````shell
Force the model to touch all relevant parts of the codebase — moving from a vague ticket to a concrete list of technical inquiries. This is the first defense against the instruction budget problem: instead of cramming alignment into a mega-prompt, it happens through targeted questions.
````

**pa-scope** == let the agent gather fact about the projet

````shell
- Research (R) — Gather objective facts about the current codebase
- Hide the original feature ticket during this phase
- Trace logic flows and identify existing endpoints without forming opinions on changes
- Produce a technical map — factual record only
- not a plan or recommendation
- Human reviews the factual record before any implementation thinking begins
- Address the plan-reading illusion by building a factual record, not a persuasive narrative
````

**pa-vision** == here is where we're going

````shell
The highest-leverage stage. The agent “brain dumps” its understanding into a ~200-line markdown artifact covering current state, desired end state, and design decisions. The engineer reviews the agent’s proposed patterns. If the agent picks a legacy pattern the team has moved away from, the human performs what Horthy calls “brain surgery” — redirecting the agent toward correct architectural standards before any code is planned. This replaces the magic words trap with an explicit alignment conversation that happens by default, not by incantation.
````

**pa-architect** == here is how do we get there

````shell
If the design is “where we’re going,” the structure outline is “how we get there.” Horthy compares it to a C header file — it defines signatures, new types, and high-level phases. This is where vertical slices get enforced: build a mock API, then the front end, then the database, with checkpoints after each slice. Not horizontal plans that can’t be tested until everything is assembled.
````
