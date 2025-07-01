

# Cannabis Document Classifier - Methodology and Approach

## 1. Overview of the Approach

The goal of this project was to develop a rule-based document classification system that evaluates municipal documents for cannabis business relevance.

Our implementation uses a fully **regex-based keyword matching approach**, without involving any advanced NLP techniques or machine learning models.

The entire scoring system, including keyword categories, context modifiers, and classification thresholds, was designed strictly based on the scoring instructions provided in the client’s test assignment description.

Additionally, the system simulates automation workflows by generating mock Slack alerts, weekly digests, and log files corresponding to each priority.

## 2. Scoring Logic

### 2.1 Keyword Categories and Base Scores

Documents are evaluated against predefined High, Medium, and Low value keyword lists, each carrying different point values:

| Category | Points per Match |
|---|---|
| High Value Keywords | 10 |
| Medium Value Keywords | 5 |
| Low Value Keywords | 2 |

*(Keyword lists are fully configurable in `config.py`.)*

### 2.2 Context Modifiers

| Modifier | Points |
|---|---|
| Positive tone keywords (e.g., approved, passed) | +3 |
| Negative tone keywords (e.g., prohibited, banned) | -3 |
| Appearance in title or heading | +2 |

### 2.3 Date-Based Scoring

If a document mentions a specific date within the next 90 days, it receives an additional +5 points.

**Supported date formats include:**

- Month Day, Year (e.g., July 15, 2025)
- MM/DD/YYYY
- YYYY-MM-DD

> **Note:**  
> During testing, none of the client-provided documents contained dates within the 90-day window, so this rule did not affect the test results.  
> However, we validated the logic by temporarily expanding the date window.

### 2.4 Final Classification Thresholds

| Score | Classification |
|---|---|
| 70+ | HIGH_PRIORITY |
| 30-69 | MEDIUM_PRIORITY |
| 10-29 | LOW_PRIORITY |
| Below 10 | IRRELEVANT |

## 3. Automation Workflow Simulation

| Priority | Simulated Action | Output File |
|---|---|---|
| High | Immediate Slack Alert | `outputs/mock_slack_alerts.txt` |
| Medium | Weekly Digest Email | `outputs/weekly_digest.txt` |
| Low | JSON Log (No active alert) | `outputs/low_priority_log.json` |
| Irrelevant | No action | None |

Any processing errors (e.g., unreadable PDFs) are logged in:  
`outputs/failed_files_log.json`

## 4. Limitations of the Provided Document Set

1. **Document Format Coverage:**  
While the system supports both PDF and plain text files, all client-provided documents were in PDF format, except for one `.docx` file.  
To stay within scope, only `.pdf` files were processed for this assignment.

2. **Lack of Recent Dates:**  
No documents included dates within the 90-day scoring window.  
However, we tested the date logic manually by extending the window and confirmed that it works as expected.

## 5. Configurability

The system's core scoring logic, keywords, thresholds, and modifiers are all defined inside the `config.py` file, making it easy to:

- Add new keywords
- Adjust scoring weights
- Change classification thresholds
- Update the date window size
- Modify context modifiers

## 6. Possible Improvements / Future Enhancements

### 6.1 Score Normalization to Reduce False Positives

The current additive scoring model may overemphasize keyword frequency in longer documents.  
Future improvements could include score normalization, such as:

- Normalizing by document length
- Capping score contribution per keyword
- Using weighted averages or percentiles

### 6.2 Incorporating User Feedback Loop

To improve long-term accuracy:

- Track reviewer feedback on false positives and missed relevant documents
- Adjust scoring logic based on real-world use
- Potentially introduce supervised ML models for classification

### 6.3 Transition to NLP/LLM-Based Classification

For improved semantic understanding:

- Introduce NLP techniques (e.g., keyword embeddings, semantic similarity)
- Integrate pre-trained LLMs (e.g., GPT, BERT) for classification
- Apply NER (Named Entity Recognition) or topic modeling