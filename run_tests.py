#!/usr/bin/env python
"""
Test runner script for the authentication service.
"""
import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print("=" * 60)

    result = subprocess.run(command, shell=True, capture_output=False)

    if result.returncode != 0:
        print(f"\n❌ {description} failed with return code {result.returncode}")
        return False
    else:
        print(f"\n✅ {description} completed successfully")
        return True


def main():
    """Main test runner function."""
    print("🚀 Authentication Service Test Runner")
    print("=" * 60)

    # Change to project directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # Test commands to run
    test_commands = [
        # Run all tests with verbose output
        ("pytest tests/ -v", "All Tests (Verbose)"),
        # Run tests with coverage
        ("pytest tests/ --cov=src --cov-report=term-missing", "Tests with Coverage"),
        # Run only unit tests (excluding integration)
        (
            "pytest tests/domain/ tests/application/ tests/infrastructure/ -v",
            "Unit Tests Only",
        ),
        # Run only integration tests
        ("pytest tests/test_integration.py -v", "Integration Tests Only"),
        # Run tests and generate HTML coverage report
        (
            "pytest tests/ --cov=src --cov-report=html:htmlcov",
            "Tests with HTML Coverage Report",
        ),
        # Run tests with junit XML output (for CI/CD)
        ("pytest tests/ --junitxml=test-results.xml", "Tests with JUnit XML Output"),
    ]

    successful_runs = 0
    total_runs = len(test_commands)

    for command, description in test_commands:
        if run_command(command, description):
            successful_runs += 1
        else:
            print(f"⚠️  Continuing with remaining tests...")

    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Successful: {successful_runs}/{total_runs}")
    print(f"Failed: {total_runs - successful_runs}/{total_runs}")

    if successful_runs == total_runs:
        print("🎉 All test runs completed successfully!")
        print("\n📁 Check the following files for results:")
        print("   - htmlcov/index.html (Coverage Report)")
        print("   - test-results.xml (JUnit XML)")
        return 0
    else:
        print("❌ Some test runs failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
