"""CLI for capability-reporter – authorized testing / harness validation only."""

from __future__ import annotations

import argparse

AUTHORIZED_USE = (
    "This tool is intended ONLY for authorized testing, training, and "
    "AegisPath harness validation. Unauthorized use is prohibited."
)

CAPABILITIES = {
    "network": "none",
    "filesystem": "none",
    "process": "none",
    "credentials": "none",
    "persistence": "none",
    "required_privileges": [],
    "notes": "Reference tool – zero capability surface.",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="capability-reporter (AegisPath reference tool)"
    )
    parser.add_argument(
        "--show-capabilities",
        action="store_true",
        help="Print the capability declaration and exit",
    )
    parser.add_argument(
        "--show-notice",
        action="store_true",
        help="Print the authorized-use notice and exit",
    )
    args = parser.parse_args()

    if args.show_capabilities:
        for key, value in CAPABILITIES.items():
            print(f"{key}: {value}")
        return
    if args.show_notice:
        print(AUTHORIZED_USE)
        return

    print(AUTHORIZED_USE)
    print("capability-reporter v0.1.0 – dry reference scaffold only.")
    print(
        "No network, filesystem, process, credential, or persistence actions are performed."
    )


if __name__ == "__main__":
    main()
