#!/usr/bin/env python3
"""
Job Requirements Parser Module

This module parses job requirements from JSON format and extracts relevant information
for matching with resumes.
"""

import json
import spacy
import re
from pathlib import Path

# Load spaCy model
nlp = spacy.load('en_core_web_md')

class JobRequirementsParser:
    """
    A class to parse job requirements from JSON format and extract relevant information.
    """
    
    def __init__(self):
        """Initialize the JobRequirementsParser."""
        # Common categories for job requirements
        self.categories = {
            'education': ['degree', 'bachelor', 'master', 'phd', 'education', 'university', 'college', 'academic'],
            'experience': ['experience', 'year', 'work', 'industry', 'background', 'history'],
            'skills': ['skill', 'proficiency', 'knowledge', 'familiar', 'ability', 'capable', 'competent'],
            'tools': ['tool', 'software', 'framework', 'library', 'platform', 'system', 'technology'],
            'soft_skills': ['communication', 'teamwork', 'leadership', 'problem-solving', 'analytical', 'interpersonal']
        }
        
        # Common skills for software engineering (same as in ResumeParser)
        self.common_skills = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'html', 'css', 'sql', 'nosql', 'mongodb', 'mysql', 'postgresql', 'oracle',
            'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'devops', 'ci/cd', 'jenkins',
            'git', 'github', 'gitlab', 'bitbucket', 'agile', 'scrum', 'kanban',
            'machine learning', 'artificial intelligence', 'data science', 'big data',
            'rest api', 'graphql', 'microservices', 'testing', 'junit', 'selenium',
            'linux', 'unix', 'windows', 'macos', 'android', 'ios', 'mobile',
            'frontend', 'backend', 'fullstack', 'web development', 'mobile development',
            'database', 'networking', 'security', 'cloud', 'distributed systems',
            'algorithms', 'data structures', 'object-oriented', 'functional programming',
            'software architecture', 'design patterns', 'mvc', 'mvvm', 'rest', 'soap',
            'json', 'xml', 'yaml', 'markdown', 'documentation', 'jira', 'confluence',
            'communication', 'teamwork', 'problem-solving', 'analytical', 'critical thinking',
            'leadership', 'project management', 'time management', 'debugging',
            'performance optimization', 'scalability', 'reliability', 'maintainability',
            'code review', 'pair programming', 'mentoring', 'continuous learning',
            'snmp', 'dcim', 'networking configuration', 'embedded systems', 'iot'
        ]
    
    def load_job_requirements(self, json_path):
        """
        Load job requirements from a JSON file.
        
        Args:
            json_path (str): Path to the JSON file
            
        Returns:
            dict: Dictionary containing job requirements
        """
        try:
            with open(json_path, 'r') as json_file:
                job_data = json.load(json_file)
            return job_data
        except Exception as e:
            print(f"Error loading job requirements from {json_path}: {e}")
            return {}
    
    def extract_years_of_experience(self, text):
        """
        Extract years of experience from text.
        
        Args:
            text (str): Text to extract years of experience from
            
        Returns:
            int: Number of years of experience required, or 0 if not found
        """
        # Pattern to match years of experience (e.g., "5+ years", "3-5 years", "at least 2 years")
        pattern = re.compile(r'(\d+)(?:\+|\s*\-\s*\d+)?\s*(?:years|year|yrs|yr)')
        match = pattern.search(text.lower())
        
        if match:
            return int(match.group(1))
        
        # Check for textual representations
        if "entry level" in text.lower() or "junior" in text.lower():
            return 0
        elif "mid level" in text.lower() or "intermediate" in text.lower():
            return 2
        elif "senior" in text.lower() or "experienced" in text.lower():
            return 5
        
        return 0
    
    def extract_education_level(self, text):
        """
        Extract education level from text.
        
        Args:
            text (str): Text to extract education level from
            
        Returns:
            str: Education level (bachelor, master, phd, or "")
        """
        text_lower = text.lower()
        
        if "bachelor" in text_lower or "b.s." in text_lower or "b.a." in text_lower or "undergraduate" in text_lower:
            return "bachelor"
        elif "master" in text_lower or "m.s." in text_lower or "m.a." in text_lower or "graduate" in text_lower:
            return "master"
        elif "phd" in text_lower or "ph.d" in text_lower or "doctorate" in text_lower:
            return "phd"
        
        return ""
    
    def extract_skills_from_text(self, text):
        """
        Extract skills from text.
        
        Args:
            text (str): Text to extract skills from
            
        Returns:
            list: List of extracted skills
        """
        text_lower = text.lower()
        found_skills = []
        
        # Use spaCy for better text processing
        doc = nlp(text_lower)
        
        # Extract skills using common skills list
        for skill in self.common_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        # Use spaCy's entity recognition for additional skills
        for ent in doc.ents:
            if ent.label_ == "PRODUCT" or ent.label_ == "ORG":
                skill_candidate = ent.text.lower()
                if skill_candidate in self.common_skills and skill_candidate not in found_skills:
                    found_skills.append(skill_candidate)
        
        return found_skills
    
    def categorize_requirements(self, requirements):
        """
        Categorize job requirements into different categories.
        
        Args:
            requirements (list): List of job requirement strings
            
        Returns:
            dict: Dictionary with categorized requirements
        """
        categorized = {
            'education': [],
            'experience': [],
            'skills': [],
            'tools': [],
            'soft_skills': [],
            'other': []
        }
        
        for req in requirements:
            req_lower = req.lower()
            categorized_flag = False
            
            # Check each category
            for category, keywords in self.categories.items():
                if any(keyword in req_lower for keyword in keywords):
                    categorized[category].append(req)
                    categorized_flag = True
                    break
            
            # If not categorized, put in 'other'
            if not categorized_flag:
                categorized['other'].append(req)
        
        return categorized
    
    def extract_required_skills(self, job_data):
        """
        Extract required skills from job data.
        
        Args:
            job_data (dict): Dictionary containing job data
            
        Returns:
            list: List of required skills
        """
        skills = []
        
        # Extract skills from job_skills field
        if 'job_skills' in job_data and job_data['job_skills']:
            skills_text = job_data['job_skills']
            # Split by common separators
            for skill in re.split(r'[|,;]', skills_text):
                skill = skill.strip().lower()
                if skill and skill not in skills:
                    skills.append(skill)
        
        # Extract skills from job requirements
        if 'job_requirements' in job_data and job_data['job_requirements']:
            for req in job_data['job_requirements']:
                extracted_skills = self.extract_skills_from_text(req)
                for skill in extracted_skills:
                    if skill not in skills:
                        skills.append(skill)
        
        # Extract skills from job description
        if 'description' in job_data and job_data['description']:
            extracted_skills = self.extract_skills_from_text(job_data['description'])
            for skill in extracted_skills:
                if skill not in skills:
                    skills.append(skill)
        
        return skills
    
    def parse_job_requirements(self, json_path):
        """
        Parse job requirements from a JSON file.
        
        Args:
            json_path (str): Path to the JSON file
            
        Returns:
            dict: Dictionary containing parsed job requirements
        """
        # Load job data
        job_data = self.load_job_requirements(json_path)
        
        if not job_data:
            return {
                'job_title': '',
                'company': '',
                'required_experience_years': 0,
                'required_education': '',
                'required_skills': [],
                'categorized_requirements': {},
                'full_description': '',
                'original_data': {}
            }
        
        # Extract job title and company
        job_title = job_data.get('job_title', '')
        company = job_data.get('company', '')
        
        # Extract required experience years
        required_experience_years = 0
        if 'job_requirements' in job_data and job_data['job_requirements']:
            for req in job_data['job_requirements']:
                years = self.extract_years_of_experience(req)
                if years > required_experience_years:
                    required_experience_years = years
        
        # Extract required education
        required_education = ''
        if 'job_requirements' in job_data and job_data['job_requirements']:
            for req in job_data['job_requirements']:
                education = self.extract_education_level(req)
                if education:
                    # Prioritize higher education levels
                    if education == 'phd':
                        required_education = 'phd'
                        break
                    elif education == 'master' and required_education != 'phd':
                        required_education = 'master'
                    elif education == 'bachelor' and required_education not in ['phd', 'master']:
                        required_education = 'bachelor'
        
        # Extract required skills
        required_skills = self.extract_required_skills(job_data)
        
        # Categorize requirements
        categorized_requirements = {}
        if 'job_requirements' in job_data and job_data['job_requirements']:
            categorized_requirements = self.categorize_requirements(job_data['job_requirements'])
        
        # Get full description
        full_description = job_data.get('description', '')
        
        return {
            'job_title': job_title,
            'company': company,
            'required_experience_years': required_experience_years,
            'required_education': required_education,
            'required_skills': required_skills,
            'categorized_requirements': categorized_requirements,
            'full_description': full_description,
            'original_data': job_data
        }

# Example usage
if __name__ == "__main__":
    parser = JobRequirementsParser()
    
    # Parse job requirements
    # parsed_job = parser.parse_job_requirements("path/to/job_requirements.json")
    # print(f"Job Title: {parsed_job['job_title']}")
    # print(f"Required Experience: {parsed_job['required_experience_years']} years")
    # print(f"Required Education: {parsed_job['required_education']}")
    # print(f"Required Skills: {parsed_job['required_skills']}")
