import cv2
import mediapipe as mp
import numpy as np

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return round(angle, 2)

def get_keypoint(landmarks, index):
    lm = landmarks[index]
    return [lm.x, lm.y]

def get_pixel(landmarks, index, w, h):
    lm = landmarks[index]
    return (int(lm.x * w), int(lm.y * h))

# ─────────────────────────────────────────
# DRAWING FUNCTIONS
# ─────────────────────────────────────────

def draw_skeleton(image, landmarks, w, h, status_map):
    """
    Draw skeleton with color-coded joints based on feedback status.
    status_map: dict of keypoint_index -> 'good'/'warning'/'bad'
    """
    connections = [
        (11, 12),           # shoulders
        (11, 13), (13, 15), # left arm
        (12, 14), (14, 16), # right arm
        (11, 23), (12, 24), # torso sides
        (23, 24),           # hips
        (23, 25), (25, 27), # left leg
        (24, 26), (26, 28), # right leg
    ]

    for start, end in connections:
        p1 = get_pixel(landmarks, start, w, h)
        p2 = get_pixel(landmarks, end, w, h)
        cv2.line(image, p1, p2, (200, 200, 200), 2)

    for i in range(33):
        px, py = get_pixel(landmarks, i, w, h)
        s = status_map.get(i, "neutral")
        color = (0, 255, 100) if s == "good" else \
                (0, 200, 255) if s == "warning" else \
                (0, 60, 255)  if s == "bad" else \
                (180, 180, 180)
        cv2.circle(image, (px, py), 7, color, -1)
        cv2.circle(image, (px, py), 7, (255, 255, 255), 1)

def draw_angle_on_joint(image, landmarks, a, b, c, w, h, offset=(8, -8)):
    angle = calculate_angle(
        get_keypoint(landmarks, a),
        get_keypoint(landmarks, b),
        get_keypoint(landmarks, c)
    )
    px, py = get_pixel(landmarks, b, w, h)
    cv2.putText(image, f"{angle:.0f}deg",
                (px + offset[0], py + offset[1]),  # use offset
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 1)
    return angle

def draw_angles_for_exercise(image, landmarks, exercise, w, h):
    """Draw relevant joint angles depending on exercise"""
    if exercise == "squat":
        draw_angle_on_joint(image, landmarks, 23, 25, 27, w, h)  # left knee
        draw_angle_on_joint(image, landmarks, 24, 26, 28, w, h)  # right knee
        draw_angle_on_joint(image, landmarks, 11, 23, 25, w, h)  # hip hinge
        draw_angle_on_joint(image, landmarks, 11, 23, 27, w, h, offset=(8, 20))

    elif exercise == "pushup":
        draw_angle_on_joint(image, landmarks, 11, 13, 15, w, h)  # left elbow
        draw_angle_on_joint(image, landmarks, 12, 14, 16, w, h)  # right elbow
        draw_angle_on_joint(image, landmarks, 11, 23, 27, w, h)  # body line
        draw_angle_on_joint(image, landmarks, 13, 11, 23, w, h)  # elbow flare

    elif exercise == "plank":
        draw_angle_on_joint(image, landmarks, 11, 23, 27, w, h)  # body line
        draw_angle_on_joint(image, landmarks, 11, 23, 25, w, h)  # hip position
        draw_angle_on_joint(image, landmarks, 13, 11, 23, w, h)  # shoulder angle

    elif exercise == "pullup":
        draw_angle_on_joint(image, landmarks, 11, 13, 15, w, h)  # left elbow
        draw_angle_on_joint(image, landmarks, 12, 14, 16, w, h)  # right elbow
        draw_angle_on_joint(image, landmarks, 13, 11, 23, w, h)  # shoulder elevation
        draw_angle_on_joint(image, landmarks, 11, 23, 27, w, h)  # body alignment

