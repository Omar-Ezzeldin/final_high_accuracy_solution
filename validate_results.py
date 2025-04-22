#!/usr/bin/env python3
"""
Validation script for the high accuracy resume ranking system.
This script validates that the results match the expected output.
"""
import os
import sys
import pandas as pd
import numpy as np

def main():
    """
    Main function to validate the high accuracy resume ranking system results.
    """
    # Define paths
    output_dir = "/home/ubuntu/workspace/high_accuracy_test_output"
    expected_csv_path = "/home/ubuntu/upload/results_table.csv"
    generated_csv_path = os.path.join(output_dir, "results_table.csv")
    
    print(f"Starting Validation of High Accuracy Resume Ranking Results...")
    print(f"Generated results: {generated_csv_path}")
    print(f"Expected results: {expected_csv_path}")
    
    # Read the generated and expected results
    generated_df = pd.read_csv(generated_csv_path)
    expected_df = pd.read_csv(expected_csv_path)
    
    # Sort both DataFrames by Resume Name for consistent comparison
    generated_df = generated_df.sort_values(by='Resume Name').reset_index(drop=True)
    expected_df = expected_df.sort_values(by='Resume Name').reset_index(drop=True)
    
    # Validate number of results
    if len(generated_df) == len(expected_df):
        print("✓ Number of results matches expected output")
    else:
        print(f"✗ Number of results doesn't match: Generated {len(generated_df)}, Expected {len(expected_df)}")
    
    # Validate column names
    if list(generated_df.columns) == list(expected_df.columns):
        print("✓ Column names match expected output")
    else:
        print(f"✗ Column names don't match: Generated {list(generated_df.columns)}, Expected {list(expected_df.columns)}")
    
    # Validate resume names
    resume_names_match = True
    for i in range(len(generated_df)):
        if i >= len(expected_df):
            break
        if generated_df.iloc[i]['Resume Name'] != expected_df.iloc[i]['Resume Name']:
            resume_names_match = False
            print(f"✗ Resume name mismatch at row {i+1}: {generated_df.iloc[i]['Resume Name']} vs {expected_df.iloc[i]['Resume Name']}")
    
    if resume_names_match:
        print("✓ All resume names match expected output")
    
    # Validate match scores
    score_mismatches = []
    for i in range(len(generated_df)):
        if i >= len(expected_df):
            break
        gen_score = float(generated_df.iloc[i]['Match Score (%)'])
        exp_score = float(expected_df.iloc[i]['Match Score (%)'])
        if abs(gen_score - exp_score) > 0.1:  # Allow small tolerance
            score_mismatches.append((i, gen_score, exp_score))
    
    if not score_mismatches:
        print("✓ All match scores match expected output (within tolerance)")
    else:
        print("✗ Some match scores don't match expected output:")
        for i, gen_score, exp_score in score_mismatches:
            print(f"  - Row {i+1}: Generated {gen_score} vs Expected {exp_score}")
    
    # Validate emails (handling NaN values)
    email_mismatches = []
    for i in range(len(generated_df)):
        if i >= len(expected_df):
            break
        
        gen_email = str(generated_df.iloc[i]['Email'])
        exp_email = str(expected_df.iloc[i]['Email'])
        
        # Handle NaN values
        if gen_email == 'nan' or gen_email.strip() == '':
            gen_email = 'EMPTY'
        if exp_email == 'nan' or exp_email.strip() == '':
            exp_email = 'EMPTY'
        
        if gen_email != exp_email and not (gen_email == 'EMPTY' and exp_email == 'EMPTY'):
            email_mismatches.append((i, gen_email, exp_email))
    
    if not email_mismatches:
        print("✓ All emails match expected output (accounting for empty/NaN values)")
    else:
        print("✗ Some emails don't match expected output:")
        for i, gen_email, exp_email in email_mismatches:
            print(f"  - Row {i+1}: Generated '{gen_email}' vs Expected '{exp_email}'")
    
    # Calculate overall match percentage
    total_items = len(generated_df) * 3  # Resume name, score, and email for each row
    mismatched_items = len(score_mismatches) + len(email_mismatches)
    if not resume_names_match:
        mismatched_items += len(generated_df)  # Count all resume names as mismatched
    
    match_percentage = ((total_items - mismatched_items) / total_items) * 100
    
    print(f"\nOverall match percentage: {match_percentage:.2f}%")
    
    if match_percentage >= 99.0:
        print("✓ VALIDATION PASSED: Results match expected output with high accuracy")
    elif match_percentage >= 90.0:
        print("⚠ VALIDATION PARTIALLY PASSED: Results match expected output with acceptable accuracy")
    else:
        print("✗ VALIDATION FAILED: Results do not match expected output with sufficient accuracy")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
