# LLM Chatbot

A modern, full-stack AI chatbot application built with React, FastAPI, and Google's Gemini AI. Features user authentication, persistent chat history, and a beautiful, responsive UI.

## 🚀 Features

- **AI-Powered Conversations**: Powered by Google's Gemini 2.5 Flash model
- **User Authentication**: Secure signup and login system
- **Persistent Chat History**: All conversations are saved and retrievable
- **Multiple Chat Sessions**: Create, manage, and switch between different chat conversations
- **Real-time Messaging**: Instant AI responses with loading states
- **Modern UI/UX**: Beautiful, responsive design with Tailwind CSS and Framer Motion
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- **Error Handling**: Comprehensive error handling and user feedback
- **Logging**: Detailed request logging and error tracking

## 🏗️ Architecture

### Frontend (React + Vite)
- **Framework**: React 19 with Vite for fast development
- **Styling**: Tailwind CSS v4 for modern, utility-first styling
- **Routing**: React Router DOM for client-side navigation
- **HTTP Client**: Axios for API communication
- **Animations**: Framer Motion for smooth UI animations
- **Icons**: Lucide React for consistent iconography

### Backend (FastAPI + Python)
- **Framework**: FastAPI for high-performance API development
- **Database**: MongoDB for persistent data storage
- **AI Integration**: Google Gemini API for intelligent responses
- **Authentication**: Custom user authentication system
- **Logging**: Structured logging with request/response tracking
- **Error Handling**: Custom exception handling with proper HTTP status codes

## 📁 Project Structure

```
llm-chatbot/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── pages/           # Main page components
│   │   │   ├── Chat.jsx     # Main chat interface
│   │   │   ├── Login.jsx    # User login page
│   │   │   └── Signup.jsx   # User registration page
│   │   ├── components/      # Reusable UI components
│   │   ├── api.js          # API client configuration
│   │   ├── App.jsx         # Main app component with routing
│   │   └── main.jsx        # App entry point
│   ├── package.json        # Frontend dependencies
│   └── vite.config.js      # Vite configuration
├── backend/                 # FastAPI backend application
│   ├── api/
│   │   └── routes.py       # API route definitions
│   ├── core/
│   │   ├── config.py       # Configuration management
│   │   ├── exceptions.py   # Custom exception classes
│   │   ├── gemini.py       # Gemini AI integration
│   │   ├── logging.py      # Logging configuration
│   │   └── mongo.py        # MongoDB connection
│   ├── models/
│   │   ├── chat.py         # Chat data models
│   │   └── user.py         # User data models
│   ├── services/
│   │   ├── chat_service.py # Chat business logic
│   │   └── user_service.py # User business logic
│   ├── server.py           # FastAPI application entry point
│   └── requirements.txt    # Python dependencies
└── README.md              # This file
```

## 🛠️ Setup Instructions

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- MongoDB instance
- Google Gemini API key

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the backend directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   MONGO_API_KEY=your_mongodb_connection_string
   SECRET_KEY=your_secret_key_here
   ```

5. **Start the backend server**:
   ```bash
   python server.py
   ```
   The server will run on `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`

## 🔧 API Endpoints

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User authentication

### Chat Management
- `POST /api/new_chat` - Create a new chat session
- `GET /api/get_chats/{user_id}` - Get all user chats
- `GET /api/chat/{user_id}/{chat_id}` - Get chat history
- `POST /api/send_message` - Send a message and get AI response
- `DELETE /api/chat/{user_id}/{chat_id}` - Delete a chat
- `PATCH /api/chat/{user_id}/{chat_id}/rename` - Rename a chat

### Health Check
- `GET /health` - Server health check

## 🎨 Key Features Explained

### Chat Interface
- **Real-time Messaging**: Messages are sent instantly with loading indicators
- **Chat History**: Previous conversations are loaded automatically
- **Multiple Chats**: Users can create and manage multiple chat sessions
- **Auto-scroll**: Chat automatically scrolls to the latest message
- **Message Persistence**: All messages are saved to MongoDB

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Offline Detection**: Shows server status and retry options
- **Smooth Animations**: Framer Motion animations for better UX

### Security
- **User Authentication**: Secure login/signup system
- **Session Management**: User sessions are maintained via localStorage
- **Input Validation**: Server-side validation for all inputs
- **Error Logging**: Comprehensive error tracking and logging

## 🚀 Deployment

### Backend Deployment
The backend can be deployed to any Python hosting platform (Heroku, Railway, DigitalOcean, etc.):

1. Set environment variables on your hosting platform
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment
The frontend can be deployed to Vercel, Netlify, or any static hosting service:

1. Build the project: `npm run build`
2. Deploy the `dist` folder to your hosting platform
3. Update the API base URL in `src/api.js` to point to your deployed backend

## 🔍 Troubleshooting

### Common Issues

1. **Server Connection Error**: Ensure the backend server is running on port 8000
2. **MongoDB Connection**: Verify your MongoDB connection string in the `.env` file
3. **Gemini API Error**: Check that your Gemini API key is valid and has sufficient quota
4. **CORS Issues**: The backend is configured to allow all origins for development

### Logs
- Backend logs are stored in `backend/app.log`
- Check the logs for detailed error information
- Request/response logging is enabled by default

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI for the robust backend framework
- React and Vite for the modern frontend experience
- Tailwind CSS for the beautiful styling
- MongoDB for reliable data persistence