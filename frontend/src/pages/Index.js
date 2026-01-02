import React from 'react';
import Chat from '../components/Chat';
import styles from './Index.module.css';

function Index() {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>
          <span className={styles.emoji}>🤖</span> AI Todo Chatbot
        </h1>
        <p className={styles.subtitle}>
          Powered by Google Gemini • Manage your tasks with natural language
        </p>
      </div>
      <Chat />
      <footer className={styles.footer}>
        <p>Try: "Add a task to buy groceries" • "Show all tasks" • "Mark task 1 as completed"</p>
      </footer>
    </div>
  );
}

export default Index;