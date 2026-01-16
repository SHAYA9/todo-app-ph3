import React, { useState, useEffect } from 'react';
import Chat from '../components/Chat';
import Auth from '../components/Auth';
import { useSession, signOut } from '../lib/auth-client';
import styles from './Index.module.css';

function Index() {
  const { data: session, isPending } = useSession();
  const [showAuth, setShowAuth] = useState(false);

  useEffect(() => {
    if (!isPending && !session) {
      setShowAuth(true);
    } else if (session) {
      setShowAuth(false);
    }
  }, [session, isPending]);

  const handleSignOut = async () => {
    await signOut();
    setShowAuth(true);
  };

  if (isPending) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.spinner}></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (showAuth) {
    return <Auth onAuthSuccess={() => setShowAuth(false)} />;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.headerContent}>
          <div>
            <h1 className={styles.title}>
              <span className={styles.emoji}>🤖</span> AI Todo Chatbot
            </h1>
            <p className={styles.subtitle}>
              Powered by Xpertsphere • Manage your tasks with natural language
            </p>
          </div>
          <div className={styles.userInfo}>
            <span className={styles.userName}>👤 {session?.user?.name}</span>
            <button onClick={handleSignOut} className={styles.signOutButton}>
              Sign Out
            </button>
          </div>
        </div>
      </div>
      <Chat />
      <footer className={styles.footer}>
        <p>Try: "Add a task to buy groceries" • "Show all tasks" • "Mark task 1 as completed"</p>
      </footer>
    </div>
  );
}

export default Index;