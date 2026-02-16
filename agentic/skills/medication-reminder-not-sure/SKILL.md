---
name: medication-reminder-not-sure
description: Use when the user is unsure if they took the medication. Delegate to Nurse to send a clarification question; do not mark as taken until resolved.
---

# medication-reminder-not-sure

## Overview

This skill handles the flow when the user is not sure whether they took their medication.

## Instructions

1. Delegate to the Nurse subagent to send a short clarification question in the user's language (EN or HE).

2. The question should ask when they might have taken it (e.g. this morning or earlier) and offer the option "I didn't take it."

3. Optionally attach quick-reply buttons such as "This morning", "Earlier", "I didn't take it" (in the user's language).

4. Do **not** mark the dose as taken. Wait for the user's next message to resolve.

5. Use send_whatsapp_message for the clarification. Do not give medical advice.
