from pathlib import Path
from datetime import datetime
import json
import os
import shutil
import uuid

from dotenv import load_dotenv


load_dotenv()

WATCH_DIR = Path(os.environ["WATCH_DIR"]).expanduser()
RAW_DIR = Path(os.environ["RAW_DIR"]).expanduser()
METADATA_PATH = Path(os.environ["METADATA_PATH"]).expanduser()

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}

RAW_DIR.mkdir(parents=True, exist_ok=True)
METADATA_PATH.parent.mkdir(parents=True, exist_ok=True)


def append_metadata(record: dict):
    with METADATA_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def process_video(path: Path):
    print(f"\nProcessing: {path.name}")

    prompt_en = input("English prompt: ").strip()

    capture_type = (
        input("Type [sentence/word/letter] (default: sentence): ").strip()
        or "sentence"
    )

    take_str = input("Take number (default: 1): ").strip()
    take = int(take_str) if take_str else 1

    quality = (
        input(
            "Quality [good/uncertain/incorrect/practice] "
            "(default: practice): "
        ).strip()
        or "practice"
    )

    preferred_take = (
        input("Preferred take? [y/N]: ").strip().lower() == "y"
    )

    recording_id = str(uuid.uuid4())

    now = datetime.now()
    timestamp = now.strftime("%y%m%d-%H%M%S")

    new_filename = f"{timestamp}_{recording_id}{path.suffix.lower()}"
    destination = RAW_DIR / new_filename

    shutil.move(str(path), str(destination))

    record = {
        "recording_id": recording_id,
        "filename": new_filename,
        "path": str(destination),
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

    print(f"Saved video: {destination}")
    print(f"Metadata:    {METADATA_PATH}")


def main():
    pending_files = sorted(
        p
        for p in WATCH_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS
    )

    if not pending_files:
        print("No unprocessed videos found.")
        return

    print(f"Found {len(pending_files)} unprocessed video(s).")

    for path in pending_files:
        process_video(path)

    print("\nDone. All detected videos were processed.")


if __name__ == "__main__":
    main()