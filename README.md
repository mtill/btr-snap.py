# btr-snap.py
minimalist tool to create btrfs snapshots automatically

## usage
```
usage: storybook [-h] [--config CONFIG] --task TASK [--dry_run]

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
0 *     * * *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task hourly
0 2     * * *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task daily
30 2    * * 0   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task weekly
0 3     1 * *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task monthly
30 3    1 1 *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --task yearly
```

