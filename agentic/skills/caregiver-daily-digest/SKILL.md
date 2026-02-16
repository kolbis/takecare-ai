---
name: caregiver-daily-digest
description: Build and send the daily digest for the caregiver. Use tools to get events for the day (missed, snoozes, escalations), format a short summary, and call notify_caregiver.
---

# caregiver-daily-digest

## Overview

This skill is used by the Caregiver Summarizer subagent to produce and send a daily digest to the caregiver.

## Instructions

1. Use the available tools to retrieve events for the given user and date: missed doses, snoozes, escalations, and any "not sure" resolutions.

2. Format a short, readable summary (e.g. bullet points or a short paragraph) suitable for the caregiver.

3. Call notify_caregiver with reason "daily_digest" and the summary as the body. Include user_id and date in the summary.

4. Do not include medical advice. This is an informational digest only.
