#!/bin/bash
RESULT_DIR='./results_from_transcribe/'

python3 src/main.py -wer ${RESULT_DIR}
