#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pathlib import Path
import argparse
import datetime
import subprocess
import json


def snappy(theconfigs, therule, dry_run):
    for theconfig in theconfigs:
        print("\n== " + theconfig["subvolume"] + " ==")
        rules = theconfig.get("rules", [])
        if therule not in rules:   # rule not defined for this config; continuing
            print("   nothing to do for rule \"" + therule + "\"")
            continue

        preserve = rules[therule].get("preserve", None)
        if preserve is not None and preserve <= 0:
            raise RuntimeError("   preserve: should be a positive number")

        subvol = Path(theconfig["subvolume"])
        snapDir = subvol / Path(theconfig.get("snapshot_dir", "_snapshots")) / therule
        snapDir.mkdir(mode=0o771, exist_ok=True)

        if preserve is not None:
            existingSnapshots = sorted(snapDir.iterdir(), key=lambda f: f.stat().st_ctime)
            numEntriesToDelete = len(existingSnapshots) - preserve + 1
            if numEntriesToDelete > 0:
                print("   deleting " + str(numEntriesToDelete) + " older snapshots:")
                for s in existingSnapshots[0:numEntriesToDelete]:
                    print("     deleting " + str(s))
                    if not args.dry_run:
                        delProcess = subprocess.run(["btrfs", "subvolume", "delete", str(s)], check=True, stdout=subprocess.DEVNULL)
	
                print()

        nowStr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        snapshotName = nowStr
        fullSnapDir = snapDir / snapshotName
        print("   creating snapshot: " + str(fullSnapDir))
        if not args.dry_run:
            snapProcess = subprocess.run(["btrfs", "subvolume", "snapshot", "-r", theconfig["subvolume"], str(fullSnapDir)], check=True, stdout=subprocess.DEVNULL)
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='storybook')
    parser.add_argument('--config', required=True, help='path to config file')
    parser.add_argument('--rule', required=True, help='selected rule (e.g., "hourly"/"monthly" etc.')
    parser.add_argument('--dry_run', action='store_true', help='perform dry run')
    args = parser.parse_args()

    with open(args.config, "r") as f:
        theconfigs = json.load(f)

    if args.dry_run:
        print("\n  || === DRY RUN === ||")

    snappy(theconfigs=theconfigs, therule=args.rule, dry_run=args.dry_run)

