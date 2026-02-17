from dataclasses import dataclass, field
from typing import List
from app.domain import value_objects


@dataclass
class MedicationEntity:
    id: value_objects.MedicationId
    name: value_objects.MedicationName
    description: value_objects.MedicationDescription

    warnings: List[str] = field(default_factory=list)
    side_effects: List[str] = field(default_factory=list)
    interactions: List[str] = field(default_factory=list)
    precautions: List[str] = field(default_factory=list)
    how_to_take: List[str] = field(default_factory=list)
    how_to_store: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Medication id cannot be empty.")

        if not self.name.strip():
            raise ValueError("Medication name cannot be empty.")

        if not self.description.strip():
            raise ValueError("Medication description cannot be empty.")

        # Normalize text fields
        self.name = self.name.strip()
        self.description = self.description.strip()

        # Clean list fields (remove empty entries & strip)
        self.warnings = self._clean_list(self.warnings)
        self.side_effects = self._clean_list(self.side_effects)
        self.interactions = self._clean_list(self.interactions)
        self.precautions = self._clean_list(self.precautions)
        self.how_to_take = self._clean_list(self.how_to_take)
        self.how_to_store = self._clean_list(self.how_to_store)

    def add_warning(self, warning: str) -> None:
        warning = warning.strip()
        if warning and warning not in self.warnings:
            self.warnings.append(warning)

    def remove_warning(self, warning: str) -> None:
        if warning in self.warnings:
            self.warnings.remove(warning)

    def add_side_effect(self, side_effect: str) -> None:
        side_effect = side_effect.strip()
        if side_effect and side_effect not in self.side_effects:
            self.side_effects.append(side_effect)

    def remove_side_effect(self, side_effect: str) -> None:
        if side_effect in self.side_effects:
            self.side_effects.remove(side_effect)

    def add_interaction(self, interaction: str) -> None:
        interaction = interaction.strip()
        if interaction and interaction not in self.interactions:
            self.interactions.append(interaction)

    def remove_interaction(self, interaction: str) -> None:
        if interaction in self.interactions:
            self.interactions.remove(interaction)

    def add_precaution(self, precaution: str) -> None:
        precaution = precaution.strip()
        if precaution and precaution not in self.precautions:
            self.precautions.append(precaution)

    def remove_precaution(self, precaution: str) -> None:
        if precaution in self.precautions:
            self.precautions.remove(precaution)

    def add_how_to_take(self, how_to_take: str) -> None:
        how_to_take = how_to_take.strip()
        if how_to_take and how_to_take not in self.how_to_take:
            self.how_to_take.append(how_to_take)

    def remove_how_to_take(self, how_to_take: str) -> None:
        if how_to_take in self.how_to_take:
            self.how_to_take.remove(how_to_take)

    def add_how_to_store(self, how_to_store: str) -> None:
        how_to_store = how_to_store.strip()
        if how_to_store and how_to_store not in self.how_to_store:
            self.how_to_store.append(how_to_store)

    def remove_how_to_store(self, how_to_store: str) -> None:
        if how_to_store in self.how_to_store:
            self.how_to_store.remove(how_to_store)

    @staticmethod
    def _clean_list(values: List[str]) -> List[str]:
        return list({v.strip() for v in values if v and v.strip()})
