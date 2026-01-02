const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL || 'http://localhost:5000';

export const sendMessageToAgent = async (message, conversationHistory = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        message,
        conversation_history: conversationHistory 
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to get response from agent');
    }

    const data = await response.json();
    return {
      response: data.response,
      conversationHistory: data.conversation_history
    };
  } catch (error) {
    console.error('Error sending message to agent:', error);
    throw error;
  }
};