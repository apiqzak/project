# Workout Posture Analysis Bot

This project is a practical computer vision skill for checking workout posture from a single image. A user sends or selects a workout photo, chooses the exercise type, and receives an annotated image plus a posture feedback report.

The project supports:

- Squat
- Pushup
- Plank
- Pullup

## Target User

The target users are fitness beginners, physical education students, sports club members, and non-technical users who want quick visual feedback on basic workout form.

## Real-World Problem

Beginners often cannot tell whether their body alignment, joint angles, or exercise depth are correct from a photo. This can make practice inefficient and may lead to poor habits. The system helps users inspect their form quickly using computer vision and gives simple corrective feedback.

## Visual Input

The input is a clear full-body workout image. The image should show one person and the main joints needed for analysis.

Recommended camera views:

- Squat: front view
- Pushup: side view
- Plank: side view
- Pullup: front view

## Computer Vision Method

The system uses MediaPipe Pose Landmarker for pose estimation. MediaPipe detects human body landmarks such as shoulders, elbows, hips, knees, and ankles. The project then calculates joint angles from these landmarks using vector geometry.

Main CV concepts used:

- Image acquisition from local files or Telegram uploads
- Person pose detection
- Keypoint and pose feature extraction
- Joint angle calculation
- Visual localization using skeleton overlays
- Image-to-report conversion

## System Workflow

1. User provides a workout image.
2. User selects the exercise type.
3. MediaPipe detects body landmarks.
4. The system calculates exercise-specific joint angles.
5. Rule-based logic evaluates form quality.
6. The image is annotated with skeleton, angle values, and feedback panel.
7. The user receives a visual result and text report.

## Output

The system produces:

- Annotated posture image
- Joint angle values
- Exercise phase detection
- Camera angle warning
- Form feedback
- Score showing how many checks passed

## Project Files

- `test_pose.py`: core pose detection, angle calculation, form analysis, and output generation
- `telegram_bot.py`: Telegram bot integration
- `pose_landmarker.task`: MediaPipe pose model
- `requirements.txt`: Python dependencies
- `WORKOUT_POSTURE_SKILL.md`: formal skill file for assignment requirements
- `PHASE_5_TESTING_GUIDE.md`: testing and presentation preparation checklist
- `PRESENTATION_OUTLINE.md`: slide-by-slide presentation guide
- `DEMO_EVIDENCE.md`: evidence template for screenshots and test cases

## Setup

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run Local Analyzer

```powershell
python test_pose.py
```

Then enter an image filename such as:

```text
squat.jpg
```

Choose the exercise:

```text
squat
```

The output is saved as:

```text
output.jpg
```

## Run Telegram Bot

Create a Telegram bot token using BotFather, then run:

```powershell
$env:TELEGRAM_BOT_TOKEN="paste-your-token-here"
python telegram_bot.py
```

In Telegram:

1. Send `/start`
2. Choose an exercise or send `/set squat`
3. Upload a clear full-body workout photo
4. Receive the annotated image and text report

## Limitations

- Works best with one person in the image.
- Needs clear visibility of the full body.
- Single-image analysis cannot evaluate motion quality across a full repetition.
- Camera angle can affect landmark accuracy.
- The feedback is educational and should not replace a coach, trainer, doctor, or physiotherapist.

## Ethical Boundary

The system only analyzes exercise posture from visible body landmarks. It does not identify the person, judge attractiveness, infer health conditions, diagnose injuries, or provide medical advice.
