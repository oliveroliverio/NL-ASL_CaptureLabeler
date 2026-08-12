from pathlib import Path
from datetime import datetime
import json
import time
import uuid

WATCH_DIR = Path("/Users/mbp-14/Downloads/DATALAKE_mb14/NL-ASL/_Watch")
METADATA_PATH = WATCH_DIR.parent / "metadata" / "recordings.jsonl"

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}

METADATA_PATH.parent.mkdir(parents=True, exist_ok=True)


def append_metadata(record: dict):
    with METADATA_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def wait_for_file_to_finish(path: Path, stable_seconds=2):
    previous_size = -1
    stable_count = 0

    while stable_count < stable_seconds:
        current_size = path.stat().st_size

        if current_size == previous_size:
            stable_count += 1
        else:
            stable_count = 0

        previous_size = current_size
        time.sleep(1)


def process_new_video(path: Path):
    print(f"\nDetected: {path.name}")

    wait_for_file_to_finish(path)

    prompt_en = input("English prompt: ").strip()

    capture_type = input(
        "Type [sentence/word/letter] (default: sentence): "
    ).strip() or "sentence"

    take_str = input("Take number (default: 1): ").strip()
    take = int(take_str) if take_str else 1

    quality = input(
        "Quality [good/uncertain/incorrect/practice] "
        "(default: practice): "
    ).strip() or "practice"

    preferred_input = input(
        "Preferred take? [y/N]: "
    ).strip().lower()

    preferred_take = preferred_input == "y"

    recording_id = str(uuid.uuid4())

    now = datetime.now()
    timestamp = now.strftime("%y%m%d-%H%M%S")

    new_filename = f"{timestamp}_{recording_id}{path.suffix.lower()}"
    new_path = path.with_name(new_filename)

    path.rename(new_path)

    record = {
        "recording_id": recording_id,
        "filename": new_filename,
        "recorded_at": now.astimezone().isoformat(),
        "prompt_en": prompt_en,
        "ASL_gloss": None,
        "capture_type": capture_type,
        "take": take,
        "preferred_take": preferred_take,
        "self_quality": quality,
        "accuracy_status": "unverified",
        "source": "self_recorded",
        "signer_id": "oo",
    }

    append_metadata(record)

    print(f"Renamed to: {new_filename}")
    print(f"Metadata appended to: {METADATA_PATH}")


def main():
    print("Watching:")
    print(WATCH_DIR)
    print("\nPress Ctrl+C to stop.\n")

    known_files = {
        p.resolve()
        for p in WATCH_DIR.iterdir()
        if p.is_file()
    }

    while True:
        current_files = {
            p.resolve()
            for p in WATCH_DIR.iterdir()
            if p.is_file()
            and p.suffix.lower() in VIDEO_EXTENSIONS
        }

        new_files = current_files - known_files

        for file_path in sorted(new_files):
            process_new_video(Path(file_path))

        known_files |= new_files

        time.sleep(1)


if __name__ == "__main__":
    main()