# Frontend Testing Checklist

## Pre-Testing Setup

- [ ] Backend server is running on `http://localhost:8000`
- [ ] Firebase project is configured
- [ ] `.env` file has correct Firebase credentials
- [ ] Dependencies installed (`npm install`)
- [ ] Dev server started (`npm run dev`)

## Authentication Testing

### Google OAuth
- [ ] Navigate to `http://localhost:3000`
- [ ] Redirected to login page
- [ ] Click "Continue with Google"
- [ ] Google popup appears
- [ ] Select Google account
- [ ] Successfully authenticated
- [ ] Redirected to `/chat`
- [ ] User info displayed in header

### Session Persistence
- [ ] Refresh page while logged in
- [ ] Still authenticated (no redirect to login)
- [ ] User info persists

### Logout
- [ ] Click "Sign Out" in header
- [ ] Redirected to login page
- [ ] Cannot access protected routes

## Agent Switcher Testing

### Basic Switching
- [ ] Both agents visible in switcher
- [ ] Professional Learning Coach selected by default
- [ ] Click Classroom Curriculum Coach
- [ ] No messages: switches immediately
- [ ] With messages: confirmation dialog appears
- [ ] Confirm switch: messages cleared, agent changes
- [ ] Cancel switch: stays on current agent

### Visual Feedback
- [ ] Active agent highlighted (blue gradient)
- [ ] Inactive agent has hover effect
- [ ] Icons display correctly (👥 and 📚)
- [ ] Descriptions are readable

## Chat Interface Testing

### Message Input
- [ ] Text area accepts input
- [ ] Send button enabled when text present
- [ ] Send button disabled when empty
- [ ] Enter key sends message
- [ ] Shift+Enter creates new line
- [ ] Text area auto-grows with content

### Message Display
- [ ] User messages appear on right (blue)
- [ ] AI messages appear on left (white)
- [ ] Messages auto-scroll to bottom
- [ ] Timestamps display correctly
- [ ] Loading indicator shows while waiting

### Message Sending
- [ ] Type "What are the four critical questions of a PLC?"
- [ ] Click Send
- [ ] Loading indicator appears
- [ ] Response received from backend
- [ ] Response displays with formatting
- [ ] Citations appear below response (if any)

### Error Handling
- [ ] Stop backend server
- [ ] Try sending message
- [ ] Error message displays in chat
- [ ] Can retry after backend restarts

## Citation Testing

### Display
- [ ] Citations numbered (1, 2, 3...)
- [ ] Source title displays
- [ ] Page number shows
- [ ] Relevance score bar displays
- [ ] Percentage shows next to bar

### Interaction
- [ ] Click citation to expand
- [ ] Chunk text appears
- [ ] Click again to collapse
- [ ] Multiple citations can be expanded simultaneously

### Styling
- [ ] Citations have blue border
- [ ] Hover effect works
- [ ] Text is readable
- [ ] Icons display correctly

## Rating System Testing

### Rating Submission
- [ ] Stars appear after AI response
- [ ] Hover over stars changes color
- [ ] Click 3rd star
- [ ] Rating submits to backend
- [ ] "Thank you" message appears
- [ ] Stars disappear after rating

### API Integration
- [ ] Check backend logs for rating submission
- [ ] Verify session_id and message_id sent correctly

## Session Management Testing

### Navigation
- [ ] Click "Sessions" in sidebar
- [ ] Sessions page loads
- [ ] Empty state if no sessions
- [ ] "Start Chatting" button works

### Session List
- [ ] Have at least one conversation
- [ ] Session appears in list
- [ ] Shows agent icon and name
- [ ] Shows date/time
- [ ] Shows message count (if available)

### Loading Session
- [ ] Click on a session
- [ ] Loading state appears
- [ ] Redirects to chat page
- [ ] Previous messages load
- [ ] Correct agent selected
- [ ] Can continue conversation

### Deleting Session
- [ ] Click trash icon on session
- [ ] Confirmation dialog appears
- [ ] Confirm deletion
- [ ] Session removed from list
- [ ] Cancel: session remains

## Analytics Page Testing

### Mocked Dashboard
- [ ] Navigate to Analytics
- [ ] Four stat cards display
- [ ] All show "--" as values
- [ ] Notice banner explains it's mocked
- [ ] Agent usage section displays
- [ ] Recent activity section displays

## Layout & Navigation Testing

### Header
- [ ] Solution Tree logo displays
- [ ] User profile photo/initial shows
- [ ] User name and email display
- [ ] Sign out button works

### Sidebar
- [ ] Desktop: always visible
- [ ] Mobile: hidden by default
- [ ] Menu button opens sidebar on mobile
- [ ] Navigation links work
- [ ] Active link highlighted
- [ ] Close button works on mobile

### Responsive Design
- [ ] Test on mobile (< 640px)
- [ ] Test on tablet (640-1024px)
- [ ] Test on desktop (> 1024px)
- [ ] All features accessible on all sizes
- [ ] No horizontal scroll
- [ ] Touch targets large enough

## Accessibility Testing

### Keyboard Navigation
- [ ] Tab through all interactive elements
- [ ] Focus visible on all elements
- [ ] Enter/Space activates buttons
- [ ] Escape closes dialogs

### Screen Reader
- [ ] Run with screen reader (if available)
- [ ] All buttons have labels
- [ ] Form inputs have labels
- [ ] Images have alt text

## Performance Testing

### Load Times
- [ ] Initial page load < 2s
- [ ] Message send < 3s (depends on backend)
- [ ] Session load < 1s
- [ ] Smooth animations

### Browser Console
- [ ] No errors in console
- [ ] No warning about missing keys
- [ ] No 404 errors for assets

## Edge Cases

### Network Issues
- [ ] Disconnect internet
- [ ] Try sending message
- [ ] Error message displays
- [ ] Reconnect internet
- [ ] Can send messages again

### Long Messages
- [ ] Send very long message (500+ chars)
- [ ] Displays correctly
- [ ] No layout breaks
- [ ] Scrollable if needed

### Special Characters
- [ ] Send message with emojis
- [ ] Send message with code ```
- [ ] Send message with markdown **bold**
- [ ] All render correctly

### Rapid Actions
- [ ] Send multiple messages quickly
- [ ] All messages process correctly
- [ ] No duplicate messages
- [ ] Correct order maintained

### Empty States
- [ ] New user: no sessions
- [ ] No messages: empty chat
- [ ] All show appropriate UI

## Browser Compatibility

- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

## Final Checks

- [ ] No console errors
- [ ] No broken images
- [ ] All links work
- [ ] All buttons functional
- [ ] Smooth user experience
- [ ] Colors match brand
- [ ] Professional appearance

## Issues Found

Document any issues here:

1. Issue: _______________
   - Expected: _______________
   - Actual: _______________
   - Severity: High/Medium/Low

2. Issue: _______________
   - Expected: _______________
   - Actual: _______________
   - Severity: High/Medium/Low

## Sign-off

- [ ] All P0 features tested and working
- [ ] All P1 features tested and working
- [ ] Documentation complete
- [ ] Ready for deployment

**Tested by:** _______________
**Date:** _______________
**Status:** ☐ Pass ☐ Pass with notes ☐ Fail
