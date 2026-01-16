import { useState, useEffect } from 'react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL || 'http://localhost:5000';

// Custom auth client that works with FastAPI backend
const createCustomAuthClient = () => {
  return {
    signUp: {
      email: async ({ email, password, name }) => {
        try {
          const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ email, password, name }),
          });

          const data = await response.json();

          if (!response.ok) {
            return { error: { message: data.detail || 'Sign up failed' } };
          }

          return { data };
        } catch (error) {
          return { error: { message: error.message || 'Network error' } };
        }
      },
    },

    signIn: {
      email: async ({ email, password }) => {
        try {
          const response = await fetch(`${API_BASE_URL}/api/auth/signin`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ email, password }),
          });

          const data = await response.json();

          if (!response.ok) {
            return { error: { message: data.detail || 'Sign in failed' } };
          }

          return { data };
        } catch (error) {
          return { error: { message: error.message || 'Network error' } };
        }
      },
    },

    signOut: async () => {
      try {
        await fetch(`${API_BASE_URL}/api/auth/signout`, {
          method: 'POST',
          credentials: 'include',
        });
      } catch (error) {
        console.error('Sign out error:', error);
      }
    },

    getSession: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/auth/session`, {
          credentials: 'include',
        });

        if (!response.ok) {
          return null;
        }

        const user = await response.json();
        return user;
      } catch (error) {
        console.error('Get session error:', error);
        return null;
      }
    },
  };
};

export const authClient = createCustomAuthClient();

export const { signIn, signUp, signOut } = authClient;

// Custom useSession hook
export const useSession = () => {
  const [session, setSession] = useState(null);
  const [isPending, setIsPending] = useState(true);

  useEffect(() => {
    const fetchSession = async () => {
      setIsPending(true);
      const user = await authClient.getSession();
      setSession(user ? { user } : null);
      setIsPending(false);
    };

    fetchSession();
  }, []);

  return { data: session, isPending };
};

export const getSession = authClient.getSession;