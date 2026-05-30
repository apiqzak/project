# Workout Posture Analysis Skill

## Skill Name

Workout Posture Analysis Assistant

## Target User

Fitness beginners, physical education students, sports club members, and non-technical users who want quick feedback on basic workout form from a photo.

## Real-World Problem

Many beginners practice exercises without knowing whether their joint alignment, body posture, or movement depth is correct. They may not have immediate access to a coach. This skill helps users inspect their workout form from an image and receive understandable feedback.

## Input Format

The skill accepts a workout image showing one person performing one supported exercise.

Supported exercises:

- Squat
- Pushup
- Plank
- Pullup

Accepted input sources:

- Local image file for `test_pose.py`
- Telegram photo upload for `telegram_bot.py`

The user must also provide or select the exercise type.

## Computer Vision or Image-Processing Method

The skill uses MediaPipe Pose Landmarker to detect human pose landmarks. These landmarks are normalized body keypoints such as shoulders, elbows, hips, knees, ankles, and wrists.

After landmark detection, the system performs:

- Pose keypoint extraction
- Joint angle calculation using three landmark points
- Camera angle estimation using shoulder and hip spacing
- Exercise phase detection
- Rule-based form analysis
- Skeleton and feedback visualization on the output image

## Step-by-Step Workflow

1. Receive image and exercise type.
2. Load the image using OpenCV or Telegram file download.
3. Run MediaPipe Pose Landmarker on the image.
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
12. Save and return the annotated image.
13. Return a structured text report with score, joint angles, feedback, and limitations.

## Output Format

The skill outputs:

- Annotated image with skeleton and joint angles
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
- The image does not show the full body
- The camera angle is not ideal for the selected exercise
- The photo captures a mid-repetition position
- The result may be affected by an angled shot

The system is designed to fail gracefully with a clear user-facing message instead of producing silent or confusing output.

## Ethical Boundary

The skill does not identify the person, judge body appearance, rate attractiveness, infer private attributes, diagnose injuries, or replace medical advice. It only evaluates visible exercise posture using body landmarks.

The feedback should be treated as educational guidance. Users with pain, injury, or medical concerns should consult a qualified coach, trainer, doctor, or physiotherapist.

## Why Computer Vision Is Needed

The input is visual body posture. Plain text processing cannot measure joint alignment or body angles from a workout photo. Pose estimation is needed to locate body joints, and image annotation is needed to show the user where the analysis comes from.

## Practical Recommendation

The output helps users decide what to adjust next, such as:

- Squat deeper
- Keep chest up
- Tighten core
- Tuck elbows closer
- Keep hips level
- Control swinging during pullups

This turns the visual input into actionable exercise feedback.
