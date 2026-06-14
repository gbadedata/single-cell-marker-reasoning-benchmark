import json
from scbench.scoring import score_solver_answers


def main() -> None:
    report = score_solver_answers()

    print("Solver answer scoring complete.")
    print(json.dumps(report["summary"], indent=2))
    print("\nDetailed report saved to:")
    print("results/reports/sample_solver_score_report.json")


if __name__ == "__main__":
    main()
