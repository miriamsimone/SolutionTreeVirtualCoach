"""
Firebase service for authentication and session storage.
"""
from typing import List, Dict, Any, Optional
import firebase_admin
from firebase_admin import credentials, auth, db
import logging
from datetime import datetime
from app.config import Settings
from app.models.schemas import UserInfo, SessionResponse, Message
import uuid
import json

logger = logging.getLogger(__name__)


class FirebaseService:
    """Service for Firebase authentication and Realtime Database operations."""

    _initialized = False

    def __init__(self, settings: Settings):
        """
        Initialize Firebase service.

        Args:
            settings: Application settings containing Firebase configuration
        """
        self.settings = settings
        self.database_url = settings.firebase_database_url

        # Initialize Firebase Admin SDK once
        if not FirebaseService._initialized:
            try:
                cred = credentials.Certificate(settings.firebase_credentials_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': self.database_url
                })
                FirebaseService._initialized = True
                logger.info("Firebase Admin SDK initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase: {str(e)}")
                raise

    async def verify_token(self, id_token: str) -> UserInfo:
        """
        Verify Firebase ID token and return user information.

        Args:
            id_token: Firebase ID token from client

        Returns:
            UserInfo object with user details

        Raises:
            Exception: If token verification fails
        """
        try:
            decoded_token = auth.verify_id_token(id_token)
            user_id = decoded_token['uid']
            email = decoded_token.get('email')
            name = decoded_token.get('name')

            logger.info(f"Token verified for user: {user_id}")

            return UserInfo(
                user_id=user_id,
                email=email,
                name=name,
                verified=True
            )
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            raise

    async def create_session(
        self,
        user_id: str,
        agent_id: str,
        title: Optional[str] = None
    ) -> str:
        """
        Create a new chat session in Firebase Realtime Database.

        Args:
            user_id: User ID who owns the session
            agent_id: Initial agent for the session
            title: Optional session title

        Returns:
            Session ID (UUID)
        """
        try:
            session_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()

            session_data = {
                'session_id': session_id,
                'user_id': user_id,
                'agent_id': agent_id,
                'title': title or f"Session {timestamp}",
                'created_at': timestamp,
                'last_accessed': timestamp,
                'messages': []
            }

            # Store in Firebase: /sessions/{user_id}/{session_id}
            ref = db.reference(f'sessions/{user_id}/{session_id}')
            ref.set(session_data)

            logger.info(f"Created session {session_id} for user {user_id}")
            return session_id

        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            raise

    async def get_session(
        self,
        user_id: str,
        session_id: str
    ) -> Optional[SessionResponse]:
        """
        Retrieve a session from Firebase.

        Args:
            user_id: User ID who owns the session
            session_id: Session ID to retrieve

        Returns:
            SessionResponse object or None if not found
        """
        try:
            ref = db.reference(f'sessions/{user_id}/{session_id}')
            session_data = ref.get()

            if not session_data:
                return None

            # Convert messages to Message objects
            messages = []
            for msg_data in session_data.get('messages', []):
                messages.append(Message(
                    role=msg_data['role'],
                    content=msg_data['content'],
                    timestamp=datetime.fromisoformat(msg_data['timestamp']),
                    message_id=msg_data.get('message_id'),
                    citations=msg_data.get('citations')
                ))

            return SessionResponse(
                session_id=session_data['session_id'],
                user_id=session_data['user_id'],
                agent_id=session_data['agent_id'],
                title=session_data.get('title'),
                messages=messages,
                created_at=datetime.fromisoformat(session_data['created_at']),
                last_accessed=datetime.fromisoformat(session_data['last_accessed'])
            )

        except Exception as e:
            logger.error(f"Failed to get session: {str(e)}")
            raise

    async def get_user_sessions(
        self,
        user_id: str,
        limit: int = 50
    ) -> List[SessionResponse]:
        """
        Get all sessions for a user.

        Args:
            user_id: User ID
            limit: Maximum number of sessions to return

        Returns:
            List of SessionResponse objects
        """
        try:
            ref = db.reference(f'sessions/{user_id}')
            sessions_data = ref.get()

            if not sessions_data:
                return []

            sessions = []
            for session_id, session_data in sessions_data.items():
                # Convert messages
                messages = []
                for msg_data in session_data.get('messages', []):
                    messages.append(Message(
                        role=msg_data['role'],
                        content=msg_data['content'],
                        timestamp=datetime.fromisoformat(msg_data['timestamp']),
                        message_id=msg_data.get('message_id'),
                        citations=msg_data.get('citations')
                    ))

                sessions.append(SessionResponse(
                    session_id=session_data['session_id'],
                    user_id=session_data['user_id'],
                    agent_id=session_data['agent_id'],
                    title=session_data.get('title'),
                    messages=messages,
                    created_at=datetime.fromisoformat(session_data['created_at']),
                    last_accessed=datetime.fromisoformat(session_data['last_accessed'])
                ))

            # Sort by last accessed, most recent first
            sessions.sort(key=lambda x: x.last_accessed, reverse=True)

            return sessions[:limit]

        except Exception as e:
            logger.error(f"Failed to get user sessions: {str(e)}")
            raise

    async def add_message_to_session(
        self,
        user_id: str,
        session_id: str,
        message: Message
    ) -> None:
        """
        Add a message to a session.

        Args:
            user_id: User ID who owns the session
            session_id: Session ID
            message: Message to add
        """
        try:
            # Get current messages
            ref = db.reference(f'sessions/{user_id}/{session_id}')
            session_data = ref.get()

            if not session_data:
                raise ValueError(f"Session {session_id} not found")

            # Convert message to dict
            message_dict = {
                'role': message.role,
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'message_id': message.message_id
            }

            if message.citations:
                message_dict['citations'] = [c.model_dump() for c in message.citations]

            # Append message
            messages = session_data.get('messages', [])
            messages.append(message_dict)

            # Update session
            ref.update({
                'messages': messages,
                'last_accessed': datetime.utcnow().isoformat()
            })

            logger.info(f"Added message to session {session_id}")

        except Exception as e:
            logger.error(f"Failed to add message to session: {str(e)}")
            raise

    async def delete_session(
        self,
        user_id: str,
        session_id: str
    ) -> None:
        """
        Delete a session.

        Args:
            user_id: User ID who owns the session
            session_id: Session ID to delete
        """
        try:
            ref = db.reference(f'sessions/{user_id}/{session_id}')
            ref.delete()
            logger.info(f"Deleted session {session_id}")
        except Exception as e:
            logger.error(f"Failed to delete session: {str(e)}")
            raise

    async def save_feedback(
        self,
        user_id: str,
        session_id: str,
        message_id: str,
        rating: int,
        comment: Optional[str] = None
    ) -> str:
        """
        Save user feedback for a message.

        Args:
            user_id: User ID
            session_id: Session ID
            message_id: Message ID being rated
            rating: Rating value (1-5)
            comment: Optional feedback comment

        Returns:
            Feedback ID
        """
        try:
            feedback_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()

            feedback_data = {
                'feedback_id': feedback_id,
                'user_id': user_id,
                'session_id': session_id,
                'message_id': message_id,
                'rating': rating,
                'comment': comment,
                'timestamp': timestamp
            }

            # Store in Firebase: /feedback/{feedback_id}
            ref = db.reference(f'feedback/{feedback_id}')
            ref.set(feedback_data)

            logger.info(f"Saved feedback {feedback_id} for message {message_id}")
            return feedback_id

        except Exception as e:
            logger.error(f"Failed to save feedback: {str(e)}")
            raise
