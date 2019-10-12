#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SRC_DIR="${SCRIPT_DIR}/dist/"
DST_DIR="/media/pkv/CIRCUITPY/"

rsync -r "${SRC_DIR}" "${DST_DIR}"
sync
