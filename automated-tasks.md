# Automated Tasks

This file tracks all recurring automated tasks and cron jobs.

## Luxury Automotive News Daily
- **Schedule:** Monday to Friday at 08:30 UTC
- **Cron Expression:** `30 8 * * 1-5`
- **Job ID:** `f1ddba89-69cf-497b-8b0b-dc2ec0bf790f`
- **Target:** Telegram user 5404518130 (@Not_Wolfe)
- **Created:** 2026-02-02
- **Description:** Daily luxury automotive news summary focused on the luxury car sector (Bentley, Rolls-Royce, Ferrari, Lamborghini, Aston Martin, Porsche, Mercedes, etc.), including electric luxury developments, market trends, and industry news.

---

## Word of the Day Check
- **Script:** `word-of-the-day-check.py`
- **Target:** Telegram user 5404518130 (@Not_Wolfe)
- **Created:** 2026-02-03
- **Description:** Checks Gmail for Dictionary.com Word of the Day emails and sends formatted summary with word, pronunciation, definition, explanation, and example sentence via Telegram.
- **State file:** `.word_of_the_day_state.json` (tracks processed emails)
- **Frequency:** To be configured via cron (suggested: every 2 hours during day)

---

*Created: 2026-02-02*
*Updated: 2026-02-03*
