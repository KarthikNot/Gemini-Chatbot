import axios from 'axios';

const API = axios.create({
    baseURL: 'http://127.0.0.1:8000/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Request interceptor to add auth headers
API.interceptors.request.use(
    (config) => {
        const userId = localStorage.getItem('user_id');
        if (userId) {
            config.headers['User-ID'] = userId;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
API.interceptors.response.use(
    (response) => response.data,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('user_id');
            localStorage.removeItem('username');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Authentication
export const signupUser = (data) => API.post('/signup', data);
export const loginUser = (data) => API.post('/login', data);

// Chat operations
export const newChat = (userId, title) =>
    API.post('/new_chat', { user_id: userId, title });

export const getChats = (userId) =>
    API.get(`/get_chats/${userId}`);

export const getChatHistory = (userId, chatId) =>
    API.get(`/chat/${userId}/${chatId}`);

export const sendMessage = (userId, chatId, message) =>
    API.post('/send_message', { user_id: userId, chat_id: chatId, message });

export const deleteChat = (userId, chatId) =>
    API.delete(`/chat/${userId}/${chatId}`);

export const renameChat = (userId, chatId, newTitle) =>
    API.patch(`/chat/${userId}/${chatId}/rename`, { new_title: newTitle });

// Health check
export const healthCheck = () => API.get('/health');