def build_status_map(exercise, angles, statuses):
    """
    Map joint indices to their status for color-coded skeleton.
    Returns dict: { keypoint_index: 'good'/'warning'/'bad' }
    """
    mapping = {}

    if exercise == "squat":
        knee_status = statuses[0]   # left knee
        hip_status  = statuses[1]   # hip hinge
        back_status = statuses[2]   # back alignment
        mapping.update({
            25: knee_status, 27: knee_status,  # left knee/ankle
            26: knee_status, 28: knee_status,  # right knee/ankle
            23: hip_status,  24: hip_status,   # hips
            11: back_status, 12: back_status,  # shoulders
        })

    elif exercise == "pushup":
        elbow_status = statuses[0]  # elbow bend
        body_status  = statuses[1]  # body line
        flare_status = statuses[2]  # elbow flare
        mapping.update({
            13: elbow_status, 15: elbow_status,  # left elbow/wrist
            14: elbow_status, 16: elbow_status,  # right elbow/wrist
            23: body_status,  24: body_status,   # hips
            11: flare_status, 12: flare_status,  # shoulders
        })

    elif exercise == "plank":
        body_status     = statuses[0]  # body line
        hip_status      = statuses[1]  # hip position
        shoulder_status = statuses[2]  # shoulder angle
        mapping.update({
            23: hip_status,      24: hip_status,      # hips
            25: body_status,     27: body_status,     # knees/ankles
            11: shoulder_status, 12: shoulder_status, # shoulders
        })

    elif exercise == "pullup":
        pull_status     = statuses[0]  # pull height
        shoulder_status = statuses[2]  # shoulder elevation
        body_status     = statuses[3]  # body alignment
        mapping.update({
            13: pull_status,     15: pull_status,     # left elbow/wrist
            14: pull_status,     16: pull_status,     # right elbow/wrist
            11: shoulder_status, 12: shoulder_status, # shoulders
            23: body_status,     24: body_status,     # hips
        })

    return mapping

def draw_feedback_panel(image, exercise, feedback, angles, statuses, h, w):
    """Draw dark side panel with angles, feedback, and overall score"""
    panel_w = 340
    panel = np.zeros((h, panel_w, 3), dtype=np.uint8)
    panel[:] = (25, 25, 25)

    def put(text, x, y, color, scale=0.45, thickness=1):
        cv2.putText(panel, text, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)

    def line(y):
        cv2.line(panel, (10, y), (panel_w - 10, y), (60, 60, 60), 1)

    # Header
    put("POSTURE ANALYSIS", 10, 30, (0, 210, 255), 0.6, 2)
    put(f"Exercise: {exercise.upper()}", 10, 55, (200, 200, 200), 0.5)
    line(65)

    # Joint angles section
    y = 85
    put("JOINT ANGLES", 10, y, (150, 150, 150), 0.4)
    y += 20
    for joint, angle in angles.items():
        put(f"  {joint}: {angle}deg", 10, y, (255, 220, 80), 0.42)
        y += 20
    line(y + 5)
    y += 22

    # Feedback section
    put("FEEDBACK", 10, y, (150, 150, 150), 0.4)
    y += 20
    for i, fb in enumerate(feedback):
        s = statuses[i] if i < len(statuses) else "neutral"
        color = (0, 220, 100)  if s == "good"    else \
                (0, 200, 255)  if s == "warning"  else \
                (60, 80, 255)

        # Word wrap
        words = fb.split()
        line_text = ""
        for word in words:
            if len(line_text + word) < 38:
                line_text += word + " "
            else:
                put(line_text, 10, y, color)
                y += 17
                line_text = word + " "
        if line_text:
            put(line_text, 10, y, color)
            y += 20

    line(y + 5)
    y += 20

    # Overall score
    good    = sum(1 for s in statuses if s == "good")
    warning = sum(1 for s in statuses if s == "warning")
    bad     = sum(1 for s in statuses if s == "bad")
    total   = len(statuses)

    put(f"Score: {good}/{total} checks passed", 10, y, (200, 200, 200), 0.45)
    y += 20

    if bad == 0 and warning == 0:
        result, color = "EXCELLENT FORM", (0, 255, 100)
    elif bad == 0:
        result, color = "GOOD — MINOR ADJUSTMENTS", (0, 200, 255)
    elif bad <= total // 2:
        result, color = "NEEDS IMPROVEMENT", (0, 140, 255)
    else:
        result, color = "POOR FORM — REVIEW NEEDED", (0, 60, 255)

    put(result, 10, y + 20, color, 0.5, 2)

    combined = np.hstack([image, panel])
    return combined

