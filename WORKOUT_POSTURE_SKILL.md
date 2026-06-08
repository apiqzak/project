# Workout Posture Analysis Skill

## Skill Name

Workout Posture Analysis Assistant

## Target User

Fitness beginners, physical education students, sports club members, and non-technical users who want quick feedback on basic workout form from a photo or short video.

## Real-World Problem

Many beginners practice exercises without knowing whether their joint alignment, body posture, or movement depth is correct. They may not have immediate access to a coach. This skill helps users inspect their workout form from an image or sampled video frames and receive understandable feedback.

## Input Format

The skill accepts a workout image or short video showing one person performing one supported exercise.

Supported exercises:

- Squat
- Pushup
- Plank
- Pullup

Accepted input sources:

- OpenClaw uploaded image/video or file path through `analyze_cli.py` (primary workflow)
- Local image file for `test_pose.py` (backend/debug workflow)
- Telegram photo upload for `telegram_bot.py` (optional legacy extra)

The user must also provide or select the exercise type.

## OpenClaw Tool Interface

OpenClaw is the main user interface for the assignment demo. It should use `skills/fitform/SKILL.md` or `OPENCLAW_SKILL_PROMPT.md` as the skill instructions and call `analyze_cli.py` as the backend tool bridge.

Preferred flow:

```text
User uploads image/video + enters prompt in OpenClaw
-> FitForm skill
-> analyze_cli.py
-> test_pose.py or video_analyzer.py
-> annotated image/video + report + JSON
```

Example command:

```cmd
python analyze_cli.py --input "squat.jpg" --exercise "squat" --media-type auto --output "openclaw_output.jpg" --report "openclaw_report.txt" --json "openclaw_report.json"
```

Example video command:

```cmd
python analyze_cli.py --input "squat_video.mp4" --exercise "squat" --media-type auto --output "openclaw_output.mp4" --report "openclaw_report.txt" --json "openclaw_report.json" --representative-frame "openclaw_keyframe.jpg" --frame-step 5 --max-seconds 30
```

The OpenClaw response should return or display the annotated image, annotated video, or representative keyframe and summarize the generated text report.

## Computer Vision or Image-Processing Method

The skill uses MediaPipe Pose Landmarker to detect human pose landmarks. These landmarks are normalized body keypoints such as shoulders, elbows, hips, knees, ankles, and wrists.

After landmark detection, the system performs:

- Pose keypoint extraction
- Joint angle calculation using three landmark points
- Camera angle estimation using shoulder and hip spacing
- Exercise phase detection
- Rule-based form analysis
- Skeleton and feedback visualization on the output image or sampled video frames

## Step-by-Step Workflow

1. Receive image/video and exercise type.
2. Load the media using OpenCV through the CLI bridge.
3. Run MediaPipe Pose Landmarker on the image or sampled video frame.
4. If no pose is detected, return a full-body visibility warning.
5. Extract body landmarks for the first detected person.
6. Detect approximate camera angle.
7. Calculate exercise-specific joint angles:
   - Squat: knees, hip hinge, back alignment
   - Pushup: elbows, body line, elbow flare
   - Plank: body line, hip position, shoulder angle
   - Pullup: elbows, shoulder elevation, body alignment
8. Detect exercise phase, such as bottom position, top position, hold position, or mid-rep.
9. Compare angles against rule-based thresholds.
10. Generate feedback messages and pass/fail status.
11. Draw skeleton, joint angle labels, and feedback panel.
12. Save and return the annotated image or annotated video.
13. For video, save an optional representative annotated frame.
14. Return a structured text report with score, joint angles, feedback, and limitations.

## Output Format

The skill outputs:

- Annotated image or video with skeleton and joint angles
- Representative annotated frame for video input, if generated
- Exercise name
- Detected phase
- Camera angle recommendation
- Joint angle table
- Feedback list
- Score such as `3/5 checks passed`
- Limitation or visibility warning when needed

Example output summary:

```text
Exercise: SQUAT
Phase: BOTTOM POSITION
Score: 4/5 checks passed

Joint Angles:
- Left Knee: 95 deg
- Right Knee: 101 deg
- Hip Hinge: 82 deg
- Back Alignment: 158 deg

Feedback:
- [GOOD] Camera angle: FRONT view, ideal for squat
- [GOOD] Knee depth: Full squat depth achieved
- [WARN] Knee symmetry: Uneven, check for knee caving
```

## Limitation Handling

The skill handles limitations by giving warnings when:

- No pose is detected
- The image/video does not show the full body
- The camera angle is not ideal for the selected exercise
- The photo captures a mid-repetition position
- The video has frames where no pose is detected
- The video is long, blurry, or sampled rather than analyzed frame-by-frame
- The result may be affected by an angled shot

The system is designed to fail gracefully with a clear user-facing message instead of producing silent or confusing output.

## Ethical Boundary

The skill does not identify the person, judge body appearance, rate attractiveness, infer private attributes, diagnose injuries, or replace medical advice. It only evaluates visible exercise posture using body landmarks.

The feedback should be treated as educational guidance. Users with pain, injury, or medical concerns should consult a qualified coach, trainer, doctor, or physiotherapist.

## Why Computer Vision Is Needed

The input is visual body posture. Plain text processing cannot measure joint alignment or body angles from a workout photo or video. Pose estimation is needed to locate body joints, and media annotation is needed to show the user where the analysis comes from.

## Practical Recommendation

The output helps users decide what to adjust next, such as:

- Squat deeper
- Keep chest up
- Tighten core
- Tuck elbows closer
- Keep hips level
- Control swinging during pullups

This turns the visual input into actionable exercise feedback.
