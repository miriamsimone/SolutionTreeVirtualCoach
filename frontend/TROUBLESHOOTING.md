# Frontend Troubleshooting Guide

## Current Issues & Solutions

### Issue: App Stuck on Loading Screen

**Symptoms:**
- Infinite loading spinner
- Page never progresses past initial load

**Causes & Solutions:**

1. **Backend returning 500 errors**
   - **Problem:** Backend `/api/auth/verify` endpoint is returning HTTP 500
   - **Solution:**
     - Check backend logs for errors
     - Ensure Firebase Admin SDK is properly initialized in backend
     - The frontend now gracefully handles this by falling back to Firebase-only auth

2. **Firebase popup cancelled**
   - **Problem:** Multiple sign-in attempts trigger `auth/cancelled-popup-request`
   - **Solution:**
     - Clear browser localStorage: `localStorage.clear()` in console
     - Refresh the page
     - Try signing in again with just one click

### Issue: CORS Errors

**Error Message:**
```
Origin http://localhost:3000 is not allowed by Access-Control-Allow-Origin
```

**Solution:**
- This appears when backend returns 500 errors
- The actual issue is the 500 error, not CORS
- Backend CORS is properly configured for `http://localhost:3000`
- Fix the backend 500 error and CORS messages will disappear

### Issue: Backend 500 Error on /api/auth/verify

**Symptoms:**
```
POST http://localhost:8000/api/auth/verify -> 500 Internal Server Error
```

**Backend Issue - Check:**
1. Backend server is running on port 8000
2. Firebase Admin SDK is initialized
3. Backend logs show the actual error
4. Environment variables are loaded (FIREBASE_PROJECT_ID, etc.)

**Frontend Workaround (Already Implemented):**
- Frontend now falls back to Firebase-only authentication
- Users can still log in even if backend verification fails
- App will work in "degraded mode" without full backend integration

### Issue: Multiple Sign-In Popups

**Symptoms:**
- Multiple Google sign-in windows open
- "Popup closed" errors

**Solution:**
1. Clear browser state:
   ```javascript
   // In browser console
   localStorage.clear()
   sessionStorage.clear()
   location.reload()
   ```

2. Click sign-in button only once
3. Wait for popup to complete

## How to Reset Everything

If the app is in a bad state:

```bash
# 1. Stop all servers
# Press Ctrl+C in terminals

# 2. Clear browser data
# In browser console:
localStorage.clear()
sessionStorage.clear()

# 3. Restart frontend
cd /Users/miriam/projects/SolutionTree/frontend
npm run dev

# 4. Refresh browser
# Go to http://localhost:3000
```

## Current Frontend Status

✅ **Working:**
- Development server
- Build process
- Code quality (no lint errors)
- Firebase initialization
- Login UI
- Routing
- Component rendering

⚠️ **Degraded:**
- Backend authentication verification (500 error)
  - Frontend handles this gracefully
  - Users can still authenticate via Firebase
  - Chat and sessions won't work until backend is fixed

❌ **Blocked (Backend Issues):**
- Chat messages
- Session management
- Rating submission
- Agent switching with backend persistence

## Quick Fixes Applied

### 1. Authentication Timeout
Added 5-second timeout to backend verification:
```javascript
// Now times out after 5 seconds instead of hanging forever
const timeoutId = setTimeout(() => controller.abort(), 5000);
```

### 2. Graceful Fallback
If backend fails, app continues with Firebase-only auth:
```javascript
catch (err) {
  // Still set user from Firebase even if backend fails
  setUser({ uid, email, displayName, photoURL });
}
```

### 3. Better Error Logging
Added detailed error logging to help diagnose issues:
```javascript
console.error('Server error (500):', data);
console.error('Network error - backend may not be running');
```

## Backend TODO (Not Frontend Issues)

The backend needs to fix:
1. ❌ `/api/auth/verify` returning 500 error
2. ❌ Firebase Admin SDK initialization
3. ❌ Error handling in auth endpoints

## Testing After Backend Fix

Once backend 500 errors are resolved:

1. Clear browser cache
2. Refresh page
3. Try signing in with Google
4. Should redirect to chat page
5. Try sending a message
6. Verify citations appear
7. Try rating a response

## Environment Check

Make sure these are set:

**Frontend `.env`:**
```bash
VITE_FIREBASE_API_KEY=AIzaSy...
VITE_FIREBASE_PROJECT_ID=solutiontreevirtualcoach
VITE_FIREBASE_AUTH_DOMAIN=solutiontreevirtualcoach.firebaseapp.com
VITE_FIREBASE_DATABASE_URL=https://solutiontreevirtualcoach-default-rtdb.firebaseio.com
VITE_BACKEND_API_URL=http://localhost:8000
```

**Backend `.env`:**
- FIREBASE_PROJECT_ID
- FIREBASE_PRIVATE_KEY
- FIREBASE_CLIENT_EMAIL
- Other backend vars

## Console Commands

Useful commands to run in browser console:

```javascript
// Clear all storage
localStorage.clear();
sessionStorage.clear();
location.reload();

// Check Firebase config
console.log(import.meta.env);

// Check current auth state
// (If you have access to auth object)
auth.currentUser;
```

## Current Server Status

```
Frontend: http://localhost:3000 ✅ Running
Backend:  http://localhost:8000 ⚠️ Running (500 errors)
```

## Next Steps

1. **Fix Backend** (Priority)
   - Investigate 500 error in `/api/auth/verify`
   - Check Firebase Admin SDK setup
   - Review backend logs

2. **Test Frontend Again**
   - After backend fix, test full flow
   - Verify all features work
   - Run through TESTING_CHECKLIST.md

3. **Monitor Errors**
   - Keep browser console open
   - Watch for new errors
   - Check backend logs
