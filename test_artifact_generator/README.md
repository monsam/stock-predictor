# Test Artifact Generator

A comprehensive Flask web application that automatically generates test documentation from project requirements, UX mockups, and templates using AI.

## Features

### 🔧 **File Processing**
- **Multi-format Support**: PDF, DOCX, TXT, PNG, JPG, JPEG
- **OCR Integration**: Extract text from images using Tesseract
- **Document Parsing**: Intelligent extraction from various document types

### 🤖 **AI-Powered Generation**
- **Test Cases**: Functional, non-functional, edge cases, and integration tests
- **Test Plans**: Comprehensive strategies, schedules, and resource requirements
- **Test Reports**: Execution summaries, defect analysis, and recommendations

### 📊 **Output Generation**
- **PDF Reports**: Professional downloadable test documentation
- **JSON Data**: Structured data for further processing
- **Multiple Formats**: Test cases, plans, and reports in various formats

## Quick Start

### Prerequisites
- Python 3.7+
- Tesseract OCR (for image processing)
- OpenAI API Key (for AI generation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd test_artifact_generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   - **macOS**: `brew install tesseract`
   - **Ubuntu**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

4. **Configure environment**
   ```bash
   cp env_example.txt .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   python start.py
   ```

6. **Access the application**
   - Open browser and go to: `http://localhost:5000`
   - Upload your documents and generate test artifacts

## Usage

### 1. Upload Documents
- **Requirements Document**: Project specifications and requirements
- **UX Mockups**: Design files and user interface mockups
- **Templates**: Existing test templates or documentation

### 2. Generate Test Artifacts
- **Test Cases**: Detailed test scenarios with steps and expected results
- **Test Plans**: Comprehensive testing strategies and schedules
- **Test Reports**: Execution summaries and defect analysis

### 3. Download Results
- **PDF Reports**: Professional test documentation
- **JSON Data**: Structured data for integration with other tools

## Project Structure

```
test_artifact_generator/
├── app.py                 # Main Flask application
├── start.py              # Startup script with dependency checks
├── requirements.txt      # Python dependencies
├── env_example.txt      # Environment variables template
├── templates/           # HTML templates
│   └── index.html      # Main web interface
├── uploads/            # Uploaded files storage
└── outputs/            # Generated PDF reports
```

## API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload and process documents
- `GET /download/<session_id>/<artifact_type>` - Download generated PDFs
- `GET /results/<session_id>` - Get processing results

## Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Supported File Types
- **Documents**: PDF, DOCX, DOC, TXT
- **Images**: PNG, JPG, JPEG
- **Size Limit**: Configurable upload limits

## Dependencies

### Core Dependencies
- Flask - Web framework
- OpenAI - AI text generation
- PyPDF2 - PDF processing
- python-docx - DOCX processing
- pytesseract - OCR for images
- reportlab - PDF generation
- Pillow - Image processing

### Development Dependencies
- python-dotenv - Environment management
- flask-cors - Cross-origin support
- pandas - Data processing
- numpy - Numerical operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

## Roadmap

- [ ] Multi-language support
- [ ] Custom test case templates
- [ ] Integration with test management tools
- [ ] Advanced AI models support
- [ ] Real-time collaboration features 