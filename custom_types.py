from typing import TypedDict, List


class ClassificationResult(TypedDict):
    classification: str
    score: int
    reasoning: str
    key_phrases: List[str]
    recommended_action: str
    source_file: str
