# ASL Practice + Dataset Capture Workflow

Use this workflow so that **ASL practice stays primary** while your database grows almost automatically.

## 1. Choose one sentence or exercise

- Read the English prompt.
- Watch the instructor/reference.
- Focus on meaning, sign order, handshape, movement, and facial grammar.

## 2. Practice the full sentence 2–3 times without recording

The goal is to **learn the sentence first**, not perform for the dataset immediately.

## 3. Break out the useful sign units

Identify the actual ASL signs/components you want isolated examples of.

- Do not assume every English word maps 1:1 to an ASL sign.
- Prioritize signs that are difficult, unfamiliar, or useful to preserve as isolated examples.

## 4. Capture isolated signs

For each sign:

1. Run `asl_obs_capture.py`.
2. Enter the label or English prompt, for example: `bowling`
3. Choose `word` as the capture type.
4. Record one take.
5. If it felt fine, stop there. With only one take, the script automatically marks it as preferred.
6. If needed, record additional takes.
7. Rate each take as `good`, `uncertain`, `incorrect`, or `practice`.
8. If there are multiple takes, choose the preferred take—or choose none if none felt good enough.

## 5. Practice the complete sentence again

Now that you have isolated difficult components, put them back into continuous signing.

Focus on:

- smooth transitions
- natural timing
- sign order
- facial grammar
- overall meaning

## 6. Capture the complete sentence

Run the same tool again, for example:

```text
prompt_en = Have you ever taken up bowling?
capture_type = sentence
```

Then:

- Record one satisfactory take and stop, or
- Record several takes and choose the best one, or
- Leave all takes as non-preferred if none felt good.

## 7. Leave ASL gloss for later when needed

During the study session, do not interrupt your learning flow just to create a gloss annotation.

It is fine to keep:

```json
"ASL_gloss": null
```

You can manually annotate or programmatically generate gloss later.

## Example session

A single lesson might produce:

```text
BOWLING
TAKE-UP
YOU

full sentence take 1
full sentence take 2
```

The important point is that you are **still studying ASL the whole time**. The structured dataset is a byproduct of the learning session.

## How to think about the workflow

Do not think:

> I need to build a good ML dataset.

Instead:

> I am practicing ASL, and my practice system happens to preserve structured examples.

This helps prevent data collection from taking over the learning activity.

## Keep imperfect takes

Do not automatically delete mistakes.

A recording such as:

```json
{
  "self_quality": "incorrect",
  "preferred_take": false
}
```

may later be valuable for models that distinguish:

- correct vs. incorrect signing
- learner errors
- confidence or quality levels
- progress over time

## What your database can eventually represent

Over time, your dataset can become a longitudinal record of:

```text
prompt
→ attempts
→ self-evaluation
→ preferred performance
→ eventual verified annotation
```

That is much richer than keeping only polished “correct” examples.

## Recommended unit of work

Keep each study cycle small:

```text
one sentence
→ isolate difficult signs
→ capture isolated signs
→ capture the full sentence
→ move to the next exercise
```

This keeps the workflow fast enough that ASL learning remains the primary activity.
