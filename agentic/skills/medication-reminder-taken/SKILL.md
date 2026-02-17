---
name: medication-reminder-taken
description: Use when the user confirms they took their medication (button "Taken" or equivalent). Coordinate Safety Officer then Nurse to check double-dose risk, then mark taken or escalate.
---

# medication-reminder-taken

## Overview

This skill handles the flow when the user confirms they have taken their medication.

## Instructions

1. The current reminder may have **one or multiple medications** (see current_reminder.medications in context). For each medication, delegate to the Safety Officer subagent to check double-dose risk. Pass user_id, medication_id, and slot_time (and dose_index if present) from each medication in current_reminder.medications.

2. If the Safety Officer returns **SAFE** for all medications: Delegate to the Nurse subagent to mark **all** doses as taken (call mark_dose_taken once per medication with user_id, medication_id, slot_time, dose_index). Then send the taken-confirmation message in the user's language via send_whatsapp_message.

3. If the Safety Officer returns **RISK** for any medication: Delegate to the Nurse subagent to notify the caregiver (use notify_caregiver with reason "double_dose_risk") and send the double-dose escalation message to the user. Do **not** mark any dose as taken.

4. Ensure all user-facing text is in the user's preferred language (EN or HE).
