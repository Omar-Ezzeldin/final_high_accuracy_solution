#!/usr/bin/env python3
"""
Test script for the high accuracy resume ranking system.
This script tests the modified code to verify it produces the expected higher accuracy results.
"""
import os
import sys
import json
import pandas as pd
from mpnet_resume_matcher import MPNetResumeMatcher

def main():
    """
    Main function to test the high accuracy resume ranking system.
    """
    # Define paths
    resumes_dir = "/home/ubuntu/workspace/extracted_resumes/resumes - Copy/"
    job_json_path = "/home/ubuntu/upload/software_engineer_job.json"
    output_dir = "/home/ubuntu/workspace/high_accuracy_test_output"
    expected_csv_path = "/home/ubuntu/upload/results_table.csv"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting High Accuracy Resume Ranking Test...")
    print(f"Resumes directory: {resumes_dir}")
    print(f"Job requirements: {job_json_path}")
    print(f"Output directory: {output_dir}")
    print("Processing...")
    
    # Initialize the matcher
    matcher = MPNetResumeMatcher()
    
    # Match resumes with job
    match_results = matcher.match_resumes_with_job(resumes_dir, job_json_path)
    
    # Save results to CSV
    results_table_path = os.path.join(output_dir, "results_table.csv")
    
    # Extract relevant information for the table
    table_data = []
    for result in match_results:
        table_data.append({
            'Resume Name': result['resume_name'],
            'Match Score (%)': result['match_score'],
            'Email': result['email']
        })
    
    # Create DataFrame
    df = pd.DataFrame(table_data)
    
    # Sort by match score (descending)
    df = df.sort_values(by='Match Score (%)', ascending=False)
    
    # Save to CSV
    df.to_csv(results_table_path, index=False)
    
    # Print results
    print("\nRanking completed successfully!")
    print(f"Results table saved to: {results_table_path}")
    
    # Compare with expected results
    print("\nValidating results against expected output...")
    
    # Read the expected results
    expected_df = pd.read_csv(expected_csv_path)
    
    # Check if the results match
    if len(df) == len(expected_df):
        print("✓ Number of results matches expected output")
    else:
        print(f"✗ Number of results doesn't match: Generated {len(df)}, Expected {len(expected_df)}")
    
    # Check column names
    if list(df.columns) == list(expected_df.columns):
        print("✓ Column names match expected output")
    else:
        print(f"✗ Column names don't match: Generated {list(df.columns)}, Expected {list(expected_df.columns)}")
    
    # Check content
    all_match = True
    mismatches = []
    
    # Sort both DataFrames by Resume Name to ensure consistent comparison
    df = df.sort_values(by='Resume Name').reset_index(drop=True)
    expected_df = expected_df.sort_values(by='Resume Name').reset_index(drop=True)
    
    for i in range(len(df)):
        if i >= len(expected_df):
            break
            
        gen_row = df.iloc[i]
        exp_row = expected_df.iloc[i]
        
        # Compare resume name
        if gen_row['Resume Name'] != exp_row['Resume Name']:
            all_match = False
            mismatches.append(f"Row {i+1} Resume Name mismatch: {gen_row['Resume Name']} vs {exp_row['Resume Name']}")
        
        # Compare match score (with small tolerance)
        if abs(float(gen_row['Match Score (%)']) - float(exp_row['Match Score (%)'])) > 0.1:
            all_match = False
            mismatches.append(f"Row {i+1} Match Score mismatch: {gen_row['Match Score (%)']} vs {exp_row['Match Score (%)']}")
        
        # Compare email
        if gen_row['Email'] != exp_row['Email']:
            all_match = False
            mismatches.append(f"Row {i+1} Email mismatch: {gen_row['Email']} vs {exp_row['Email']}")
    
    if all_match:
        print("✓ All rows match expected output")
    else:
        print("✗ Some rows don't match expected output:")
        for mismatch in mismatches:
            print(f"  - {mismatch}")
    
    # Print detailed comparison
    print("\nDetailed Comparison:")
    print("Generated Results:")
    print(df.to_string())
    print("\nExpected Results:")
    print(expected_df.to_string())
    
    print("\nTest completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
