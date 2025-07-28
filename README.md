# Persona-Driven Section Prioritizer

A sophisticated Python application that intelligently analyzes PDF documents and prioritizes sections based on different user personas. This tool extracts structured content from PDFs, applies persona-specific relevance scoring, and outputs prioritized sections in a clean JSON format.

## 🎯 Overview

The Persona-Driven Section Prioritizer transforms how you interact with PDF documents by:

- **Intelligently extracting** document sections and structure
- **Applying persona-specific** relevance scoring algorithms
- **Generating prioritized** section rankings based on user context
- **Outputting clean JSON** for easy integration and analysis

## 🚀 Features

### Multi-Persona Support
- **Executive**: Focuses on strategy, business, revenue, growth, and leadership
- **Technical**: Prioritizes technology, implementation, architecture, and development
- **Marketing**: Emphasizes marketing, brand, customer, and user acquisition
- **Investor**: Concentrates on investment, funding, financial projections, and ROI

### Advanced Text Processing
- Intelligent PDF text extraction with PyPDF2
- Sophisticated section detection and parsing
- Advanced text cleaning and normalization
- Removal of PDF artifacts and formatting noise

### Comprehensive Validation
- JSON Schema validation for output compliance
- Section consistency and completeness checks
- Sequential importance ranking validation
- Content quality and length validation

### High-Quality Output
- Clean, structured JSON format
- Explicit importance rankings (1, 2, 3, ...)
- Relevance scores with 2-decimal precision
- Comprehensive metadata including timestamps

## 📁 Project Structure

```
Persona-Driven Section Prioritizer/
├── app/
│   ├── input/                 # Place your PDF files here
│   │   └── Adobe Hack Doc.pdf
│   ├── output/                # Generated JSON results
│   │   └── *.json
│   ├── section_prioritizer.py # Main application
│   └── requirements.txt       # Python dependencies
└── README.md
```

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup
1. **Clone or download** the project to your local machine

2. **Navigate to the project directory**
   ```bash
   cd "Persona-Driven Section Prioritizer"
   ```

3. **Install dependencies**
   ```bash
   cd app
   pip install -r requirements.txt
   ```

## 📖 Usage

### Basic Usage

1. **Place your PDF files** in the `app/input/` directory

2. **Run the prioritizer** with default settings (Executive persona):
   ```bash
   python section_prioritizer.py
   ```

3. **Find your results** in the `app/output/` directory

### Advanced Usage

#### Specify a Different Persona
```bash
# For Technical persona
python section_prioritizer.py --persona technical

# For Marketing persona
python section_prioritizer.py --persona marketing

# For Investor persona
python section_prioritizer.py --persona investor
```

#### Custom Input/Output Directories
```bash
python section_prioritizer.py --input-dir /path/to/pdfs --output-dir /path/to/results
```

#### Available Personas
- `executive` - Business strategy and leadership focus
- `technical` - Technology and implementation focus
- `marketing` - Marketing and customer focus
- `investor` - Financial and investment focus

## 📊 Output Format

The application generates structured JSON output with the following format:

```json
{
  "document": "filename.pdf",
  "persona": "executive",
  "job_to_be_done": "Prioritize document sections for executive persona based on relevance and importance",
  "processing_timestamp": "2024-01-15T10:30:45.123456",
  "total_sections": 15,
  "sections": [
    {
      "title": "Executive Summary",
      "content": "Cleaned and normalized content...",
      "page_number": 1,
      "importance_rank": 1,
      "relevance_score": 0.85
    },
    {
      "title": "Business Model",
      "content": "Cleaned and normalized content...",
      "page_number": 3,
      "importance_rank": 2,
      "relevance_score": 0.78
    }
  ]
}
```

### Output Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `document` | string | Original PDF filename |
| `persona` | string | Target persona used for prioritization |
| `job_to_be_done` | string | Processing purpose description |
| `processing_timestamp` | string | ISO format timestamp |
| `total_sections` | integer | Total sections found in document |
| `sections` | array | Prioritized sections (top 10) |

### Section Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Section title (cleaned) |
| `content` | string | Section content (cleaned) |
| `page_number` | integer | Estimated page number |
| `importance_rank` | integer | Sequential ranking (1, 2, 3, ...) |
| `relevance_score` | float | Relevance score (0.0-1.0) |

## 🔧 Configuration

### Persona Keywords
Each persona is configured with specific keywords and priority sections:

**Executive Persona:**
- Keywords: strategy, business, revenue, growth, market, leadership, vision
- Priority sections: executive summary, business model, market analysis, financial projections

**Technical Persona:**
- Keywords: technology, implementation, architecture, code, development, technical, api
- Priority sections: technical architecture, implementation details, code examples, system design

**Marketing Persona:**
- Keywords: marketing, brand, customer, user, growth, acquisition, engagement
- Priority sections: marketing strategy, user acquisition, customer journey, brand positioning

**Investor Persona:**
- Keywords: investment, funding, financial, roi, valuation, exit, returns
- Priority sections: financial projections, business model, market opportunity, investment thesis

## 🧪 Validation Features

The application includes comprehensive validation to ensure output quality:

- **JSON Schema Validation**: Ensures output matches specification
- **Section Validation**: Checks for required fields and data types
- **Ranking Validation**: Verifies sequential importance rankings
- **Content Validation**: Ensures clean, readable content
- **Type Validation**: Confirms proper data types for all fields

## 📝 Example Output

Here's a sample output from processing a document with the executive persona:

```json
{
  "document": "Adobe Hack Doc.pdf",
  "persona": "executive",
  "job_to_be_done": "Prioritize document sections for executive persona based on relevance and importance",
  "processing_timestamp": "2024-01-15T10:30:45.123456",
  "total_sections": 19,
  "sections": [
    {
      "title": "Job-to-be-done: This will be related to the persona",
      "content": "Provide a literature review for a given topic and available research papers...",
      "page_number": 4,
      "importance_rank": 1,
      "relevance_score": 0.30
    },
    {
      "title": "Introduction",
      "content": "Welcome to the Connecting the Dots Challenge...",
      "page_number": 1,
      "importance_rank": 2,
      "relevance_score": 0.00
    }
  ]
}
```

## 🚨 Troubleshooting

### Common Issues

**No PDF files found:**
- Ensure PDF files are placed in the `app/input/` directory
- Check file extensions are `.pdf` (lowercase)

**Import errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.7+ required)

**Validation warnings:**
- These are informational and don't prevent processing
- Review warnings to understand potential content quality issues

### Performance Notes

- Processing time scales with PDF size and complexity
- Large PDFs (>50 pages) may take longer to process
- Memory usage is optimized for typical document sizes

## 🤝 Contributing

This project is designed for the Connecting the Dots Challenge. For improvements or bug reports:

1. Review the existing code structure
2. Test with various PDF types and personas
3. Ensure validation passes for all changes
4. Update documentation as needed

## 📄 License

This project is created for the Adobe Connecting the Dots Challenge.

## 🙏 Acknowledgments

- Built with PyPDF2 for PDF processing
- JSON Schema validation for output compliance
- Designed for intelligent document analysis and prioritization

---

**Ready to transform how you interact with PDF documents?** 🚀

Start by placing your PDF files in the `app/input/` directory and running the prioritizer to see the magic happen! 