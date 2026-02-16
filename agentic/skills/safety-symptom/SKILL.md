---
name: safety-symptom
description: Assess reported symptom severity for escalation. Use check_symptom_severity. Return severity and whether to escalate. Do not give medical advice.
allowed-tools: check_symptom_severity
---

# safety-symptom

## Overview

This skill is used by the Safety Officer subagent to assess symptom severity when the user reports feeling unwell or describes a symptom.

## Instructions

1. Use check_symptom_severity with the user_id and the reported text (last message from the user).

2. Return the severity (e.g. low, medium, high, emergency) and a clear indication that the case should be escalated (notify caregiver). Do not give any medical advice or treatment suggestions.

3. Output only the assessment result so the orchestrator can delegate to the Nurse to notify the caregiver and send the standard disclaimer to the user.
