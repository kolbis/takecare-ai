---
name: medication-reminder-symptom
description: Use when the user reports a symptom or feeling unwell. Delegate to Safety Officer for severity, then Nurse to notify caregiver and send escalation disclaimer. Never give medical advice.
---

# medication-reminder-symptom

## Overview

This skill handles the flow when the user reports a symptom or feeling unwell.

## Instructions

1. Delegate to the Safety Officer subagent to assess the reported symptom severity (use check_symptom_severity with the user_id and the user's reported text).

2. Delegate to the Nurse subagent to notify the caregiver (use notify_caregiver with reason "symptom_reported" and a short summary including severity).

3. The Nurse should send the standard escalation disclaimer to the user in their language (EN or HE) via send_whatsapp_message. The message must state that this is not medical advice, that the caregiver has been notified, and that the user should contact a doctor or caregiver if they feel unwell.

4. Do **not** give any medical advice, dosage advice, or treatment suggestions. Always escalate.
