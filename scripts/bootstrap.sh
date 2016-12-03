#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="$(dirname $SCRIPT_DIR)"

$SCRIPT_DIR/manage.sh migrate
$SCRIPT_DIR/manage.sh loadtestdata stats.Trader:100 stats.Transaction:10000 stats.Deal:300000
