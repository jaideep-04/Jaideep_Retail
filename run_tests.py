#!/usr/bin/env python
"""
Comprehensive test runner for Retail Analytics Platform
Runs all tests with coverage reporting
"""

import subprocess
import sys
import os

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def run_tests():
    """Run all tests with coverage"""
    
    print_header("RETAIL ANALYTICS PLATFORM - TEST SUITE")
    
    # Check if test files exist
    test_files = ['test_api.py', 'test_etl.py', 'test_database.py']
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"Warning: {test_file} not found")
    
    print("Installing test dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "test_requirements.txt"])
    
    # Test 1: API Tests
    print_header("RUNNING API TESTS")
    result_api = subprocess.run([
        sys.executable, "-m", "pytest", 
        "test_api.py", 
        "-v", 
        "--tb=short",
        "-m", "api"
    ])
    
    # Test 2: ETL Tests
    print_header("RUNNING ETL PIPELINE TESTS")
    result_etl = subprocess.run([
        sys.executable, "-m", "pytest", 
        "test_etl.py", 
        "-v", 
        "--tb=short",
        "-m", "etl"
    ])
    
    # Test 3: Database Tests
    print_header("RUNNING DATABASE TESTS")
    result_db = subprocess.run([
        sys.executable, "-m", "pytest", 
        "test_database.py", 
        "-v", 
        "--tb=short",
        "-m", "database"
    ])
    
    # Test 4: All Tests with Coverage
    print_header("RUNNING ALL TESTS WITH COVERAGE")
    result_all = subprocess.run([
        sys.executable, "-m", "pytest", 
        "test_api.py", "test_etl.py", "test_database.py",
        "-v",
        "--cov=src",
        "--cov-report=html",
        "--cov-report=term-missing"
    ])
    
    # Summary
    print_header("TEST SUMMARY")
    
    test_results = {
        "API Tests": result_api.returncode,
        "ETL Tests": result_etl.returncode,
        "Database Tests": result_db.returncode,
        "All Tests": result_all.returncode
    }
    
    passed = sum(1 for v in test_results.values() if v == 0)
    failed = sum(1 for v in test_results.values() if v != 0)
    
    for test_name, returncode in test_results.items():
        status = "✓ PASSED" if returncode == 0 else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n  Total: {passed} passed, {failed} failed")
    
    if result_all.returncode == 0:
        print("\n✓ ALL TESTS PASSED!")
        print("\nCoverage report generated in: htmlcov/index.html")
    else:
        print("\n✗ SOME TESTS FAILED")
        print("Review output above for details")
    
    return result_all.returncode

if __name__ == "__main__":
    sys.exit(run_tests())