// Use relative URL to leverage nginx proxy configuration in Kubernetes
const API_BASE_URL = '';

export const sendMessageToAgent = async (message, conversationId = null, token = null) => {
  try {
    const headers = {
      'Content-Type': 'application/json',
    };
    
    // Add authorization header if token is provided
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers,
      credentials: 'include', // Include cookies for session
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