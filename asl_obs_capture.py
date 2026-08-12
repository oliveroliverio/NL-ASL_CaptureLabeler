from datetime import datetime
from pathlib import Path
import json
import os
import time
import uuid

import obsws_python as obs
from dotenv import load_dotenv


load_dotenv()

RAW_DIR = Path(os.environ["RAW_DIR"]).expanduser()
METADATA_PATH = Path(os.environ["METADATA_PATH"]).expanduser()

OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", "4455"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD", "")

RAW_DIR.mkdir(parents=True, exist_ok=True)
METADATA_PATH.parent.mkdir(parents=True, exist_ok=True)


def append_metadata(record: dict):
    with METADATA_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def choose_preferred_take(records: list[dict]):
    # If there is only one take, default it to preferred.
    if len(records) == 1:
        records[0]["preferred_take"] = True
        print("\nOnly one take recorded → marked as preferred.")
        return

    print("\nRecorded takes:")
    for record in records:
        print(
            f"  Take {record['take']}: "
            f"{record['self_quality']} | "
            f"{record['filename']}"
        )

    while True:
        choice = input(
            "\nPreferred take number, or ENTER for none: "
        ).strip()

        if choice == "":
            print("No preferred take selected.")
            return

        try:
            preferred_take = int(choice)
        except ValueError:
            print("Enter a take number or press ENTER for none.")
            continue

        matching = [
            record
            for record in records
            if record["take"] == preferred_take
        ]

        if not matching:
            print("That take number does not exist.")
            continue

        matching[0]["preferred_take"] = True
        print(f"Take {preferred_take} marked as preferred.")
        return


def main():
    client = obs.ReqClient(
        host=OBS_HOST,
        port=OBS_PORT,
        password=OBS_PASSWORD,
        timeout=5,
    )

    print("Connected to OBS.")

    prompt_en = input("English word / sentence: ").strip()

    capture_type = (
        input(
            "Type [word/sentence/letter] "
            "(default: word): "
        ).strip()
        or "word"
    )

    session_id = str(uuid.uuid4())

    records = []
    take = 1

    while True:
        input(
            f"\nTake {take}: "
            "press ENTER to start recording..."
        )

        client.start_record()
        print("● RECORDING")

        input("Press ENTER to stop recording...")

        response = client.stop_record()
        print("■ STOPPED")

        obs_path = Path(response.output_path)

        # Give OBS/filesystem a moment to finalize the recording.
        time.sleep(0.5)

        recording_id = str(uuid.uuid4())
        now = datetime.now().astimezone()
        timestamp = now.strftime("%y%m%d-%H%M%S")

        new_filename = (
            f"{timestamp}_{recording_id}"
            f"{obs_path.suffix.lower()}"
        )

        destination = RAW_DIR / new_filename

        obs_path.rename(destination)

        quality = (
            input(
                "Quality "
                "[good/uncertain/incorrect/practice] "
                "(default: practice): "
            ).strip()
            or "practice"
        )

        record = {
            "recording_id": recording_id,
            "session_id": session_id,
            "filename": new_filename,
            "path": str(destination),
            "recorded_at": now.isoformat(),
            "prompt_en": prompt_en,
            "ASL_gloss": None,
            "capture_type": capture_type,
            "take": take,
            "preferred_take": False,
            "self_quality": quality,
            "accuracy_status": "unverified",
            "source": "self_recorded",
            "signer_id": "oo",
        }

        records.append(record)

        print(f"Saved: {destination.name}")

        another = (
            input("Record another take? [Y/n]: ")
            .strip()
            .lower()
        )

        if another == "n":
            break

        take += 1

    choose_preferred_take(records)

    # Write finalized session metadata only after
    # preferred-take selection is complete.
    for record in records:
        append_metadata(record)

    print("\nSession complete.")
    print("Session ID:", session_id)
    print(f"Saved {len(records)} metadata record(s).")


if __name__ == "__main__":
    main()