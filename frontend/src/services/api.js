const API_BASE_URL = process.env.REACT_APP_BACKEND_API_URL || 'http://localhost:5000';
const USER_ID = process.env.REACT_APP_USER_ID || 'demo_user';

export const sendMessageToAgent = async (message, conversationId = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/${USER_ID}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        message,
        conversation_id: conversationId
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to get response from agent');
    }

    const data = await response.json();
    return {
      conversationId: data.conversation_id,
      response: data.response,
      toolCalls: data.tool_calls
    };
  } catch (error) {
    console.error('Error sending message to agent:', error);
    throw error;
  }
};