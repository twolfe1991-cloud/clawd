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
- **Schedule:** Every 2 hours (at the top of the hour: 00:00, 02:00, 04:00, 06:00, 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00 UTC)
- **Cron Expression:** `0 */2 * * *`
- **Job ID:** `79b0ee58-ac3c-49e8-8f4e-e2bd189440b4`
- **Script:** `word-of-the-day-check.py`
- **Target:** Telegram user 5404518130 (@Not_Wolfe)
- **Created:** 2026-02-03
- **Description:** Checks Gmail for Dictionary.com Word of the Day emails and sends formatted summary with word, pronunciation, definition, explanation, and example sentence via Telegram.
- **State file:** `.word_of_the_day_state.json` (tracks processed emails)

---

*Created: 2026-02-02*
*Updated: 2026-02-03*
