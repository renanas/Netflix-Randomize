#!/usr/bin/env python
"""Run all scripts in sequence and report results."""
import subprocess
import os
import sys
from pathlib import Path

scripts_dir = Path("scripts")
scripts = [
    "debug_env.py",
    "test_mongodb_connection_class.py",
    "test_mongo_ping.py",
    "hash_existing_password.py",
    "test_movie_repository.py",
    "test_tmdb.py",
]

print("=" * 70)
print("RUNNING ALL SCRIPTS")
print("=" * 70)

for script in scripts:
    script_path = scripts_dir / script
    if not script_path.exists():
        print(f"\n❌ {script} - NOT FOUND")
        continue
    
    print(f"\n{'='*70}")
    print(f"▶️  {script}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=False,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"✅ {script} - SUCCESS")
        else:
            print(f"⚠️  {script} - EXIT CODE {result.returncode}")
    except subprocess.TimeoutExpired:
        print(f"⏱️  {script} - TIMEOUT")
    except Exception as e:
        print(f"❌ {script} - ERROR: {e}")

print(f"\n{'='*70}")
print("ALL SCRIPTS COMPLETED")
print(f"{'='*70}")
