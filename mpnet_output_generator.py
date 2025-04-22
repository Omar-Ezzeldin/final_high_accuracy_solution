#!/usr/bin/env python3
"""
Output Generator for MPNet-based Resume Ranker

This module generates the final output for the MPNet-based AI Resume Ranker,
including a results table with resume name, match score, and email, as well as
detailed reports for each resume.
"""

import os
import json
import pandas as pd
from mpnet_resume_matcher import MPNetResumeMatcher

class MPNetOutputGenerator:
    """
    A class to generate output for the MPNet-based AI Resume Ranker results.
    """
    
    def __init__(self):
        """Initialize the MPNetOutputGenerator."""
        self.matcher = MPNetResumeMatcher()
    
    def generate_results_table(self, match_results):
        """
        Generate a results table with resume name, match score, and email.
        
        Args:
            match_results (list): List of match results from the matching algorithm
            
        Returns:
            pandas.DataFrame: DataFrame containing the results table
        """
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
        
        # Rename columns to match expected output format
        df = df.rename(columns={
            'Resume Name': 'Resume Name',
            'Match Score (%)': 'Match Score (%)',
            'Email': 'Email'
        })
        
        return df
    
    def generate_detailed_report(self, match_result):
        """
        Generate a detailed report for a single resume match.
        
        Args:
            match_result (dict): Match result for a single resume
            
        Returns:
            str: Detailed report text
        """
        report = []
        
        # Basic information
        report.append(f"# Detailed Match Report for {match_result['resume_name']}")
        report.append(f"Email: {match_result['email']}")
        report.append(f"Overall Match Score: {match_result['match_score']}%")
        report.append("")
        
        # Get match details
        match_details = match_result['match_details']
        
        # Skills match
        skills_details = match_details['skills']
        report.append("## Skills Match")
        report.append(f"Score: {skills_details['score']}% (Weight: {skills_details['weight']}%)")
        
        report.append("\n### Direct Matching Skills:")
        if skills_details.get('direct_matches'):
            for skill in skills_details['direct_matches']:
                report.append(f"- {skill}")
        else:
            report.append("- No direct skill matches found")
        
        # Add semantic matches if available
        if 'semantic_matches' in skills_details and skills_details['semantic_matches']:
            report.append("\n### Semantically Similar Skills:")
            for job_skill, resume_skill, score in skills_details['semantic_matches']:
                report.append(f"- {job_skill} (matched with {resume_skill}, similarity: {score}%)")
        
        # Add missing skills if available
        if 'missing_skills' in skills_details and skills_details['missing_skills']:
            report.append("\n### Missing Skills:")
            for skill in skills_details['missing_skills']:
                report.append(f"- {skill}")
        
        # Experience match
        experience_details = match_details['experience']
        report.append("\n## Experience Match")
        report.append(f"Score: {experience_details['score']}% (Weight: {experience_details['weight']}%)")
        
        # Add experience details
        if 'estimated_years' in experience_details:
            report.append(f"Estimated Experience: {experience_details['estimated_years']} years")
            report.append(f"Required Experience: {experience_details['required_years']} years")
            report.append(f"Experience Level: {experience_details['experience_level']}")
        else:
            report.append(f"Required Years of Experience: {experience_details.get('required_years', 'Not specified')}")
        
        # Education match
        education_details = match_details['education']
        report.append("\n## Education Match")
        report.append(f"Score: {education_details['score']}% (Weight: {education_details['weight']}%)")
        
        # Add education details
        if 'detected_level' in education_details:
            report.append(f"Detected Education Level: {education_details['detected_level']}")
            report.append(f"Required Education Level: {education_details['required_level']}")
            if education_details.get('field_match'):
                # Use plain text checkmark instead of Unicode character
                report.append("(Checkmark) Relevant field of study detected")
        else:
            report.append(f"Required Education Level: {education_details.get('required_level', 'Not specified')}")
        
        # Semantic similarity
        semantic_details = match_details['semantic_similarity']
        report.append("\n## Semantic Content Similarity")
        report.append(f"Score: {semantic_details['score']}% (Weight: {semantic_details['weight']}%)")
        report.append("This score represents how well the overall content of the resume matches the job description semantically.")
        
        # Keyword relevance
        keyword_details = match_details['keyword_relevance']
        report.append("\n## Keyword Relevance")
        report.append(f"Score: {keyword_details['score']}% (Weight: {keyword_details['weight']}%)")
        report.append("This score measures how well the resume contains key terms and concepts from the job description.")
        
        # Recommendations
        report.append("\n## Recommendations")
        if match_result['match_score'] >= 80:
            report.append("This candidate is an excellent match for the position. Consider scheduling an interview as a top priority.")
        elif match_result['match_score'] >= 70:
            report.append("This candidate is a strong match for the position. Recommended for interview.")
        elif match_result['match_score'] >= 60:
            report.append("This candidate is a good match for the position. Consider reviewing their application further.")
        elif match_result['match_score'] >= 50:
            report.append("This candidate is a moderate match for the position. May be worth considering if top candidates are unavailable.")
        else:
            report.append("This candidate may not be the best match for this specific position.")
        
        # Areas for improvement
        report.append("\n### Areas for Improvement:")
        improvements = []
        
        # Check each component for low scores
        if skills_details['score'] < 60:
            improvements.append("- **Skills**: The candidate's skills do not strongly align with the job requirements.")
            if 'missing_skills' in skills_details and skills_details['missing_skills']:
                improvements.append(f"  - Consider focusing on these key missing skills: {', '.join(skills_details['missing_skills'][:3])}")
        
        if experience_details['score'] < 60:
            improvements.append("- **Experience**: The candidate may not have sufficient relevant experience for this role.")
            if 'estimated_years' in experience_details and 'required_years' in experience_details:
                if experience_details['estimated_years'] < experience_details['required_years']:
                    improvements.append(f"  - The position requires {experience_details['required_years']} years of experience, but the candidate has approximately {experience_details['estimated_years']} years.")
        
        if education_details['score'] < 60:
            improvements.append("- **Education**: The candidate's education may not meet the requirements for this position.")
            if 'detected_level' in education_details and 'required_level' in education_details:
                improvements.append(f"  - The position requires a {education_details['required_level']} degree, but the candidate has a {education_details['detected_level']} degree.")
        
        if semantic_details['score'] < 60:
            improvements.append("- **Content Relevance**: The resume content does not strongly align with the job description.")
        
        if improvements:
            report.extend(improvements)
        else:
            report.append("- No significant areas for improvement identified.")
        
        return "\n".join(report)
    
    def save_results_table(self, match_results, output_file):
        """
        Save the results table to a CSV file.
        
        Args:
            match_results (list): List of match results from the matching algorithm
            output_file (str): Path to the output CSV file
            
        Returns:
            str: Path to the saved CSV file
        """
        # Generate results table
        df = self.generate_results_table(match_results)
        
        # Fix: Ensure column names match exactly what's expected
        df.columns = ['Resume Name', 'Match Score (%)', 'Email']
        
        # Save to CSV with UTF-8 encoding
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        return output_file
    
    def save_detailed_reports(self, match_results, output_dir):
        """
        Save detailed reports for each resume to individual markdown files.
        
        Args:
            match_results (list): List of match results from the matching algorithm
            output_dir (str): Directory to save the reports
            
        Returns:
            list: List of paths to the saved report files
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        report_files = []
        for result in match_results:
            # Generate report
            report = self.generate_detailed_report(result)
            
            # Create filename from resume name
            resume_name = os.path.splitext(result['resume_name'])[0]
            safe_name = "".join([c if c.isalnum() else "_" for c in resume_name])
            report_file = os.path.join(output_dir, f"{safe_name}_report.md")
            
            # Save report with UTF-8 encoding
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            report_files.append(report_file)
        
        return report_files
    
    def run_ranking_process(self, resumes_dir, job_json_path, output_dir):
        """
        Run the complete ranking process and generate all outputs.
        
        Args:
            resumes_dir (str): Path to directory containing resumes
            job_json_path (str): Path to job requirements JSON file
            output_dir (str): Directory to save the outputs
            
        Returns:
            dict: Dictionary containing paths to all output files
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Match resumes with job
        match_results = self.matcher.match_resumes_with_job(resumes_dir, job_json_path)
        
        # Save results table
        results_table_path = os.path.join(output_dir, "results_table.csv")
        self.save_results_table(match_results, results_table_path)
        
        # Save detailed reports
        reports_dir = os.path.join(output_dir, "detailed_reports")
        report_files = self.save_detailed_reports(match_results, reports_dir)
        
        # Save match results as JSON for further processing if needed
        results_json_path = os.path.join(output_dir, "match_results.json")
        with open(results_json_path, 'w', encoding='utf-8') as f:
            # Convert match results to serializable format
            serializable_results = []
            for result in match_results:
                serializable_result = {
                    'resume_name': result['resume_name'],
                    'email': result['email'],
                    'match_score': result['match_score'],
                    'match_details': result['match_details']
                }
                serializable_results.append(serializable_result)
            
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        return {
            'results_table': results_table_path,
            'detailed_reports': report_files,
            'results_json': results_json_path
        }

# Example usage
if __name__ == "__main__":
    generator = MPNetOutputGenerator()
    
    # Run ranking process
    # output_files = generator.run_ranking_process(
    #     "path/to/resumes",
    #     "path/to/job.json",
    #     "path/to/output"
    # )
    # print(f"Results table saved to: {output_files['results_table']}")
    # print(f"Detailed reports saved to: {', '.join(output_files['detailed_reports'])}")
    # print(f"Results JSON saved to: {output_files['results_json']}")
