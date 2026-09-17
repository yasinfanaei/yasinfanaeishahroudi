#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.validation import validate_repository

def validate_site(root:Path): return validate_repository(root)
if __name__=='__main__':
    problems=validate_site(Path(__file__).resolve().parents[1])
    if problems:
        [print(f'ERROR: {x}') for x in problems]; raise SystemExit(1)
    print('Content validation passed.')
