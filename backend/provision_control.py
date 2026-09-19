"""Generate private control-portal account configuration.

Usage:
  python backend/provision_control.py --role owner --username owner@example.com
  python backend/provision_control.py --role worker --username reviewer@example.com

The password is entered interactively and the script prints a password hash only.
It never writes credentials into the repository or logs the password.
"""
from __future__ import annotations

import argparse
import getpass
import secrets
import sys

from control_auth import password_hash


def main() -> int:
    parser = argparse.ArgumentParser(description="Provision a Manavivaha control account")
    parser.add_argument("--role", choices=("owner", "worker", "moderator", "support", "finance"), required=True)
    parser.add_argument("--username", required=True)
    args = parser.parse_args()
    first = getpass.getpass("Password (14+ characters): ")
    again = getpass.getpass("Repeat password: ")
    if first != again:
        print("Passwords do not match", file=sys.stderr)
        return 2
    try:
        encoded = password_hash(first)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print("\nAdd this account to CONTROL_ACCOUNTS_JSON in your secret manager:")
    print('{"%s":{"username":"%s","password_hash":"%s"}}' %
          (args.role, args.username.strip().lower(), encoded))
    print("\nDo not commit this value. Restart the backend after secret rotation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
