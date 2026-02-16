---
name: medication-reminder-snooze
description: Use when the user asks to be reminded later or taps "Remind later". Delegate to Nurse to snooze and send confirmation.
---

# medication-reminder-snooze

## Overview

This skill handles the flow when the user wants to snooze the current reminder.

## Instructions

1. Delegate to the Nurse subagent to snooze the current reminder (use snooze_dose with the reminder_id from context and a sensible snooze_minutes, e.g. 15).

2. The Nurse should send the snooze confirmation message in the user's language (EN or HE) via send_whatsapp_message.

3. Use the shared i18n phrasing for "I'll remind you again in [duration]."
