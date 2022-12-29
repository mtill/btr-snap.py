# btr-snap.py
minimalist tool to create btrfs snapshots automatically

## configuration

/etc/btr-snap.conf:
```
[

    {"subvolume": "/mnt/data/samba/server",
     "rules": {
         "hourly": {"preserve": 12},
         "weekly": {"preserve": 4},
         "monthly": {"preserve": 6}
     }
    },

    {"subvolume": "/mnt/data/samba/media",
     "rules": {
         "hourly": {"preserve": 12},
         "weekly": {"preserve": 4},
         "monthly": {"preserve": 6}
     }
    }

]
```

Append to /etc/crontab:
```
0 *     * * *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --rule hourly
0 2     * * *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --rule daily
30 2    * * 0   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --rule weekly
0 3     1 * *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --rule monthly
30 3    1 1 *   root    /root/btr-snap.py/btr-snap.py --config /etc/btr-snap.conf --rule yearly
```

