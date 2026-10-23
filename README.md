# 🧠 Fake News Detector

A modern web application that uses AI to detect fake news articles. Built with Flask (backend), Next.js (frontend), and powered by HuggingFace's BART Large MNLI model.

## 🚀 Features

- **AI-Powered Detection**: Uses HuggingFace's BART Large MNLI model for zero-shot classification
- **Modern UI**: Beautiful, responsive frontend built with Next.js and Tailwind CSS
- **Real-time Analysis**: Instant prediction results with confidence scores
- **Analysis History**: Keep track of recent predictions
- **Clean API**: RESTful backend with proper error handling
- **Deployment configs**: `render.yaml` for the API and Vercel for the frontend

## 🛠️ Tech Stack

### Backend
- **Flask**: Python web framework
- **Transformers**: HuggingFace library for AI models
- **BART Large MNLI**: Pre-trained model for text classification
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library
- **React Hooks**: Modern React patterns

## 📦 Installation & Setup

### Prerequisites
- Python 3.9+ 
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Fake_News_Detection_Machine_learning_project
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run the backend server:**
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   pnpm install
   # or
   yarn install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your backend URL
   ```

4. **Run the development server:**
   ```bash
   pnpm dev
   # or
   yarn dev
   ```
   The frontend will be available at `http://localhost:3000`

## 🚀 Deployment

### Backend Deployment (Heroku)

1. **Install Heroku CLI and login:**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set HF_HOME=./hf_cache
   ```

4. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Frontend Deployment (Vercel)

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy from frontend directory:**
   ```bash
   cd frontend
   vercel
   ```

3. **Set environment variables in Vercel dashboard:**
   - `NEXT_PUBLIC_API_URL`: Your deployed backend URL

## 🧪 API Usage

### Health Check
```bash
GET /
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-29T...",
  "model": "facebook/bart-large-mnli"
}
```

### Predict News Authenticity
```bash
POST /predict
Content-Type: application/json

{
  "headline": "Breaking: Major news event",
  "text": "Full article content here..."
}
```

Response:
```json
{
  "prediction": "real",
  "confidence": 87.5,
  "analysis": {
    "text_length": 150,
    "headline": "Breaking: Major news event",
    "content_preview": "Full article content..."
  }
}
```

## 🔧 Development

### Project Structure
```
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── runtime.txt           # Python version for Heroku
├── .env                  # Backend environment variables
├── frontend/
│   ├── app/
│   │   ├── page.tsx      # Main React component
│   │   ├── layout.tsx    # App layout
│   │   └── globals.css   # Global styles
│   ├── package.json      # Node.js dependencies
│   ├── tailwind.config.ts # Tailwind configuration
│   ├── tsconfig.json     # TypeScript configuration
│   └── .env.local        # Frontend environment variables
└── news/
    └── news.csv          # Sample news data
```

### Adding New Features

1. **Backend**: Add new routes in `app.py`
2. **Frontend**: Create new components in `frontend/app/`
3. **API**: Update the API documentation in this README

### Running Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

The API tests use a stub in place of the BART model, so they run in under a second without downloading it. They cover text cleaning, the health check, predictions and input validation. GitHub Actions runs them and builds the frontend on every push.

## ⚠️ Limitations

- **Zero-shot, not trained for this task.** The API asks BART-MNLI whether the text reads more like "Real" or "Fake". It doesn't check facts or sources, and it hasn't been evaluated on a labelled fake-news dataset.
- **Confidence is the model's label preference,** not the probability that the article is true.
- The notebooks explore models trained on `news/news.csv`; the API doesn't use them.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**BreyeFoka** with assistance from **GitHub Copilot**

## 🙏 Acknowledgments

- HuggingFace for the amazing BART model
- The open-source community
- All contributors and testers

## 📞 Support

If you have any questions or need help, please:
1. Check the [Issues](../../issues) page
2. Create a new issue if needed
3. Contact the maintainer

---

Made with 💜 by BreyeFoka & GitHub Copilot