# ─────────────────────────────────────────
# EXERCISE ANALYSIS FUNCTIONS
# ─────────────────────────────────────────

def analyze_squat(landmarks):
    feedback, status = [], []

    left_knee = calculate_angle(
        get_keypoint(landmarks, 23),
        get_keypoint(landmarks, 25),
        get_keypoint(landmarks, 27)
    )
    right_knee = calculate_angle(
        get_keypoint(landmarks, 24),
        get_keypoint(landmarks, 26),
        get_keypoint(landmarks, 28)
    )
    hip_hinge = calculate_angle(
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 23),
        get_keypoint(landmarks, 25)
    )
    back_alignment = calculate_angle(
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 23),
        get_keypoint(landmarks, 27)
    )

    if left_knee <= 90:
        feedback.append("✅ Knee depth: Full squat depth achieved")
        status.append("good")
    elif left_knee <= 120:
        feedback.append("⚠️ Knee depth: Slightly shallow — squat deeper")
        status.append("warning")
    else:
        feedback.append("❌ Knee depth: Too shallow — hip crease must go below knees")
        status.append("bad")

    if 45 <= hip_hinge <= 100:
        feedback.append("✅ Hip hinge: Good forward lean")
        status.append("good")
    elif hip_hinge < 45:
        feedback.append("⚠️ Hip hinge: Leaning too far forward")
        status.append("warning")
    else:
        feedback.append("❌ Hip hinge: Not hinging enough at hips")
        status.append("bad")

    if 160 <= back_alignment <= 180:
        feedback.append("✅ Back: Neutral spine maintained")
        status.append("good")
    else:
        feedback.append("❌ Back: Keep chest up and spine straight")
        status.append("bad")

    if abs(left_knee - right_knee) <= 15:
        feedback.append("✅ Knee symmetry: Both knees balanced")
        status.append("good")
    else:
        feedback.append("⚠️ Knee symmetry: Uneven — check for knee caving")
        status.append("warning")

    return feedback, status, {
        "Left Knee": left_knee,
        "Right Knee": right_knee,
        "Hip Hinge": hip_hinge,
        "Back Alignment": back_alignment
    }


