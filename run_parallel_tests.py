"""
Helper script to run parallel tests on BrowserStack.
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Run pytest with BrowserStack SDK."""
    
    # Ensure we're in the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Check environment variables
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    
    if not username or not access_key:
        print("ERROR: BrowserStack credentials not found!")
        print("Please set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables.")
        return 1
    
    print("=" * 80)
    print("RUNNING PARALLEL TESTS ON BROWSERSTACK")
    print("=" * 80)
    print(f"Username: {username}")
    print(f"Configuration: browserstack.yml")
    print(f"Platforms: 5 (3 desktop + 2 mobile)")
    print("=" * 80)
    print()
    
    # Run pytest with BrowserStack SDK
    cmd = [
        "browserstack-sdk",
        "pytest",
        "test_scraper.py",
        "-v",
        "-s",
        "--html=report.html",
        "--self-contained-html"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, cwd=project_dir)
        
        print()
        print("=" * 80)
        if result.returncode == 0:
            print("✓ TESTS COMPLETED SUCCESSFULLY")
        else:
            print("✗ TESTS FAILED")
        print("=" * 80)
        print()
        print("View detailed results:")
        print(f"  - HTML Report: {project_dir / 'report.html'}")
        print("  - BrowserStack Dashboard: https://automate.browserstack.com/dashboard")
        print()
        
        return result.returncode
        
    except FileNotFoundError:
        print("ERROR: browserstack-sdk command not found!")
        print("Please install it with: pip install browserstack-sdk")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
