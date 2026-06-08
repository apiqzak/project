# Phase 5 Testing, Refinement, and Presentation Prep

Related documents:

- `README.md`: project overview and setup
- `WORKOUT_POSTURE_SKILL.md`: formal skill file for assignment requirements
- `OPENCLAW_SKILL_PROMPT.md`: OpenClaw skill prompt and command workflow
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

## OpenClaw Bridge Test

Run the command-line bridge that OpenClaw will call for image input:

```powershell
python analyze_cli.py --input squat.jpg --exercise squat --media-type auto --output openclaw_output.jpg --report openclaw_report.txt --json openclaw_report.json
```

Expected result:

- `openclaw_output.jpg` is generated
- `openclaw_report.txt` contains the readable report
- `openclaw_report.json` contains structured output
- The terminal prints the same report

Run the bridge for video input with a short clip:

```powershell
python analyze_cli.py --input squat_video.mp4 --exercise squat --media-type auto --output openclaw_output.mp4 --report openclaw_report.txt --json openclaw_report.json --representative-frame openclaw_keyframe.jpg --frame-step 5 --max-seconds 30
```

Expected result:

- `openclaw_output.mp4` is generated
- `openclaw_keyframe.jpg` is generated when at least one representative frame is available
- `openclaw_report.txt` contains the readable video summary
- `openclaw_report.json` contains structured video output

## OpenClaw Skill Demo Test

After installing or copying the FitForm skill into OpenClaw, upload a clear workout image or short video and use a simple prompt in the OpenClaw dashboard:

```text
analyze squat
```

Expected result:

- OpenClaw runs `analyze_cli.py`
- `openclaw_output.jpg` is created for image input, or `openclaw_output.mp4` is created for video input
- `openclaw_keyframe.jpg` is created for video input when possible
- `openclaw_report.txt` is created
- `openclaw_report.json` is created
- OpenClaw replies with exercise, phase, score, main feedback, and ethical note

Successful sample result:

```text
Exercise: squat
Phase: BOTTOM POSITION
Score: 3/5 checks passed
```

## Refinement Checklist

- Use clear full-body photos with all major joints visible.
- Use short videos first, ideally under 30 seconds for the demo.
- Use front view for `squat` and `pullup`.
- Use side view for `pushup` and `plank`.
- Keep one person in the image/video.
- Test at least one good-form and one bad-form image for each exercise.
- Test at least one short video for one supported exercise.
- Save 2-3 successful OpenClaw screenshots for the presentation.

## Presentation Flow

1. Show Phase 1-3 result from `test_pose.py`.
2. Explain the four supported exercises and joint angles used.
3. Open the OpenClaw dashboard.
4. Upload a workout photo or short video and type a simple prompt such as `analyze squat`.
5. Show annotated image/video, report, score, and form feedback from OpenClaw.
6. Mention limitations: image analysis checks one moment, video analysis samples frames, camera angle sensitivity, and full-body visibility requirement.

## Submission Readiness Checklist

- `WORKOUT_POSTURE_SKILL.md` explains skill name, target user, real problem, input, CV method, workflow, output, limitations, and ethical boundary.
- `OPENCLAW_SKILL_PROMPT.md` explains how OpenClaw should call `analyze_cli.py`.
- `README.md` explains how to install and run the OpenClaw-first workflow.
- `PRESENTATION_OUTLINE.md` follows the 10-slide structure from the instruction PDF.
- `DEMO_EVIDENCE.md` contains test cases and screenshot placeholders.
- OpenClaw demo has been tested with at least one real photo.
- OpenClaw video path has been tested with at least one short clip if available.
- Annotated image/video output is shown in the presentation.

## Optional Legacy Telegram Test

Telegram is kept as an optional extra interface, not the main assignment demo.

```powershell
$env:TELEGRAM_BOT_TOKEN="paste-your-token-here"
python telegram_bot.py
```

Never commit or share a real Telegram token. If one was exposed, revoke/regenerate it in BotFather.
