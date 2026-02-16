---
name: medication-reminder-taken
description: Use when the user confirms they took their medication (button "Taken" or equivalent). Coordinate Safety Officer then Nurse to check double-dose risk, then mark taken or escalate.
---

# medication-reminder-taken

## Overview

This skill handles the flow when the user confirms they have taken their medication.

## Instructions

1. Delegate to the Safety Officer subagent to check double-dose risk for the current reminder. Pass the user_id, medication_id, and slot_time from the current reminder context.

2. If the Safety Officer returns **SAFE**: Delegate to the Nurse subagent to mark the dose as taken (use mark_dose_taken) and send the taken-confirmation message in the user's language via send_whatsapp_message.

3. If the Safety Officer returns **RISK**: Delegate to the Nurse subagent to notify the caregiver (use notify_caregiver with reason "double_dose_risk") and send the double-dose escalation message to the user. Do **not** mark the dose as taken.

4. Ensure all user-facing text is in the user's preferred language (EN or HE).
