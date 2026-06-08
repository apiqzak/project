# FitForm Assistant

FitForm Assistant is an OpenClaw-first computer vision skill for checking workout posture from an uploaded image or short video. A user uploads workout media in OpenClaw, enters a simple prompt such as `analyze squat`, and receives an annotated output plus a posture feedback report.

## Primary Workflow

```text
User uploads image/video + enters prompt in OpenClaw
-> OpenClaw FitForm skill
-> analyze_cli.py
-> test_pose.py image backend or video_analyzer.py video bridge
-> annotated image/video + text report + JSON output
```

OpenClaw is the main assignment demo interface. Telegram is kept only as an optional/legacy extra integration.

## Supported Exercises

- Squat
- Pushup
- Plank
- Pullup

## Target User

The target users are fitness beginners, physical education students, sports club members, and non-technical users who want quick visual feedback on basic workout form.

## Real-World Problem

Beginners often cannot tell whether their body alignment, joint angles, or exercise depth are correct from a photo or short clip. FitForm helps users inspect their form quickly using computer vision and gives simple corrective feedback.

## Computer Vision Method

The system uses MediaPipe Pose Landmarker for pose estimation. MediaPipe detects human body landmarks such as shoulders, elbows, hips, knees, ankles, and wrists. The project then calculates joint angles using vector geometry and applies rule-based exercise form checks.

Main CV concepts used:

- Image/video acquisition from uploaded or local files
- Person pose detection
- Keypoint and pose feature extraction
- Joint angle calculation
- Visual localization using skeleton overlays
- Media-to-report conversion

## Project Files

- `test_pose.py`: reusable CV/posture analysis backend
- `analyze_cli.py`: official integration bridge for OpenClaw and other tools
- `video_analyzer.py`: video frame sampling, annotation, and summary generation
- `skills/fitform/SKILL.md`: OpenClaw FitForm skill instructions
- `OPENCLAW_SKILL_PROMPT.md`: standalone OpenClaw prompt/reference
- `pose_landmarker.task`: MediaPipe pose model
- `requirements.txt`: Python dependencies
- `telegram_bot.py`: optional/legacy Telegram integration
- `WORKOUT_POSTURE_SKILL.md`: assignment skill design document
- `PHASE_5_TESTING_GUIDE.md`: testing and demo checklist
- `PRESENTATION_OUTLINE.md`: slide-by-slide presentation guide
- `DEMO_EVIDENCE.md`: evidence and test result log

## Setup

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

## Test The CLI Bridge

Run this from the project folder:

```powershell
python analyze_cli.py --input squat.jpg --exercise squat --media-type auto --output openclaw_output.jpg --report openclaw_report.txt --json openclaw_report.json
```

Expected output files:

- `openclaw_output.jpg`
- `openclaw_report.txt`
- `openclaw_report.json`

This confirms the OpenClaw integration bridge can call the posture analysis backend.

For video input, use a short clip first:

```powershell
python analyze_cli.py --input squat_video.mp4 --exercise squat --media-type auto --output openclaw_output.mp4 --report openclaw_report.txt --json openclaw_report.json --representative-frame openclaw_keyframe.jpg --frame-step 5 --max-seconds 30
```

Expected video output files:

- `openclaw_output.mp4`
- `openclaw_keyframe.jpg`
- `openclaw_report.txt`
- `openclaw_report.json`

## OpenClaw Demo Quick Start

1. Start or repair OpenClaw local mode if needed:

```powershell
openclaw onboard --mode local
```

2. Start the OpenClaw gateway:

```powershell
openclaw gateway --port 18789
```

Keep this terminal open.

3. Open the dashboard in another terminal:

```powershell
openclaw dashboard
```

4. Make sure the FitForm skill is available:

```powershell
openclaw skills check
```

If `fitform` does not appear, copy the workspace skill into OpenClaw's local skills folder:

```powershell
mkdir "$env:USERPROFILE\.openclaw\skills\fitform"
copy ".\skills\fitform\SKILL.md" "$env:USERPROFILE\.openclaw\skills\fitform\SKILL.md"
```

5. In OpenClaw, upload a clear workout image or short video and type:

```text
analyze squat
```

Other examples:

```text
analyze pushup
check my plank
analyze pullup
```

Expected response:

- annotated posture image/video
- representative frame for video input
- exercise type
- detected phase
- score
- main feedback
- safety note

## Local Backend Test

You can still run the backend directly:

```powershell
python test_pose.py
```

Enter an image filename such as:

```text
squat.jpg
```

Then choose the exercise:

```text
squat
```

The output is saved as:

```text
output.jpg
```

## Optional Legacy Telegram Integration

`telegram_bot.py` is kept as an optional extra interface. It is not the primary assignment workflow.

To use it, create a Telegram bot token using BotFather and set it as an environment variable:

```powershell
pip install -r requirements-telegram.txt
```

```powershell
$env:TELEGRAM_BOT_TOKEN="paste-your-token-here"
python telegram_bot.py
```

Never commit a real Telegram token. If a token was ever committed or shared, revoke/regenerate it in BotFather.

## Limitations

- Works best with one person in the image/video.
- Needs clear visibility of the full body.
- Image analysis checks one moment only.
- Video analysis samples selected frames, so very long or blurry videos may be slower or less accurate.
- Camera angle can affect landmark accuracy.
- The feedback is educational and should not replace a coach, trainer, doctor, or physiotherapist.

## Ethical Boundary

The system only analyzes exercise posture from visible body landmarks. It does not identify the person, judge attractiveness, infer health conditions, diagnose injuries, or provide medical advice.
