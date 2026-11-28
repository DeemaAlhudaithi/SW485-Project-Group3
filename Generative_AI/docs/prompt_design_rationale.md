# Prompt Design Rationale (Phase 2 – Part B)

This document explains how the two prompt templates in `Phase2_Generative_AI.ipynb` were designed, what we learned while testing them, and which references we used.

## 1. Thought process

**Goal.** The Generative AI component must not predict or diagnose. It receives the outputs of the two existing models (the supervised screening result and probability, the key indicators, and the cluster segment with its profile) and turns them into a short briefing that a non-expert can read.

**Two different communication goals.** We wanted two templates that are truly different, not two wordings of the same idea:

- **Template 1 (PT-01), Individual Patient Risk Briefing:** explains the result for one patient (summary, indicators, segment context, follow-up).
- **Template 2 (PT-02), Individual Executive Risk Summary:** a decision-oriented summary that also adds the segment size and the segment diabetes rate.

**Thought process for each template.**

- *Template 1:* the reader should understand what the screening result means for one patient. It therefore has four short sections (summary, indicators, segment context, follow-up), asks for plain language, and keeps the individual probability separate from the group-level cluster profile. It adds no information beyond the model outputs.
- *Template 2:* the reader is a decision-maker who wants the risk level and what to do next. It therefore adds the segment size and the segment diabetes rate as context, uses the titles Executive Summary, Expected Risk Level, Key Drivers and Suggested Next Steps, and asks for the next steps as bullet points.

**Same inputs for a fair comparison.** Template 2 first started as a segment-level summary. We changed it to an individual-level summary, so that both templates are tested on the same three patients (High, Moderate, Low risk) and the comparison is fair.

**Prompt structure.** Both templates use the same layout: Role, Rules, Patient data inside `<patient_data>` delimiters, and an Output format with fixed section titles and a limit of 180 words. A fixed format makes the outputs easy to compare and to check.

**Evaluation.** Each output was read manually and measured with four quantitative metrics (length, keyword alignment, Flesch-Kincaid grade, Flesch reading ease). A second language model (`qwen/qwen3.8-27b`) simulated user preference on the five qualitative criteria. The writing model is `openai/gpt-oss-20b`, so the reviewer is a different model.

## 2. How domain knowledge influenced the prompts

- **Screening, not diagnosis.** The supervised model is a screening aid. The rules therefore forbid independent diagnoses and require the result to be described exactly as given.
- **Individual versus group.** A cluster profile describes a group, not the patient. Presenting group traits (for example lower income) as personal facts could be wrong and stigmatizing, so both templates ask the model to keep the two levels separate. Template 2 also requires the diabetes rate to be marked as a group figure.
- **Probability and threshold.** The screening threshold from Phase 1 (0.35) favors catching at-risk patients, so some patients are flagged without being at risk. The wording avoids creating alarm, and the probability is always stated as given.
- **Global indicators.** The key contributing indicators are the top features of the supervised model overall. They are not calculated per patient, so every patient receives the same indicators and the prompt asks only to write them in plain words and not to explain causes. In the test cases the same three indicators (HighBP, GenHlth, HighChol) are therefore used for all patients, as in the final pipeline.
- **Data source.** The models are based on the CDC BRFSS 2015 survey (self-reported, one country, one year). The prompt therefore uses only the supplied data and does not add medical facts.
- **Privacy.** The prompt contains no names, identifiers or raw answers.

## 3. Prompt iterations and lessons learned

### Template 1: two versions

| Version | Change | Reason |
|---|---|---|
| v1 | Role, rules (no diagnosis, use only the given data, no specific tests/referrals/medications/symptoms, "the patient", exact screening result, probability stated, group versus individual) and output format | First version used in the tests. |
| v2 | Added the rule "In Suggested Follow-up Considerations, do not introduce any new action. Only restate the follow-up implied by the provided screening result." | In earlier runs the follow-up section added lifestyle review, monitoring, "potential interventions", and once "possible referrals", although v1 asked for general follow-up only. |

