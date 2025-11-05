# Meme Generator API 🎨

A powerful FastAPI backend service for generating memes with AI integration. Supports both direct API calls and autonomous meme generation through LLM function calling (Gemini/Gemma).

## 🌟 Features

- **RESTful API** for meme generation
- **AI Integration** with Google Gemini for natural language meme creation
- **Pillow-based** image processing for text overlay
- **Template Management** system
- **Function Calling** support for LLM autonomous operation
- **Static File Serving** for generated memes
- **Comprehensive API Documentation** with Swagger UI

## 📋 Requirements

- Python 3.9+
- FastAPI
- Pillow (PIL)
- Google Generative AI SDK
- Uvicorn

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd meme-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
APP_NAME=Meme Generator API
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 3. Add Meme Templates

Place your meme template images in `app/static/templates/`:

```bash
mkdir -p app/static/templates
# Add your template images (e.g., distracted_boyfriend.jpg, drake.png)
```

### 4. Run the Server

```bash
# Using the run script
python run.py

# Or directly with uvicorn
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 API Endpoints

### Health Check
```http
GET /health
```

### Get Available Templates
```http
GET /api/meme/templates
```

### Generate Meme (Direct)
```http
POST /api/meme/generate
Content-Type: application/json

{
  "template_name": "distracted_boyfriend",
  "top_text": "Me",
  "bottom_text": "New Framework",
  "font_size": 40
}
```

### Generate Meme (AI-Powered)
```http
POST /api/meme/generate-with-ai?prompt=Create a distracted boyfriend meme about choosing Python over Java
```

## 🤖 LLM Integration

The API supports function calling for autonomous meme generation by LLMs. The AI can:

1. Understand natural language requests
2. Choose appropriate meme templates
3. Generate relevant text
4. Call the meme generation function automatically

### Example Usage

```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")
model = genai.GenerativeModel('gemini-pro')

prompt = "Create a meme about debugging at 3am"
response = model.generate_content(prompt, tools=[...])
```

## 📁 Project Structure

```
meme-generator/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── api/                    # API routes
│   │   ├── routes_meme.py      # Meme generation endpoints
│   │   └── routes_health.py    # Health check endpoints
│   ├── models/                 # Pydantic models
│   │   ├── meme_models.py      # Request/Response models
│   │   └── tool_schema.py      # LLM function schemas
│   ├── services/               # Business logic
│   │   └── meme_service.py     # Meme generation service
│   ├── utils/                  # Utilities
│   │   ├── image_utils.py      # Image processing helpers
│   │   └── ai_client.py        # AI client wrapper
│   ├── config/                 # Configuration
│   │   └── settings.py         # App settings
│   └── static/                 # Static files
│       ├── templates/          # Meme templates (add your images here)
│       └── memes/              # Generated memes
├── tests/                      # Test suite
│   └── test_meme_generator.py
├── .env                        # Environment variables
├── .gitignore
├── requirements.txt
├── README.md
└── run.py                      # Application entry point
```

## 🎨 Customization

### Adding New Templates

1. Add your image file to `app/static/templates/`
2. Name it descriptively (e.g., `distracted_boyfriend.jpg`)
3. The template will be automatically available via the API

### Styling Options

Configure meme text styling in your request:

```json
{
  "template_name": "drake",
  "top_text": "Old way",
  "bottom_text": "New way",
  "font_size": 50,
  "font_color": "white",
  "stroke_color": "black",
  "stroke_width": 3
}
```

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## 🔒 Security Notes

- Never commit your `.env` file with real API keys
- Configure CORS appropriately for production
- Implement rate limiting for production deployments
- Validate and sanitize all user inputs
- Set appropriate file size limits

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google AI API key | Required |
| `APP_NAME` | Application name | "Meme Generator API" |
| `DEBUG` | Debug mode | True |
| `HOST` | Server host | "0.0.0.0" |
| `PORT` | Server port | 8000 |
| `MEME_OUTPUT_DIR` | Output directory for memes | "app/static/memes" |
| `MAX_IMAGE_SIZE` | Max upload size in bytes | 10485760 |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Pillow for image processing capabilities
- Google Generative AI for LLM integration

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ and Python