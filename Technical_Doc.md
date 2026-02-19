# Technical Documentation

## Prompt Tuning Strategy

The system prompt is designed to simulate an interviewer across different roles. The goal is to produce realistic, interview-ready questions instead of generic LLM outputs.

Key design choices:

### 1) Role and Experience driven Context

User inputs are combined into a single job description string:

```
<Job Role> – <Experience Level> – Focus on <Skill>
```

This ensures the LLM to recieve rich context.

### 2) Strict Output Constraints

The model is instructed to:

* Generate only interview questions and rubric
* Avoid explanations or markdown
* Return **valid JSON only**

This reduces hallucinated text and ensures predictable parsing.

### 3) Balanced Skill Focus

Prompt explicitly states:

* Skill focus should influence but not dominate generation
* Questions must still align with role and seniority

This prevents the model from producing questions only about the optional skill.

### 4) Interview Realism Emphasis

Prompt discourages generic questions and asks for:

* Role-specific scenarios
* Seniority-appropriate depth
* Hiring-ready evaluation rubric

---

## Difficulty Calibration Logic

Difficulty is not hard-coded.
It is **implicitly derived from experience level**.

| Experience Level | Generation Strategy                                |
| ---------------- | -------------------------------------------------- |
| Intern / Junior  | More fundamental and broader questions             |
| Mid              | Balanced fundamentals + practical scenarios        |
| Senior           | Architecture + system questions                    |

The prompt explicitly instructs the model to ask questions acoording to the level mentioned

This ensures difficulty scales naturally with seniority.

---

## Structured Output Schema

The backend enforces a strict JSON schema:

```json
{
  "technical_questions": ["string"],
  "behavioral_questions": ["string"],
  "evaluation_rubric": [
    {
      "criteria": "string",
      "weight": number,
      "what_to_look_for": "string"
    }
  ]
}
```

### Schema Guarantees

1. Two question categories:

   * Technical
   * Behavioral

2. Evaluation rubric:

   * Multiple criteria
   * Weight percentages must sum to 100
   * Clear guidance for interviewers

This structure enables:

* Consistent UI rendering
* Markdown and PDF export
* Future scoring automation

---

## Error Handling and Validation Approach

### Frontend Validation

Streamlit prevents invalid requests by checking:

* Job role must not be empty
* Backend connection errors handled gracefully
* Timeout errors handled with user feedback

### Backend Validation

Backend validates:

* JSON input structure
* Required fields presence
* Valid JSON output from LLM

If the LLM returns malformed output, the system:

* Returns error message instead of crashing
* Prevents invalid data reaching UI

### Resilience Measures

Handled failure cases:

* Backend server not running
* LLM timeout
* Unexpected API errors
* Invalid response format

This ensures stable demo and production-ready behavior.

---

## Known Limitations

1. LLM Variability
   Despite strict prompting, LLM outputs can vary slightly between runs.

2. No Persistent Storage
   Generated interview kits has no chat history across sessions or even within the session.

3. No Multi-Role Sessions
   The system currently supports one role per generation.

4. No Question Regeneration
   Individual question refinement is not implemented.

---

## Future Improvements

Planned enhancements include:

### Short-Term

* Add regeneration of individual questions
* Add multiple role support in one session
* Scoring templates mapped to the evaluation rubric

### Long-Term

* Add scoring interface for interviewers
* Add question difficulty tagging

