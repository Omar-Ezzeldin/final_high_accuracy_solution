#!/usr/bin/env python3
"""
Main Application for MPNet-based AI Resume Ranker
This script runs the complete MPNet-based AI Resume Ranker system, which matches resumes with
job requirements using the all-mpnet-base-v2 model and generates a results table and detailed reports.
"""
import os
import sys
import argparse
import torch
from mpnet_output_generator import MPNetOutputGenerator

def main():
    """
    Main function to run the MPNet-based AI Resume Ranker.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='MPNet-based AI Resume Ranker')
    parser.add_argument('--resumes_dir', type=str, required=True,
                        help='Directory containing resume files (PDF/DOCX)')
    parser.add_argument('--job_json', type=str, required=True,
                        help='Path to job requirements JSON file')
    parser.add_argument('--output_dir', type=str, default='./output_mpnet',
                        help='Directory to save output files (default: ./output_mpnet)')
    parser.add_argument('--model', type=str, default='all-mpnet-base-v2',
                        help='Sentence transformer model to use (default: all-mpnet-base-v2)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.isdir(args.resumes_dir):
        print(f"Error: Resumes directory '{args.resumes_dir}' does not exist.")
        return 1
    
    if not os.path.isfile(args.job_json):
        print(f"Error: Job JSON file '{args.job_json}' does not exist.")
        return 1
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Check for CUDA availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    print(f"Starting MPNet-based AI Resume Ranker...")
    print(f"Model: {args.model}")
    print(f"Resumes directory: {args.resumes_dir}")
    print(f"Job requirements: {args.job_json}")
    print(f"Output directory: {args.output_dir}")
    print("Processing...")
    
    # Run the ranking process
    generator = MPNetOutputGenerator()
    output_files = generator.run_ranking_process(
        args.resumes_dir,
        args.job_json,
        args.output_dir
    )
    
    # Print results
    print("\nRanking completed successfully!")
    print(f"Results table saved to: {output_files['results_table']}")
    print(f"Detailed reports saved to directory: {os.path.dirname(output_files['detailed_reports'][0])}")
    print(f"Number of resumes processed: {len(output_files['detailed_reports'])}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
