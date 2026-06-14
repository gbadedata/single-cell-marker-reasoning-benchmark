from pathlib import Path
import json

from scbench.oracles import generate_all_oracle_outputs


def main() -> None:
    generate_all_oracle_outputs()

    output_dir = Path("benchmark_tasks/oracle_outputs")

    print("Oracle output generation complete.")
    for path in sorted(output_dir.glob("*.json")):
        payload = json.loads(path.read_text())
        print(f"- {path}: {len(payload['oracle_outputs'])} oracle outputs")


if __name__ == "__main__":
    main()
