# btr-snap.py
Minimalist tool to create and prune btrfs snapshots automatically.
Snapshots can be created hourly, weekly, monthly, yearly, etc.
Older snapshots are pruned automatically based on the configured retention policy (e.g., snapshots older than 6 weeks, ...).

## usage
```
usage: btr-snap.py [-h] [--config CONFIG] --task TASK [--dry_run]

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  path to config file
  --task TASK      task to execute (e.g., "hourly"/"monthly" etc.)
  --dry_run        perform dry run
```

## configuration
/etc/btr-snap.conf:
```
[

    {"subvolume": "/mnt/data/samba/server",
     "tasks": {
         "hourly": {"preserve": 12},
         "weekly": {"preserve": 4},
         "monthly": {"preserve": 6}
     }
    },

    {"subvolume": "/mnt/data/samba/media",
     "tasks": {
         "hourly": {"preserve": 12},
         "weekly": {"preserve": 4},
         "monthly": {"preserve": 6}
     }
    }

]
```

Append to /etc/crontab:
```
0 *     * * *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task hourly > /dev/null 2>&1
0 2     * * *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task daily > /dev/null 2>&1
30 2    * * 0   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task weekly > /dev/null 2>&1
0 3     1 * *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task monthly > /dev/null 2>&1
30 3    1 1 *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task yearly > /dev/null 2>&1
```

