# Demo Evidence and Evaluation Log

Use this file to record screenshots, test cases, and presentation evidence.

## Test Environment

- Operating system:
- Python version:
- Main libraries:
  - MediaPipe
  - OpenCV
  - NumPy
- Main demo interface:
  - OpenClaw FitForm skill
- Backend/integration:
  - `analyze_cli.py`
  - `test_pose.py`
  - `video_analyzer.py`
- Optional extra interface:
  - Telegram bot

## Test Case Summary

| Test ID | Exercise | Input Media | Interface | Expected Output | Result | Notes |
|---|---|---|---|---|---|---|
| T1 | Squat | `squat.jpg` | CLI bridge | Annotated image + squat report + JSON | Pass |  |
| T2 | Squat | uploaded photo | OpenClaw | Annotated image + squat report | Pass |  |
| T3 | Pushup | uploaded photo | OpenClaw | Annotated image + pushup report | Pending |  |
| T4 | Pullup | uploaded photo | OpenClaw | Annotated image + pullup report | Pending |  |
| T5 | Squat | short video | CLI bridge | Annotated video + keyframe + video report + JSON | Pending |  |
| T6 | Squat | uploaded short video | OpenClaw | Annotated video/keyframe + squat summary | Pending |  |
| T7 | Invalid/unclear media | uploaded file | OpenClaw | No-pose or visibility warning | Pending |  |

## CLI Bridge Evidence

Command:

```powershell
python analyze_cli.py --input squat.jpg --exercise squat --media-type auto --output openclaw_output.jpg --report openclaw_report.txt --json openclaw_report.json
```

Evidence to capture:

- Terminal report
- `openclaw_output.jpg`
- `openclaw_report.txt`
- `openclaw_report.json`

Video command:

```powershell
python analyze_cli.py --input squat_video.mp4 --exercise squat --media-type auto --output openclaw_output.mp4 --report openclaw_report.txt --json openclaw_report.json --representative-frame openclaw_keyframe.jpg --frame-step 5 --max-seconds 30
```

Video evidence to capture:

- Terminal summary
- `openclaw_output.mp4`
- `openclaw_keyframe.jpg`
- `openclaw_report.txt`
- `openclaw_report.json`

## OpenClaw Demo Evidence

OpenClaw is the main assignment demo interface.

OpenClaw steps:

1. Start OpenClaw gateway.
2. Open OpenClaw dashboard.
3. Upload a workout image or short video.
4. Type a simple prompt such as `analyze squat`.
5. Save screenshot of annotated image/video/keyframe response.
6. Save screenshot of text report response.

Screenshot filenames:

- `evidence/openclaw_start.png`
- `evidence/openclaw_upload.png`
- `evidence/openclaw_video_upload.png`
- `evidence/openclaw_annotated_result.png`
- `evidence/openclaw_video_result.png`
- `evidence/openclaw_text_report.png`

## Successful OpenClaw Result

Observed output:

```text
Analysis complete.

Exercise: squat
Phase: BOTTOM POSITION
Score: 3/5 checks passed

Main feedback:
- [WARN] Camera angle: DIAGONAL view detected, FRONT view recommended for squat
- [GOOD] Knee depth: Full squat depth achieved
- [GOOD] Hip hinge: Good forward lean
- [WARN] Back: Slight forward lean, keep chest up
- [GOOD] Knee symmetry: Both knees balanced

Annotated image: openclaw_output.jpg
Report file: openclaw_report.txt
JSON report: openclaw_report.json
```

Result:

```text
Pass
```

Conclusion:

OpenClaw successfully acted as the skill interface and called `analyze_cli.py`, which connected to the MediaPipe posture analysis backend in `test_pose.py`.

For video input, `analyze_cli.py` should route to `video_analyzer.py`, sample frames, reuse the same posture rules from `test_pose.py`, and generate an annotated video plus a representative frame.

## Optional Legacy Telegram Evidence

Telegram is optional/legacy and is not the main assignment workflow.

Command:

```powershell
$env:TELEGRAM_BOT_TOKEN="paste-your-token-here"
python telegram_bot.py
```

Never commit or share a real Telegram token. If a token was exposed, revoke/regenerate it in BotFather.

## Evaluation Questions

Answer these after testing:

1. Did the system detect the body landmarks correctly?
2. Were the skeleton and angle labels visible?
3. Did the feedback match the visible posture?
4. Was the camera angle warning useful?
5. Did the output help the user decide what to adjust?
6. Did the system handle unclear or invalid input properly?
7. For video, did the summary reflect the sampled frames clearly?

## Known Limitations Observed

-

## Improvements Made After Testing

-

## Final Demo Checklist

- CLI bridge works.
- OpenClaw FitForm skill works.
- OpenClaw receives or uses image/video input.
- OpenClaw asks for or accepts exercise type.
- OpenClaw returns annotated image/video or generated media path.
- OpenClaw returns text report.
- Limitations and ethical boundary are explained in presentation.
