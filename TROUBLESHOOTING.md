# Troubleshooting Guide

## Current Status

✅ **Backend Migration**: Successfully migrated from OpenAI to Google Gemini API  
✅ **Frontend Enhancement**: Modern dark theme UI implemented  
✅ **API Endpoints**: Root and health check endpoints added  
🔄 **Server Status**: Backend server is running and should auto-reload

## Common Issues & Solutions

### 1. "Could not connect to the agent" Error

**Cause**: Backend server is not running or has crashed  
**Solution**:
```powershell
# Stop any running backend servers (Ctrl+C in terminal)
# Then restart with:
cd backend
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH="c:\Users\SHAYAN\Desktop\hackathon2\todo-app-ph3\backend\src"
python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### 2. Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'google.generativeai'`  
**Solution**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install google-generativeai
```

### 3. API Key Issues

**Error**: `401 Authentication Error`  
**Solution**: 
1. Get your Gemini API key from https://aistudio.google.com/app/apikey
2. Update `backend/.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Restart the backend server

### 4. Tool Schema Errors

**Error**: `ValueError: Protocol message Schema has no "type" field`  
**Solution**: This should be fixed in the latest code. If you still see it:
1. Make sure you have the latest version of `backend/src/agent/main.py`
2. Restart the backend server to reload the code

### 5. CORS Errors

**Error**: Browser console shows CORS policy errors  
**Solution**: The backend is configured to allow `localhost:3000`. Check:
1. Frontend is running on port 3000
2. Backend is running on port 5000
3. Both servers are running

### 6. 404 Not Found on Root

**Issue**: Accessing `http://localhost:5000/` shows 404  
**Status**: ✅ Fixed! Root endpoint now returns API information

## Verification Steps

### Test Backend

1. **Check server is running**:
   - Open browser to `http://localhost:5000/`
   - Should see API information

2. **Check health endpoint**:
   - Open `http://localhost:5000/health`
   - Should see `{"status": "healthy"}`

3. **Test chat endpoint**:
   ```powershell
   curl -X POST http://localhost:5000/chat `
     -H "Content-Type: application/json" `
     -d '{"message": "Hello"}'
   ```

### Test Frontend

1. Open `http://localhost:3000` in browser
2. Type "Add a task to test" in the chat
3. Should see agent response

## Files Changed

### Backend Files
- `backend/src/agent/main.py` - Migrated to Gemini API
- `backend/src/main.py` - Added root and health endpoints
- `backend/requirements.txt` - Updated dependencies
- `backend/.env.example` - Updated environment variables

### Frontend Files
- `frontend/src/components/Chat.js` - Enhanced with modern UI
- `frontend/src/components/Chat.module.css` - New CSS module
- `frontend/src/pages/Index.js` - Updated header and layout
- `frontend/src/pages/Index.module.css` - New CSS module  
- `frontend/src/index.css` - Updated global styles with dark theme

## Next Steps

1. ✅ Gemini API key is configured in `.env`
2. ✅ `google-generativeai` package is installed
3. 🔄 Backend server is running (should auto-reload)
4. ✅ Frontend server is running
5. 🎯 Test the chat interface at `http://localhost:3000`

## Getting Help

If issues persist:
1. Check the terminal output for both frontend and backend
2. Check browser console for frontend errors
3. Verify all file changes were applied correctly
4. Try restarting both servers completely