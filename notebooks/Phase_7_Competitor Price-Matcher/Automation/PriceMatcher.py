#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    "test_harvey.py",
    "test_currys.py",
    "test_argos.py",
    "test_donaghy.py",
    "test_dse.py",
]


def main():
    project_dir = Path(__file__).resolve().parent

    failures = []

    for script in SCRIPTS:
        print(f"\n{'=' * 70}")
        print(f"Running {script}")
        print("=" * 70)

        script_path = project_dir / script

        if not script_path.exists():
            print(
                f"[error] Missing retailer script: "
                f"{script_path}"
            )

            failures.append(script)
            continue

        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
            ],
            cwd=project_dir,
        )

        if result.returncode != 0:
            print(
                f"[warn] {script} exited with code "
                f"{result.returncode} - continuing"
            )

            failures.append(script)

    print(f"\n{'=' * 70}")

    if failures:
        print(
            f"Completed with {len(failures)} "
            f"failed retailer script(s): "
            f"{', '.join(failures)}"
        )

    else:
        print(
            "All retailer scripts finished successfully."
        )

        print(
            "Open price_comparison.xlsx to review."
        )

    print("=" * 70)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
