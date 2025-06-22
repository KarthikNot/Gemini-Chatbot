import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
    Send,
    Plus,
    Trash2,
    Edit3,
    LogOut,
    User,
    MessageSquare,
    Loader2,
    Bot,
    Menu,
    X
} from "lucide-react";
import {
    newChat,
    getChats,
    getChatHistory,
    sendMessage,
    deleteChat,
    renameChat
} from "../api";

export default function Chat() {
    const [chats, setChats] = useState([]);
    const [currentChat, setCurrentChat] = useState(null);
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [isRenaming, setIsRenaming] = useState(false);
    const [newTitle, setNewTitle] = useState("");
    const [error, setError] = useState("");

    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);
    const navigate = useNavigate();

    const userId = localStorage.getItem("user_id");
    const username = localStorage.getItem("username");

    // Auto-scroll to bottom when new messages arrive
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Load chats on component mount
    useEffect(() => {
        loadChats();
    }, []);

    // Load chat history when current chat changes
    useEffect(() => {
        if (currentChat) {
            loadChatHistory(currentChat.chat_id);
        }
    }, [currentChat]);

    const loadChats = async () => {
        try {
            const response = await getChats(userId);
            setChats(response);

            // If no current chat and chats exist, select the first one
            if (!currentChat && response.length > 0) {
                setCurrentChat(response[0]);
            }
        } catch (error) {
            console.error("Error loading chats:", error);
            setError("Failed to load chats");
        }
    };

    const loadChatHistory = async (chatId) => {
        try {
            const response = await getChatHistory(userId, chatId);
            setMessages(response);
        } catch (error) {
            console.error("Error loading chat history:", error);
            setError("Failed to load chat history");
        }
    };

    const createNewChat = async () => {
        try {
            const response = await newChat(userId, "New Chat");
            const newChatData = {
                chat_id: response.chat_id,
                title: "New Chat",
                created_at: new Date().toISOString()
            };

            setChats(prev => [newChatData, ...prev]);
            setCurrentChat(newChatData);
            setMessages([]);
            setIsSidebarOpen(false);
        } catch (error) {
            console.error("Error creating new chat:", error);
            setError("Failed to create new chat");
        }
    };

    const handleSendMessage = async () => {
        if (!inputMessage.trim() || !currentChat || isLoading) return;

        const userMessage = {
            sender: "user",
            message: inputMessage,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage("");
        setIsLoading(true);

        try {
            const response = await sendMessage(userId, currentChat.chat_id, inputMessage);

            const botMessage = {
                sender: "bot",
                message: response.response,
                timestamp: new Date().toISOString()
            };

            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error("Error sending message:", error);
            setError("Failed to send message");
        } finally {
            setIsLoading(false);
        }
    };

    const handleDeleteChat = async (chatId) => {
        if (!confirm("Are you sure you want to delete this chat?")) return;

        try {
            await deleteChat(userId, chatId);
            setChats(prev => prev.filter(chat => chat.chat_id !== chatId));

            if (currentChat?.chat_id === chatId) {
                setCurrentChat(chats.length > 1 ? chats.find(c => c.chat_id !== chatId) : null);
                setMessages([]);
            }
        } catch (error) {
            console.error("Error deleting chat:", error);
            setError("Failed to delete chat");
        }
    };

    const handleRenameChat = async () => {
        if (!newTitle.trim() || !currentChat) return;

        try {
            await renameChat(userId, currentChat.chat_id, newTitle);
            setChats(prev => prev.map(chat =>
                chat.chat_id === currentChat.chat_id
                    ? { ...chat, title: newTitle }
                    : chat
            ));
            setCurrentChat(prev => ({ ...prev, title: newTitle }));
            setIsRenaming(false);
            setNewTitle("");
        } catch (error) {
            console.error("Error renaming chat:", error);
            setError("Failed to rename chat");
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("user_id");
        localStorage.removeItem("username");
        navigate("/login");
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="h-screen flex bg-gray-50">
            {/* Sidebar */}
            <div className={`fixed inset-y-0 left-0 z-50 w-80 bg-white shadow-lg transform transition-transform duration-300 ease-in-out ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
                } lg:relative lg:translate-x-0`}>
                <div className="flex flex-col h-full">
                    {/* Header */}
                    <div className="p-4 border-b border-gray-200">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                                    <span className="text-white text-sm font-bold">AI</span>
                                </div>
                                <h1 className="text-lg font-semibold text-gray-900">AI Chat</h1>
                            </div>
                            <button
                                onClick={() => setIsSidebarOpen(false)}
                                className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
                            >
                                <X size={20} />
                            </button>
                        </div>

                        {/* User Info */}
                        <div className="mt-4 flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                            <User size={16} className="text-gray-500" />
                            <span className="text-sm text-gray-700">{username}</span>
                        </div>
                    </div>

                    {/* New Chat Button */}
                    <div className="p-4">
                        <button
                            onClick={createNewChat}
                            className="w-full flex items-center justify-center space-x-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-3 px-4 rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all"
                        >
                            <Plus size={20} />
                            <span>New Chat</span>
                        </button>
                    </div>

                    {/* Chat List */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-2">
                        {chats.map((chat) => (
                            <div
                                key={chat.chat_id}
                                className={`flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all ${currentChat?.chat_id === chat.chat_id
                                    ? 'bg-blue-50 border border-blue-200'
                                    : 'hover:bg-gray-50'
                                    }`}
                                onClick={() => setCurrentChat(chat)}
                            >
                                <div className="flex items-center space-x-3 flex-1 min-w-0">
                                    <MessageSquare size={16} className="text-gray-500 flex-shrink-0" />
                                    <span className="text-sm text-gray-700 truncate">{chat.title}</span>
                                </div>

                                {currentChat?.chat_id === chat.chat_id && (
                                    <div className="flex items-center space-x-1">
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setIsRenaming(true);
                                                setNewTitle(chat.title);
                                            }}
                                            className="p-1 hover:bg-gray-200 rounded"
                                        >
                                            <Edit3 size={14} className="text-gray-500" />
                                        </button>
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                handleDeleteChat(chat.chat_id);
                                            }}
                                            className="p-1 hover:bg-red-100 rounded"
                                        >
                                            <Trash2 size={14} className="text-red-500" />
                                        </button>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>

                    {/* Logout Button */}
                    <div className="p-4 border-t border-gray-200">
                        <button
                            onClick={handleLogout}
                            className="w-full flex items-center justify-center space-x-2 text-gray-600 hover:text-red-600 py-2 px-4 rounded-lg hover:bg-red-50 transition-all"
                        >
                            <LogOut size={16} />
                            <span>Logout</span>
                        </button>
                    </div>
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col">
                {/* Mobile Header */}
                <div className="lg:hidden p-4 border-b border-gray-200 bg-white">
                    <div className="flex items-center justify-between">
                        <button
                            onClick={() => setIsSidebarOpen(true)}
                            className="p-2 hover:bg-gray-100 rounded-lg"
                        >
                            <Menu size={20} />
                        </button>
                        <h2 className="text-lg font-semibold text-gray-900">
                            {currentChat?.title || "AI Chat"}
                        </h2>
                        <div className="w-10"></div>
                    </div>
                </div>

                {/* Chat Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {messages.length === 0 ? (
                        <div className="flex items-center justify-center h-full">
                            <div className="text-center">
                                <Bot size={48} className="text-gray-400 mx-auto mb-4" />
                                <h3 className="text-lg font-medium text-gray-900 mb-2">Start a conversation</h3>
                                <p className="text-gray-500">Send a message to begin chatting with AI</p>
                            </div>
                        </div>
                    ) : (
                        messages.map((message, index) => (
                            <div
                                key={index}
                                className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
                            >
                                <div className={`message-bubble ${message.sender} p-4 max-w-xs lg:max-w-md`}>
                                    <div className="flex items-start space-x-2">
                                        {message.sender === "bot" && (
                                            <Bot size={16} className="text-gray-500 mt-1 flex-shrink-0" />
                                        )}
                                        <div className="flex-1">
                                            <p className="text-sm whitespace-pre-wrap">{message.message}</p>
                                            <p className="text-xs text-gray-500 mt-2">
                                                {new Date(message.timestamp).toLocaleTimeString()}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}

                    {isLoading && (
                        <div className="flex justify-start">
                            <div className="message-bubble bot p-4">
                                <div className="flex items-center space-x-2">
                                    <Bot size={16} className="text-gray-500" />
                                    <Loader2 size={16} className="animate-spin text-gray-500" />
                                    <span className="text-sm text-gray-500">AI is thinking...</span>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 border-t border-gray-200 bg-white">
                    <div className="flex items-end space-x-4">
                        <div className="flex-1">
                            <textarea
                                ref={inputRef}
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Type your message..."
                                className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                rows="1"
                                disabled={isLoading || !currentChat}
                                style={{ minHeight: '44px', maxHeight: '120px' }}
                            />
                        </div>
                        <button
                            onClick={handleSendMessage}
                            disabled={!inputMessage.trim() || isLoading || !currentChat}
                            className="p-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg hover:from-blue-600 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                        >
                            <Send size={20} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Rename Modal */}
            {isRenaming && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg p-6 w-96">
                        <h3 className="text-lg font-semibold mb-4">Rename Chat</h3>
                        <input
                            type="text"
                            value={newTitle}
                            onChange={(e) => setNewTitle(e.target.value)}
                            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="Enter new title"
                        />
                        <div className="flex space-x-3 mt-4">
                            <button
                                onClick={handleRenameChat}
                                className="flex-1 bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition-colors"
                            >
                                Save
                            </button>
                            <button
                                onClick={() => {
                                    setIsRenaming(false);
                                    setNewTitle("");
                                }}
                                className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg hover:bg-gray-400 transition-colors"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
} 