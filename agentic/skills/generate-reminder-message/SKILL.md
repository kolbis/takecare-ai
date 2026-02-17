---
name: generate-reminder-message
description: Use when sending a scheduled medication reminder (no user message). Delegate to Nurse to get medication info, format in user language (EN/HE), attach quick-reply buttons, and send.
---

# generate-reminder-message

## Overview

This skill is used when the system needs to send a scheduled medication reminder to the user (e.g. at 08:00 for their morning dose).

## Instructions

1. Delegate to the Nurse subagent to get the current medication events for the user (use get_medication_event with user_id). The tool returns an **events** list; there may be one or multiple medications for the same slot.

2. Format the reminder message in the user's preferred language (EN or HE):
   - **Single medication**: "Time for your [medication_name]. Did you take it?" (EN) / "זמן ל-[medication_name]. נטלת?" (HE).
   - **Multiple medications**: Use the count and list: "You have N medications to take: [medication_list]. Did you take them?" (e.g. "You have 3 medications to take: Aspirin, Ibuprofen, and Vitamin D. Did you take them?"). Build medication_list as "X, Y, and Z" (comma-separated with " and " before the last item).

3. Attach quick-reply buttons in the user's language: Taken (נטלתי), Remind later (תזכיר אחר כך), Not sure (לא בטוח).

4. Send the message via send_whatsapp_message with the formatted text and buttons.

5. Return the response_text and response_buttons for the graph to pass to Finalize.
