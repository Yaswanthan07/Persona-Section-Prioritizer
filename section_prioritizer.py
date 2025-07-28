#!/usr/bin/env python3
"""
Persona-Driven Section Prioritizer

This script processes PDF documents and prioritizes sections based on different user personas.
It extracts text from PDFs, analyzes content relevance, and outputs prioritized sections as JSON.
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
import PyPDF2
import re
from datetime import datetime
import jsonschema


class SectionPrioritizer:
    """Main class for prioritizing document sections based on personas."""
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        """
        Initialize the SectionPrioritizer.
        
        Args:
            input_dir: Directory containing PDF files to process
            output_dir: Directory to save JSON results
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Define personas and their keywords/interests
        self.personas = {
            "executive": {
                "keywords": ["strategy", "business", "revenue", "growth", "market", "leadership", "vision"],
                "priority_sections": ["executive summary", "business model", "market analysis", "financial projections"]
            },
            "technical": {
                "keywords": ["technology", "implementation", "architecture", "code", "development", "technical", "api"],
                "priority_sections": ["technical architecture", "implementation details", "code examples", "system design"]
            },
            "marketing": {
                "keywords": ["marketing", "brand", "customer", "user", "growth", "acquisition", "engagement"],
                "priority_sections": ["marketing strategy", "user acquisition", "customer journey", "brand positioning"]
            },
            "investor": {
                "keywords": ["investment", "funding", "financial", "roi", "valuation", "exit", "returns"],
                "priority_sections": ["financial projections", "business model", "market opportunity", "investment thesis"]
            }
        }
        
        # JSON Schema for validation
        self.json_schema = {
            "type": "object",
            "required": ["document", "persona", "job_to_be_done", "processing_timestamp", "total_sections", "sections"],
            "properties": {
                "document": {"type": "string"},
                "persona": {"type": "string", "enum": ["executive", "technical", "marketing", "investor"]},
                "job_to_be_done": {"type": "string"},
                "processing_timestamp": {"type": "string", "format": "date-time"},
                "total_sections": {"type": "integer", "minimum": 0},
                "sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["title", "content", "page_number", "importance_rank", "relevance_score"],
                        "properties": {
                            "title": {"type": "string", "minLength": 1},
                            "content": {"type": "string", "minLength": 1},
                            "page_number": {"type": "integer", "minimum": 1},
                            "importance_rank": {"type": "integer", "minimum": 1},
                            "relevance_score": {"type": "number", "minimum": 0, "maximum": 1}
                        }
                    }
                }
            }
        }
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text content
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common PDF artifacts and unwanted characters
        # Keep alphanumeric, basic punctuation, and common symbols
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\"\']', '', text)
        
        # Remove excessive punctuation
        text = re.sub(r'\.{2,}', '.', text)
        text = re.sub(r'\!{2,}', '!', text)
        text = re.sub(r'\?{2,}', '?', text)
        
        # Ensure proper spacing around punctuation
        text = re.sub(r'\s+([\.\,\;\:\!\?])', r'\1', text)
        
        # Limit consecutive spaces
        text = re.sub(r'\s{2,}', ' ', text)
        
        return text.strip()
    
    def extract_sections(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract sections from the document text.
        
        Args:
            text: Document text content
            
        Returns:
            List of sections with their content and metadata
        """
        # Simple section extraction based on common patterns
        # This can be enhanced with more sophisticated NLP techniques
        
        sections = []
        lines = text.split('\n')
        current_section = {"title": "Introduction", "content": "", "page_number": 1}
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers (simple heuristic)
            if (line.isupper() or 
                re.match(r'^\d+\.\s+[A-Z]', line) or 
                re.match(r'^[A-Z][a-z]+.*:$', line) or
                len(line) < 100 and line.endswith(':')):
                
                # Save previous section
                if current_section["content"].strip():
                    current_section["content"] = self.clean_text(current_section["content"])
                    current_section["title"] = self.clean_text(current_section["title"])
                    sections.append(current_section)
                
                # Start new section
                current_section = {
                    "title": line.rstrip(':'),
                    "content": "",
                    "page_number": (i // 50) + 1  # Rough page estimation
                }
            else:
                current_section["content"] += line + "\n"
        
        # Add the last section
        if current_section["content"].strip():
            current_section["content"] = self.clean_text(current_section["content"])
            current_section["title"] = self.clean_text(current_section["title"])
            sections.append(current_section)
        
        # Filter out sections with empty or invalid content
        valid_sections = []
        for section in sections:
            if (section["title"].strip() and 
                section["content"].strip() and 
                len(section["content"]) > 10):  # Minimum content length
                valid_sections.append(section)
        
        return valid_sections
    
    def calculate_section_score(self, section: Dict[str, Any], persona: str) -> float:
        """
        Calculate relevance score for a section based on persona.
        
        Args:
            section: Section dictionary with title and content
            persona: Target persona name
            
        Returns:
            Relevance score (0-1)
        """
        if persona not in self.personas:
            return 0.0
        
        persona_config = self.personas[persona]
        keywords = persona_config["keywords"]
        priority_sections = persona_config["priority_sections"]
        
        # Check title relevance
        title_lower = section["title"].lower()
        title_score = 0.0
        
        for keyword in keywords:
            if keyword.lower() in title_lower:
                title_score += 0.3
        
        # Check content relevance
        content_lower = section["content"].lower()
        content_score = 0.0
        
        for keyword in keywords:
            count = content_lower.count(keyword.lower())
            content_score += min(count * 0.1, 0.5)  # Cap at 0.5 per keyword
        
        # Check if it's a priority section
        priority_bonus = 0.0
        for priority_section in priority_sections:
            if priority_section.lower() in title_lower:
                priority_bonus = 0.2
                break
        
        total_score = min(title_score + content_score + priority_bonus, 1.0)
        return total_score
    
    def prioritize_sections(self, sections: List[Dict[str, Any]], persona: str) -> List[Dict[str, Any]]:
        """
        Prioritize sections based on persona relevance.
        
        Args:
            sections: List of sections
            persona: Target persona
            
        Returns:
            Prioritized list of sections with explicit ranking
        """
        scored_sections = []
        
        for section in sections:
            score = self.calculate_section_score(section, persona)
            scored_section = section.copy()
            scored_section["relevance_score"] = score
            scored_sections.append(scored_section)
        
        # Sort by relevance score (descending)
        scored_sections.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Add explicit importance rank (1, 2, 3, ...)
        for i, section in enumerate(scored_sections):
            section["importance_rank"] = i + 1
            # Ensure relevance_score is a float with 2 decimal places
            section["relevance_score"] = round(float(section["relevance_score"]), 2)
        
        return scored_sections
    
    def validate_sections(self, sections: List[Dict[str, Any]]) -> List[str]:
        """
        Validate sections for consistency and completeness.
        
        Args:
            sections: List of sections to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Check for sequential importance_rank
        expected_ranks = set(range(1, len(sections) + 1))
        actual_ranks = set()
        
        for i, section in enumerate(sections):
            # Check required fields
            required_fields = ["title", "content", "page_number", "importance_rank", "relevance_score"]
            for field in required_fields:
                if field not in section:
                    errors.append(f"Section {i+1} missing required field: {field}")
            
            # Check field types and values
            if "importance_rank" in section:
                if not isinstance(section["importance_rank"], int):
                    errors.append(f"Section {i+1} importance_rank must be integer, got {type(section['importance_rank'])}")
                else:
                    actual_ranks.add(section["importance_rank"])
            
            if "relevance_score" in section:
                if not isinstance(section["relevance_score"], (int, float)):
                    errors.append(f"Section {i+1} relevance_score must be number, got {type(section['relevance_score'])}")
                elif not (0 <= section["relevance_score"] <= 1):
                    errors.append(f"Section {i+1} relevance_score must be between 0 and 1, got {section['relevance_score']}")
            
            if "page_number" in section:
                if not isinstance(section["page_number"], int) or section["page_number"] < 1:
                    errors.append(f"Section {i+1} page_number must be positive integer, got {section['page_number']}")
            
            # Check content quality
            if "title" in section and (not section["title"].strip() or len(section["title"]) < 2):
                errors.append(f"Section {i+1} title is too short or empty")
            
            if "content" in section and (not section["content"].strip() or len(section["content"]) < 10):
                errors.append(f"Section {i+1} content is too short or empty")
        
        # Check for sequential ranking
        if expected_ranks != actual_ranks:
            errors.append(f"Importance ranks are not sequential: expected {expected_ranks}, got {actual_ranks}")
        
        return errors
    
    def validate_json_structure(self, data: Dict[str, Any]) -> List[str]:
        """
        Validate JSON structure against schema.
        
        Args:
            data: JSON data to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        try:
            jsonschema.validate(instance=data, schema=self.json_schema)
        except jsonschema.exceptions.ValidationError as e:
            errors.append(f"JSON Schema validation error: {e.message}")
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
        
        return errors
    
    def process_document(self, pdf_path: Path, persona: str = "executive") -> Dict[str, Any]:
        """
        Process a single PDF document for a specific persona.
        
        Args:
            pdf_path: Path to the PDF file
            persona: Target persona for prioritization
            
        Returns:
            Dictionary containing processing results
        """
        print(f"Processing {pdf_path.name} for {persona} persona...")
        
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return {"error": f"Could not extract text from {pdf_path.name}"}
        
        # Extract sections
        sections = self.extract_sections(text)
        
        # Prioritize sections
        prioritized_sections = self.prioritize_sections(sections, persona)
        
        # Take top 10 most relevant sections
        top_sections = prioritized_sections[:10]
        
        # Validate sections
        section_errors = self.validate_sections(top_sections)
        if section_errors:
            print(f"Warning: Section validation errors in {pdf_path.name}:")
            for error in section_errors:
                print(f"  - {error}")
        
        # Prepare results with improved structure
        results = {
            "document": pdf_path.name,
            "persona": persona,
            "job_to_be_done": f"Prioritize document sections for {persona} persona based on relevance and importance",
            "processing_timestamp": datetime.now().isoformat(),
            "total_sections": len(sections),
            "sections": top_sections
        }
        
        # Validate JSON structure
        json_errors = self.validate_json_structure(results)
        if json_errors:
            print(f"Warning: JSON structure validation errors in {pdf_path.name}:")
            for error in json_errors:
                print(f"  - {error}")
        
        return results
    
    def process_all_documents(self, persona: str = "executive") -> List[Dict[str, Any]]:
        """
        Process all PDF documents in the input directory.
        
        Args:
            persona: Target persona for prioritization
            
        Returns:
            List of processing results for all documents
        """
        results = []
        
        # Find all PDF files in input directory
        pdf_files = list(self.input_dir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {self.input_dir}")
            return results
        
        for pdf_path in pdf_files:
            result = self.process_document(pdf_path, persona)
            results.append(result)
            
            # Save individual result
            output_file = self.output_dir / f"{pdf_path.stem}_{persona}_prioritized.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Save combined results
        combined_output = self.output_dir / f"all_documents_{persona}_prioritized.json"
        with open(combined_output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Processed {len(pdf_files)} documents. Results saved to {self.output_dir}")
        return results


def main():
    """Main function to run the section prioritizer."""
    parser = argparse.ArgumentParser(description="Persona-Driven Section Prioritizer")
    parser.add_argument("--persona", choices=["executive", "technical", "marketing", "investor"], 
                       default="executive", help="Target persona for prioritization")
    parser.add_argument("--input-dir", default="input", help="Input directory containing PDFs")
    parser.add_argument("--output-dir", default="output", help="Output directory for JSON results")
    
    args = parser.parse_args()
    
    # Initialize prioritizer
    prioritizer = SectionPrioritizer(args.input_dir, args.output_dir)
    
    # Process all documents
    results = prioritizer.process_all_documents(args.persona)
    
    # Print summary
    print(f"\nProcessing complete for {args.persona} persona!")
    print(f"Results saved to: {args.output_dir}")


if __name__ == "__main__":
    main() 