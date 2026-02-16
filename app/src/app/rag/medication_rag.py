"""RAG for medication info or safe-response snippets. Mocked for now."""
from dataclasses import dataclass
from typing import List


@dataclass
class MedicationRAGResult:
    chunks: List[str]


class MedicationRAG:
    """Mock: return static disclaimer; no real retrieval."""

    def retrieve_safe_response_hints(self, query: str | None = None) -> MedicationRAGResult:
        return MedicationRAGResult(
            chunks=[
                "Do not give medical advice. Only remind and confirm.",
                "For symptoms or doubts, escalate to caregiver.",
            ]
        )

    def retrieve_medication_info(self, medication_name: str) -> MedicationRAGResult:
        return MedicationRAGResult(chunks=[f"Medication: {medication_name} (mocked)."])
