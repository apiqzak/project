import argparse
import json
from pathlib import Path

from test_pose import VALID_EXERCISES, analyze_image_file, format_report


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}


def is_image_file(input_path):
    return Path(input_path).suffix.lower() in IMAGE_EXTENSIONS


def is_video_file(input_path):
    return Path(input_path).suffix.lower() in VIDEO_EXTENSIONS


def infer_media_type(input_path):
    suffix = Path(input_path).suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in VIDEO_EXTENSIONS:
        return "video"

    supported = ", ".join(sorted(IMAGE_EXTENSIONS | VIDEO_EXTENSIONS))
    raise ValueError(f"Unsupported file type '{suffix}'. Supported extensions: {supported}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Command-line bridge for Workout Posture Analysis."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the workout image or video.",
    )
    parser.add_argument(
        "--exercise",
        required=True,
        choices=VALID_EXERCISES,
        help="Exercise type to analyze.",
    )
    parser.add_argument(
        "--media-type",
        choices=["image", "video", "auto"],
        default="auto",
        help="Input media type. Use auto to infer from file extension.",
    )
    parser.add_argument(
        "--output",
        default="output.jpg",
        help="Path where the annotated image or video will be saved.",
    )
    parser.add_argument(
        "--report",
        default="report.txt",
        help="Path where the text report will be saved.",
    )
    parser.add_argument(
        "--json",
        default="report.json",
        help="Path where the structured JSON report will be saved.",
    )
    parser.add_argument(
        "--representative-frame",
        default=None,
        help="Optional path for a representative annotated frame when analyzing video.",
    )
    parser.add_argument(
        "--frame-step",
        type=int,
        default=5,
        help="Analyze every Nth frame for video inputs.",
    )
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=None,
        help="Optional maximum video duration to analyze in seconds.",
    )
    return parser.parse_args()


def analyze_image(args):
    report = analyze_image_file(
        args.input,
        args.exercise,
        output_path=args.output,
        show_window=False,
    )

    text_report = format_report(report)
    Path(args.report).write_text(text_report, encoding="utf-8")
    Path(args.json).write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(text_report)
    print()
    print(f"Annotated image: {args.output}")
    print(f"Text report: {args.report}")
    print(f"JSON report: {args.json}")
    return report


def analyze_video(args):
    try:
        from video_analyzer import analyze_video_file
    except ImportError as exc:
        raise RuntimeError(f"Video analyzer could not be imported: {exc}") from exc

    report = analyze_video_file(
        args.input,
        args.exercise,
        args.output,
        report_path=args.report,
        json_path=args.json,
        representative_frame_path=args.representative_frame,
        frame_step=args.frame_step,
        max_seconds=args.max_seconds,
    )

    print("Workout Video Posture Analysis")
    print(f"Exercise: {report['exercise'].upper()}")
    print(f"Frames processed: {report['processed_frames']}")
    print(f"Frames with pose: {report['frames_with_pose']}")
    print(f"Frames without pose: {report['frames_without_pose']}")
    print(f"Average score: {report['average_score']}/{report['total_checks']} checks passed")
    print(f"Most common phase: {report['most_common_phase']}")
    print()
    print(f"Annotated video: {args.output}")
    if report.get("representative_frame_path"):
        print(f"Representative frame: {report['representative_frame_path']}")
    print(f"Text report: {args.report}")
    print(f"JSON report: {args.json}")
    return report


def main():
    args = parse_args()

    input_path = Path(args.input)
    media_type = infer_media_type(input_path) if args.media_type == "auto" else args.media_type

    if media_type == "image" and not is_image_file(input_path):
        raise ValueError(f"Media type is image, but input does not look like an image: {args.input}")
    if media_type == "video" and not is_video_file(input_path):
        raise ValueError(f"Media type is video, but input does not look like a supported video: {args.input}")

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    if media_type == "image":
        analyze_image(args)
    elif media_type == "video":
        analyze_video(args)
    else:
        raise ValueError(f"Unsupported media type: {media_type}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[ERROR] {exc}")
        raise SystemExit(1)
