---
name: safety-double-dose
description: Evaluate whether marking the current dose as taken would be a double-dose risk. Use check_double_dose and get_medication_event. Return only SAFE or RISK and a short reason. No user-facing message text.
allowed-tools: check_double_dose, get_medication_event
---

# safety-double-dose

## Overview

This skill is used by the Safety Officer subagent to evaluate double-dose risk before the user's "taken" confirmation is recorded.

## Instructions

1. Use get_medication_event with the user_id (and optional reminder/event context) to obtain the current slot events. The result includes an **events** list; each event has medication_id, slot_time, dose_index. When the reminder has multiple medications, this skill may be invoked **once per medication** by the orchestrator.

2. For the medication you are evaluating, call check_double_dose with user_id, medication_id, slot_time, and within_hours (e.g. 24.0).

3. Return a structured result: **SAFE** or **RISK**, and if RISK include the reason string from the tool. Do not generate any user-facing message text. The main agent or Nurse will handle user messaging.

4. Output only the evaluation result so the orchestrator can decide whether to mark the dose as taken or to escalate.
