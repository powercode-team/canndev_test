import json
import os
from custom_types import ClassificationResult

# Directory to store mock outputs
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SLACK_ALERTS_FILE = os.path.join(OUTPUT_DIR, "mock_slack_alerts.txt")
WEEKLY_DIGEST_FILE = os.path.join(OUTPUT_DIR, "weekly_digest.txt")
LOW_PRIORITY_LOG_FILE = os.path.join(OUTPUT_DIR, "low_priority_log.json")
FAILED_FILES_LOG = os.path.join(OUTPUT_DIR, "failed_files_log.json")
ALL_RESULTS_LOG = os.path.join(OUTPUT_DIR, "all_results_log.json")
all_results = []


def initialize_output_files():
    # Clear Slack alerts file
    with open(SLACK_ALERTS_FILE, "w", encoding="utf-8") as f:
        f.write("")

    # Clear weekly digest file
    with open(WEEKLY_DIGEST_FILE, "w", encoding="utf-8") as f:
        f.write("")

    # Clear low priority log file
    with open(LOW_PRIORITY_LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")

    # Clear failed files log
    with open(FAILED_FILES_LOG, "w", encoding="utf-8") as f:
        f.write("")


# Initialize storage for digest and low priority logs
digest_entries = []
low_priority_entries = []
failed_files = []


def handle_automation(result: ClassificationResult):
    classification = result.get("classification")

    if classification == "HIGH_PRIORITY":
        send_mock_slack_alert(result)
    elif classification == "MEDIUM_PRIORITY":
        add_to_weekly_digest(result)
    elif classification == "LOW_PRIORITY":
        log_low_priority(result)
    all_results.append(result)


def send_mock_slack_alert(result):
    reasoning_lines = result["reasoning"].split("; ")
    formatted_reasoning = "\n".join(f"- {line.strip()}" for line in reasoning_lines)
    message = (
        f"[Slack Alert] HIGH PRIORITY DOCUMENT\n"
        f"Source: {result['source_file']}\n"
        f"Score: {result['score']}\n"
        f"Reasoning:\n{formatted_reasoning}\n\n"
    )
    with open(SLACK_ALERTS_FILE, "a", encoding="utf-8") as f:
        f.write(message)


def add_to_weekly_digest(result):
    reasoning_lines = result["reasoning"].split("; ")
    formatted_reasoning = "\n".join(f"  - {line.strip()}" for line in reasoning_lines)
    entry = (
        f"- Source: {result['source_file']}\n"
        f"  Score: {result['score']}\n"
        f"  Reasoning:\n{formatted_reasoning}\n"
    )
    digest_entries.append(entry)


def log_low_priority(result):
    low_priority_entries.append(result)


def finalize_weekly_digest():
    if digest_entries:
        with open(WEEKLY_DIGEST_FILE, "w", encoding="utf-8") as f:
            f.write("WEEKLY DIGEST - MEDIUM PRIORITY DOCUMENTS:\n\n")
            for entry in digest_entries:
                f.write(entry + "\n")


def finalize_low_priority_log():
    if low_priority_entries:
        with open(LOW_PRIORITY_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(low_priority_entries, f, indent=2)


def log_failed_file(file_path, error_message):
    failed_files.append({"file": file_path, "error": str(error_message)})


def finalize_failed_files_log():
    if failed_files:
        with open(FAILED_FILES_LOG, "w", encoding="utf-8") as f:
            json.dump(failed_files, f, indent=2)


def finalize_all_results_log():
    if all_results:
        with open(ALL_RESULTS_LOG, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2)
