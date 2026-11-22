# PROV-DM: The PROV Data Model (W3C, 2013)

- **Source:** W3C Recommendation, 30 April 2013, edited by L. Moreau and P. Missier · https://www.w3.org/TR/prov-dm/
- **File:** `../papers/w3c-2013-prov-dm.txt` (the page turned into text on 2026-11-22; it has no page numbers, so sections are cited)
- **Licence:** W3C Document License. The text is kept on the machine that read it.
- **Evidence:** a standard: definitions, not findings.
- **Read:** part of the text: the abstract, sections 2.1, 2.1.1 and 2.1.2 (core structures, entity and activity, derivation), 5.1.1 (entity), 5.1.3 (generation), 5.1.8 (invalidation, its definition and first examples), 5.2.1 to 5.2.3 (derivation, revision, quotation). Not read: agents, bundles, collections, the constraints document · 2026-11-22

## What it says
- An entity is a thing with some fixed aspects. When an aspect changes, it is another entity: a green traffic light that turns red is described as two entities (sections 2.1.1, 5.1.8).
- A derivation links a new entity to the earlier one it was transformed from, updated from or built on (sections 2.1.2, 5.2.1).
- Having used something does not make the result a derivation of it: the earlier entity has to have influenced the new one, and the standard leaves it to the describer to decide when that holds (section 2.1.2).
- A revision is a derivation whose result is a revised version of an original (section 5.2.2).
- Generation is the moment an entity comes to exist, and it can carry a time (section 5.1.3).
- Invalidation is the start of the end of an entity; after it the entity is no longer available for use (section 5.1.8).

## What it means for the plugin
- The **Id** names an object, and **From** is the derivation: what the object rests on. From lists what shaped the object, not everything that was read.
- A conclusion whose sentence changes is another version of it. This is why a challenge stamp is tied to a hash of the sentence, and why a weakened conclusion is challenged and stamped as the narrower sentence.
- The standard has no notion of "stale". The rule that an object is stale when something in its From was dropped, weakened or challenged again after it was written is the lab's own product decision; PROV-DM supplies the words (entity, derivation, the time an entity was made, invalidation).

## Quotes
- "An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects"
- "A derivation is a transformation of an entity into another, an update of an entity resulting in a new one, or the construction of a new entity based on a pre-existing entity."
- "PROV does not attempt to specify the conditions under which derivations exist"
- "is a derivation for which the resulting entity is a revised version of some original"
- "The entity is no longer available for use (or further invalidation) after invalidation."