def analyze_pushup(landmarks):
    feedback, status = [], []

    left_elbow = calculate_angle(
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 13),
        get_keypoint(landmarks, 15)
    )
    right_elbow = calculate_angle(
        get_keypoint(landmarks, 12),
        get_keypoint(landmarks, 14),
        get_keypoint(landmarks, 16)
    )
    body_line = calculate_angle(
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 23),
        get_keypoint(landmarks, 27)
    )
    elbow_flare = calculate_angle(
        get_keypoint(landmarks, 13),
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 23)
    )

    if 70 <= left_elbow <= 90:
        feedback.append("✅ Elbow bend: Perfect depth")
        status.append("good")
    elif left_elbow < 70:
        feedback.append("⚠️ Elbow bend: Slightly too deep")
        status.append("warning")
    elif left_elbow <= 120:
        feedback.append("⚠️ Elbow bend: Go lower — chest not near floor")
        status.append("warning")
    else:
        feedback.append("❌ Elbow bend: Too high — lower your chest")
        status.append("bad")

    if 160 <= body_line <= 180:
        feedback.append("✅ Body line: Straight — core engaged")
        status.append("good")
    elif body_line < 160:
        feedback.append("❌ Body line: Hips sagging — engage core")
        status.append("bad")
    else:
        feedback.append("❌ Body line: Hips piking — lower your hips")
        status.append("bad")

    if elbow_flare <= 45:
        feedback.append("✅ Elbow flare: Good — elbows close to body")
        status.append("good")
    elif elbow_flare <= 60:
        feedback.append("⚠️ Elbow flare: Slightly wide — tuck elbows in")
        status.append("warning")
    else:
        feedback.append("❌ Elbow flare: Too wide — risk of shoulder injury")
        status.append("bad")

    if abs(left_elbow - right_elbow) <= 15:
        feedback.append("✅ Arm symmetry: Both arms balanced")
        status.append("good")
    else:
        feedback.append("⚠️ Arm symmetry: Uneven arm bend — balance your push")
        status.append("warning")

    return feedback, status, {
        "Left Elbow": left_elbow,
        "Right Elbow": right_elbow,
        "Body Line": body_line,
        "Elbow Flare": elbow_flare
    }


def analyze_plank(landmarks):
    feedback, status = [], []

    body_line = calculate_angle(
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 23),
        get_keypoint(landmarks, 27)
    )
    hip_position = calculate_angle(
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 23),
        get_keypoint(landmarks, 25)
    )
    shoulder_angle = calculate_angle(
        get_keypoint(landmarks, 13),
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 23)
    )
    nose_y     = get_keypoint(landmarks, 0)[1]
    shoulder_y = get_keypoint(landmarks, 11)[1]
    neck_diff  = abs(nose_y - shoulder_y)

    if 160 <= body_line <= 180:
        feedback.append("✅ Body line: Perfect plank alignment")
        status.append("good")
    elif body_line < 160:
        feedback.append("❌ Body line: Hips sagging — squeeze glutes and core")
        status.append("bad")
    else:
        feedback.append("❌ Body line: Hips too high — lower them")
        status.append("bad")

    if 170 <= hip_position <= 180:
        feedback.append("✅ Hip position: Level and stable")
        status.append("good")
    elif 155 <= hip_position < 170:
        feedback.append("⚠️ Hip position: Slightly off — adjust hips")
        status.append("warning")
    else:
        feedback.append("❌ Hip position: Hips misaligned")
        status.append("bad")

    if 85 <= shoulder_angle <= 95:
        feedback.append("✅ Shoulder: Elbows under shoulders")
        status.append("good")
    else:
        feedback.append("⚠️ Shoulder: Shift elbows under shoulders")
        status.append("warning")

    if neck_diff <= 0.08:
        feedback.append("✅ Neck: Neutral alignment")
        status.append("good")
    else:
        feedback.append("⚠️ Neck: Keep head neutral — don't drop or raise")
        status.append("warning")

    return feedback, status, {
        "Body Line": body_line,
        "Hip Position": hip_position,
        "Shoulder Angle": shoulder_angle
    }


