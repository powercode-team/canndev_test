


# Cannabis Document Classifier - Test Assignment

## Overview
This project implements a rule-based document classification system to score municipal documents for cannabis business relevance and simulate automation workflows based on priority.

## Requirements
- Python 3.8+
- Packages listed in `requirements.txt`

## Setup

```bash
# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Pipeline

```bash
python main.py
```

## Outputs

After running, the following mock outputs will be saved in the `outputs/` folder:

- `mock_slack_alerts.txt` – High priority alerts
- `weekly_digest.txt` – Medium priority digest
- `low_priority_log.json` – Low priority logs
- `failed_files_log.json` – Any documents that failed to process

## Notes

- Input documents should be placed under the `data/` folder.
- Supported input formats: `.pdf`, `.txt`
- Configuration settings (keywords, scoring thresholds, etc.) are in `config.py`.
