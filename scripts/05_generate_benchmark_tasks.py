from pathlib import Path
import json

from scbench.benchmark_tasks import generate_all_benchmark_tasks


def count_tasks(path: Path) -> int:
    payload = json.loads(path.read_text())
    return len(payload["tasks"])


def main() -> None:
    generate_all_benchmark_tasks()

    public_dir = Path("benchmark_tasks/public")
    hidden_dir = Path("benchmark_tasks/hidden")

    print("Benchmark task generation complete.")
    print("\nPublic task files:")
    for path in sorted(public_dir.glob("*.json")):
        print(f"- {path}: {count_tasks(path)} tasks")

    print("\nHidden answer files:")
    for path in sorted(hidden_dir.glob("*.json")):
        payload = json.loads(path.read_text())
        print(f"- {path}: {len(payload['answers'])} hidden answers")


if __name__ == "__main__":
    main()
