---
name: generate-reminder-message
description: Use when sending a scheduled medication reminder (no user message). Delegate to Nurse to get medication info, format in user language (EN/HE), attach quick-reply buttons, and send.
---

# generate-reminder-message

## Overview

This skill is used when the system needs to send a scheduled medication reminder to the user (e.g. at 08:00 for their morning dose).

## Instructions

1. Delegate to the Nurse subagent to get the current medication event for the user (use get_medication_event with user_id).

2. Using the medication name and slot from the event, format the reminder message in the user's preferred language (EN or HE). Example EN: "Time for your [medication_name]. Did you take it?" Example HE: "זמן ל-[medication_name]. נטלת?"

3. Attach quick-reply buttons in the user's language: Taken (נטלתי), Remind later (תזכיר אחר כך), Not sure (לא בטוח).

4. Send the message via send_whatsapp_message with the formatted text and buttons.

5. Return the response_text and response_buttons for the graph to pass to Finalize.