In the final run with v2, the follow-up section only restated the follow-up implied by the screening result in all three cases. Because the indicators in the test cases and the natural variation between runs also changed, we cannot say how much of the improvement is due to the new rule.

### Template 2: three versions

| Version | Change | Reason |
|---|---|---|
| v1 | Segment-level executive summary | Changed to an individual-level summary so that both templates use the same patients. |
| v2 | Rules added: describe the result exactly as given, add no interpretations or conditions, do not explain causes, say the segment diabetes rate describes the group | In test outputs the model wrote that something was "scheduled", added interpretations such as "burden of disease" and "comorbid conditions", and presented group figures as the patient's own. |
| v3 | Next steps must stay general and supported by the screening result, with a list of things not to name; a rule to separate the individual probability from the cluster profile | The model still suggested specific actions and sometimes wrote cluster traits as the patient's own. |

Even after v3, the final Template 2 outputs still broke its rules in all three cases (for example "The patient should be referred for further clinical assessment", "Consider routine monitoring of blood glucose" and "The patient is scheduled for a routine follow-up"). A written rule lowers the chance of a violation but does not remove it.

### Lessons

1. **Rules should come from observed failures.** Most rules were added after reading real outputs, not before.
2. **Rules reduce errors but do not guarantee them.** Template 1 also added suggestions that its first rules did not prevent (for example "possible referrals for cardiovascular assessment", lifestyle review and monitoring in the follow-up section). An automatic check of forbidden words before showing the text is a proposed safeguard.
3. **Outputs vary between runs,** even at temperature 0.2, so conclusions from three cases are indicative, not conclusive. Between two runs of the identical Template 2 prompt and inputs, keyword alignment changed from 0.39 to 1.00 and the average length from 122 to 146 words.
4. **A required output section can push the model to invent content.** A mandatory list of next steps may have encouraged Template 2 to add steps (a hypothesis we did not test).
5. **A language-model reviewer is not a safety check.** Both reviewers we tried (first the writing model, then Qwen) gave Template 2 a Safety score of 5 although the manual reading found unsupported actions. The reviewer did not separate the templates, so the manual reading was given more weight.
6. **Use a different model as reviewer** to avoid a model rating its own writing.
7. **Check that the notebook runs the latest code.** Editing a cell without running it keeps the old variable in memory, which at one point made us read results of an old prompt. Run the notebook from top to bottom before drawing conclusions.
8. **Identical indicators can mislead the text.** Every patient receives the same global indicators (HighBP, GenHlth, HighChol). In the final run both templates listed "high blood pressure" and "high cholesterol" for the Low-risk patient whose cluster profile says normal blood pressure and cholesterol, and Template 1 wrote "the patient's high blood pressure ... contributed to the screening outcome". A possible fix (not tested) is to label the field as "most influential model features (the same for all patients)" and to forbid describing them as the patient's conditions.
9. **Handle API limits.** The service returned rate-limit errors (429), so the reviewer calls retry after a pause.

## 4. Selection result

Template 1 was selected because it deviated less from its rules in our tests. In the final run Template 1 stated the probability as given, kept the cluster profile as a group description and only restated the follow-up implied by the screening result in all three cases. Template 2 broke its own rules in all three cases (referral, monitoring of blood glucose, "scheduled" follow-up, lifestyle and symptom advice, and a group trait presented as the patient's own). Template 2 is easier to read and more detailed. Both templates share one weakness: the global indicators can read as the patient's own conditions. The selection is indicative, because there were only three cases and one final run. The full evidence and limitations are in Sections 20, 21 and 23 of the notebook.

## 5. References

1. Groq, "Prompting Guide", https://console.groq.com/docs/prompting
2. OpenAI, "Prompt Engineering", https://developers.openai.com/api/docs/guides/prompt-engineering

Both guides influenced the structure of the templates: a clear role, rules written as bullet points and placed first, input data separated from instructions by delimiters, and an explicit output format with a length limit.