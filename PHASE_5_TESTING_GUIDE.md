# Phase 5 Testing, Refinement, and Presentation Prep

Related documents:

- `README.md`: project overview and setup
- `WORKOUT_POSTURE_SKILL.md`: formal skill file for assignment requirements
- `PRESENTATION_OUTLINE.md`: slide-by-slide presentation plan
- `DEMO_EVIDENCE.md`: testing evidence and screenshot log

## Local Analyzer Test

Run the original analyzer flow:

```powershell
python test_pose.py
```

Try each sample image:

- `squat.jpg` with `squat`
- `pushup.jpg` with `pushup`
- `pullup.jpg` with `pullup`
- `workout.jpg` with the matching exercise you want to demonstrate

Expected result:

- `output.jpg` is generated
- pose skeleton and joint angles are visible
- side panel shows exercise, phase, score, joint angles, and feedback

## Telegram Bot Test

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a bot token using Telegram BotFather, then run:

```powershell
$env:TELEGRAM_BOT_TOKEN="paste-your-token-here"
python telegram_bot.py
```

In Telegram:

1. Send `/start`
2. Choose an exercise or send `/set squat`
3. Send a clear full-body workout photo
4. Confirm the bot replies with an annotated image and text report

You can also send the photo with a caption:

```text
squat
```

## Refinement Checklist

- Use clear full-body photos with all major joints visible.
- Use front view for `squat` and `pullup`.
- Use side view for `pushup` and `plank`.
- Keep one person in the photo.
- Test at least one good-form and one bad-form image for each exercise.
- Save 2-3 successful Telegram screenshots for the presentation.

## Presentation Flow

1. Show Phase 1-3 result from `test_pose.py`.
2. Explain the four supported exercises and joint angles used.
3. Run `telegram_bot.py`.
4. Send a workout photo in Telegram.
5. Show annotated image, report, score, and form feedback.
6. Mention limitations: single-image analysis, camera angle sensitivity, and full-body visibility requirement.

## Submission Readiness Checklist

- `WORKOUT_POSTURE_SKILL.md` explains skill name, target user, real problem, input, CV method, workflow, output, limitations, and ethical boundary.
- `README.md` explains how to install and run the local analyzer and Telegram bot.
- `PRESENTATION_OUTLINE.md` follows the 10-slide structure from the instruction PDF.
- `DEMO_EVIDENCE.md` contains test cases and screenshot placeholders.
- Telegram demo has been tested with at least one real photo.
- Annotated image output is shown in the presentation.
