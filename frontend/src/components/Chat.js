import React, { useState, useRef, useEffect } from 'react';
import { sendMessageToAgent } from '../services/api';
import styles from './Chat.module.css';

const renderAgentMessageContent = (content) => {
  try {
    const data = JSON.parse(content);
    // Check if it's an array of objects with 'id', 'description', 'status'
    if (Array.isArray(data) && data.every((item) => item.id && item.description && item.status)) {
      if (data.length === 0) {
        return <p className={styles.noTasks}>No tasks found.</p>;
      }
      return (
        <ul className={styles.taskList}>
          {data.map((task) => (
            <li 
              key={task.id} 
              className={`${styles.taskItem} ${task.status === 'completed' ? styles.completed : ''}`}
            >
              <span className={styles.taskIcon}>
                {task.status === 'completed' ? '✅' : '⏳'}
              </span>
              <span>
                {task.description} <span style={{ opacity: 0.6 }}>(ID: {task.id})</span>
              </span>
            </li>
          ))}
        </ul>
      );
    }
  } catch (e) {
    // Not a JSON string, or not a task list format
  }
  return <p>{content}</p>;
};

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationHistory, setConversationHistory] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() && !loading) {
      const userMessage = { type: 'user', text: input };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      const currentInput = input;
      setInput('');
      setLoading(true);

      try {
        const result = await sendMessageToAgent(currentInput, conversationHistory);
        setMessages((prevMessages) => [...prevMessages, { type: 'agent', text: result.response }]);
        setConversationHistory(result.conversationHistory);
      } catch (error) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { type: 'agent', text: 'Error: Could not connect to the agent. Please check if the backend is running.' },
        ]);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSend();
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messagesArea}>
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`${styles.messageWrapper} ${styles[msg.type]}`}
          >
            <div className={`${styles.messageBubble} ${styles[msg.type]}`}>
              {msg.type === 'agent' ? renderAgentMessageContent(msg.text) : msg.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className={`${styles.messageWrapper} ${styles.agent}`}>
            <div className={`${styles.messageBubble} ${styles.agent}`}>
              <div className={styles.loadingIndicator}>
                <span>Agent is thinking</span>
                <div className={styles.typingDots}>
                  <span className={styles.dot}></span>
                  <span className={styles.dot}></span>
                  <span className={styles.dot}></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className={styles.inputArea}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          className={styles.input}
          disabled={loading}
        />
        <button
          onClick={handleSend}
          className={styles.sendButton}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;