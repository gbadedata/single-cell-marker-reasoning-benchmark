from pathlib import Path
import json

from scbench.calibration import generate_calibration_assets


def main() -> None:
    generate_calibration_assets()

    output_dir = Path("benchmark_tasks/calibration_logs")
    print("Calibration assets generated.")

    for path in sorted(output_dir.glob("*.json")):
        payload = json.loads(path.read_text())
        print(f"- {path}")
        print(f"  keys: {list(payload.keys())}")


if __name__ == "__main__":
    main()
