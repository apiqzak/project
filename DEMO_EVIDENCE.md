# Demo Evidence and Evaluation Log

Use this file to record screenshots, test cases, and presentation evidence.

## Test Environment

- Operating system:
- Python version:
- Main libraries:
  - MediaPipe
  - OpenCV
  - NumPy
  - python-telegram-bot
- Demo interface:
  - Local script
  - Telegram bot

## Test Case Summary

| Test ID | Exercise | Input Image | Interface | Expected Output | Result | Notes |
|---|---|---|---|---|---|---|
| T1 | Squat | `squat.jpg` | Local | Annotated image + squat report | Pending |  |
| T2 | Pushup | `pushup.jpg` | Local | Annotated image + pushup report | Pending |  |
| T3 | Pullup | `pullup.jpg` | Local | Annotated image + pullup report | Pending |  |
| T4 | Plank | user photo | Telegram | Annotated image + plank report | Pending |  |
| T5 | Invalid/unclear image | user photo | Telegram | No-pose or visibility warning | Pending |  |

## Local Demo Evidence

Command:

```powershell
python test_pose.py
```

Evidence to capture:

- Terminal input and output
- Generated `output.jpg`
- Annotated skeleton and feedback panel

Screenshot filenames:

- `evidence/local_squat_output.png`
- `evidence/local_pushup_output.png`
- `evidence/local_pullup_output.png`

## Telegram Demo Evidence

Command:

```powershell
$env:TELEGRAM_BOT_TOKEN="paste-your-token-here"
python telegram_bot.py
```

Telegram steps:

1. Send `/start`.
2. Select exercise.
3. Upload workout photo.
4. Save screenshot of annotated image response.
5. Save screenshot of text report response.

Screenshot filenames:

- `evidence/telegram_start.png`
- `evidence/telegram_exercise_selection.png`
- `evidence/telegram_annotated_result.png`
- `evidence/telegram_text_report.png`

## Evaluation Questions

Answer these after testing:

1. Did the system detect the body landmarks correctly?
2. Were the skeleton and angle labels visible?
3. Did the feedback match the visible posture?
4. Was the camera angle warning useful?
5. Did the output help the user decide what to adjust?
6. Did the system handle unclear or invalid input properly?

## Known Limitations Observed

- 

## Improvements Made After Testing

- 

## Final Demo Checklist

- Local analyzer works.
- Telegram bot starts.
- Bot receives image.
- Bot asks for or accepts exercise type.
- Bot sends annotated image.
- Bot sends text report.
- Limitations and ethical boundary are explained in presentation.
