import os
import stat
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# Attempt to import watchdog; handle the case if it's missing
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("Warning: 'watchdog' module is not installed. Real-time monitoring will be disabled.")


# Default directories to scan
SCAN_DIRS = [os.path.expanduser("~"), "/etc", "/var"]

def check_permissions(file_path):
    """Check file permissions and ownership and assign risk scores."""
    try:
        st = os.stat(file_path)
        mode = st.st_mode
        uid = st.st_uid
        risk = 0
        suggestions = []

        if mode & stat.S_IWOTH:
            risk += 5
            suggestions.append("Remove world write: chmod o-w")

        if mode & stat.S_IWGRP:
            risk += 3
            suggestions.append("Remove group write: chmod g-w")

        if uid == 0 and (mode & stat.S_IWGRP or mode & stat.S_IWOTH):
            risk += 4
            suggestions.append("Restrict root-owned file permissions")

        if mode & stat.S_IXUSR and os.path.expanduser("~") in file_path:
            risk += 2
            suggestions.append("Check if executable is safe")

        return risk, suggestions
    except Exception as e:
        print(f"Error checking permissions for {file_path}: {e}")
        return 0, []

def report_file(file_path):
    """Check a file and report if it has a non-zero risk score."""
    risk, suggestions = check_permissions(file_path)
    if risk > 0:
        print(f"[ALERT] {file_path} - Risk Score: {risk}")
        for s in suggestions:
            print(f"  -> Suggestion: {s}")
        return {
            "file": file_path,
            "risk_score": risk,
            "suggestions": suggestions,
            "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
        }
    return None

def full_scan(directories):
    """Perform a full scan of specified directories."""
    results = []
    for d in directories:
        if not os.path.exists(d):
            print(f"Warning: Directory {d} does not exist. Skipping.")
        else:
            for root, _, files in os.walk(d):
                for f in files:
                    path = os.path.join(root, f)
                    try:
                        res = report_file(path)
                        if res:
                            results.append(res)
                    except PermissionError:
                        print(f"Permission denied: Skipping file {path}")
                    except Exception as e:
                        print(f"Error processing file {path}: {e}")

    if results:
        with open("prmscan_report.json", "w") as f:
            json.dump(results, f, indent=4)
        print("\nFull report saved to prmscan_report.json")

def monitor_dirs(directories):
    """Monitor directories for risky files in real-time."""
    if not WATCHDOG_AVAILABLE:
        print("Real-time monitoring is disabled because 'watchdog' is not installed.")
        return

    class RiskHandler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                report_file(event.src_path)

        def on_modified(self, event):
            if not event.is_directory:
                report_file(event.src_path)

    observer = Observer()
    handler = RiskHandler()
    for d in directories:
        if not os.path.exists(d):
            print(f"Warning: Directory {d} does not exist. Skipping.")
        else:
            observer.schedule(handler, d, recursive=True)
    observer.start()
    print("Monitoring directories for risky files (Ctrl+C to stop)...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    parser = argparse.ArgumentParser(description="PrmScan - Linux Permission Anomaly Detector")
    
    # Enhanced help message with examples
    parser.epilog = """
Examples:
  1. Scan directories and generate a report:
     python prmscan.py -d /path/to/dir1 /path/to/dir2 -r

  2. Monitor directories in real-time for risky files:
     python prmscan.py -m

  3. Use default directories and generate a report:
     python prmscan.py -r
"""
    
    parser.add_argument("-d", "--directories", nargs="*", default=SCAN_DIRS, help="Directories to scan (default: ~/ /etc /var)")
    parser.add_argument("-r", "--report", action="store_true", help="Generate a JSON report")
    parser.add_argument("-m", "--monitor", action="store_true", help="Monitor directories in real-time")

    args = parser.parse_args()

    if not any([args.report, args.monitor]):
        parser.print_help()
        return

    if args.report:
        full_scan(args.directories)
    if args.monitor:
        monitor_dirs(args.directories)

if __name__ == "__main__":
    main()