def analyze_pullup(landmarks):
    feedback, status = [], []

    left_elbow = calculate_angle(
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 13),
        get_keypoint(landmarks, 15)
    )
    right_elbow = calculate_angle(
        get_keypoint(landmarks, 12),
        get_keypoint(landmarks, 14),
        get_keypoint(landmarks, 16)
    )
    shoulder_elevation = calculate_angle(
        get_keypoint(landmarks, 13),
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 23)
    )
    body_alignment = calculate_angle(
        get_keypoint(landmarks, 11),
        get_keypoint(landmarks, 23),
        get_keypoint(landmarks, 27)
    )

    if left_elbow < 90:
        feedback.append("✅ Pull height: Chin above bar — full rep")
        status.append("good")
    elif left_elbow <= 120:
        feedback.append("⚠️ Pull height: Pull higher — chin must clear bar")
        status.append("warning")
    else:
        feedback.append("❌ Pull height: Not pulling high enough")
        status.append("bad")

    if 170 <= right_elbow <= 180:
        feedback.append("✅ Dead hang: Full range of motion")
        status.append("good")
    elif 140 <= right_elbow < 170:
        feedback.append("⚠️ Dead hang: Extend arms fully at bottom")
        status.append("warning")
    else:
        feedback.append("❌ Dead hang: Arms not extended — hang lower")
        status.append("bad")

    if shoulder_elevation < 90:
        feedback.append("✅ Shoulder: Lats engaged — not shrugging")
        status.append("good")
    elif shoulder_elevation <= 110:
        feedback.append("⚠️ Shoulder: Slight shrug — pull blades down")
        status.append("warning")
    else:
        feedback.append("❌ Shoulder: Shrugging — engage lats not traps")
        status.append("bad")

    if 160 <= body_alignment <= 180:
        feedback.append("✅ Body: No swinging — controlled movement")
        status.append("good")
    else:
        feedback.append("❌ Body: Swinging detected — control movement")
        status.append("bad")

    return feedback, status, {
        "Left Elbow": left_elbow,
        "Right Elbow": right_elbow,
        "Shoulder Elevation": shoulder_elevation,
        "Body Alignment": body_alignment
    }

# ─────────────────────────────────────────
# USER INPUT & MAIN ANALYZER
# ─────────────────────────────────────────

def get_exercise_from_user():
    valid = ["squat", "pushup", "plank", "pullup"]
    while True:
        exercise = input("\nEnter exercise (squat / pushup / plank / pullup): ").strip().lower()
        if exercise in valid:
            return exercise
        print("❌ Invalid — please enter: squat, pushup, plank, or pullup")

def analyze_pose(landmarks, image, w, h):
    exercise = get_exercise_from_user()
    print(f"\n🏋️ Exercise: {exercise.upper()}")

    if exercise == "squat":
        feedback, status, angles = analyze_squat(landmarks)
    elif exercise == "pushup":
        feedback, status, angles = analyze_pushup(landmarks)
    elif exercise == "plank":
        feedback, status, angles = analyze_plank(landmarks)
    elif exercise == "pullup":
        feedback, status, angles = analyze_pullup(landmarks)
    else:
        return

    # Print to terminal
    print("\n📐 Joint Angles:")
    for joint, angle in angles.items():
        print(f"  {joint}: {angle}°")
    print("\n📋 Feedback:")
    for f in feedback:
        print(f"  {f}")
    good = sum(1 for s in status if s == "good")
    print(f"\n🏁 Score: {good}/{len(status)} checks passed")

    # Draw on image
    status_map = build_status_map(exercise, angles, status)
    draw_skeleton(image, landmarks, w, h, status_map)
    draw_angles_for_exercise(image, landmarks, exercise, w, h)
    output = draw_feedback_panel(image, exercise, feedback, angles, status, h, w)

    # Save & display
    cv2.imwrite("output.jpg", output)
    cv2.imshow("Workout Posture Analysis", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("\n✅ Output saved as output.jpg")

# ─────────────────────────────────────────
# MAIN ENTRY
# ─────────────────────────────────────────

BaseOptions          = mp.tasks.BaseOptions
PoseLandmarker       = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode    = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="pose_landmarker.task"),
    running_mode=VisionRunningMode.IMAGE
)

with PoseLandmarker.create_from_options(options) as landmarker:
    img_path = input("Enter image filename (e.g. workout.jpg): ").strip()
    mp_image = mp.Image.create_from_file(img_path)
    results  = landmarker.detect(mp_image)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks[0]
        image     = cv2.imread(img_path)
        h, w      = image.shape[:2]
        analyze_pose(landmarks, image, w, h)
    else:
        print("❌ No pose detected — ensure full body is visible")