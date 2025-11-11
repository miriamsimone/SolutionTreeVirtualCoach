"""
Analytics routes for usage statistics and insights.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import UserInfo
from app.services.firebase_service import FirebaseService
from app.dependencies import get_current_user, get_firebase_service
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("")
async def get_analytics(
    current_user: UserInfo = Depends(get_current_user),
    firebase_service: FirebaseService = Depends(get_firebase_service),
    days: int = 7  # Last N days for recent activity
):
    """
    Get analytics and usage statistics.

    Returns:
        Analytics data including conversation counts, ratings, agent usage, etc.
    """
    try:
        # Get all sessions and feedback from Firebase
        all_sessions = []
        all_feedback = []

        # Get sessions from Firebase Realtime Database
        # Note: In production, you'd want to add pagination or caching
        try:
            sessions_ref = firebase_service.firebase_admin.db.reference('sessions')
            all_sessions_data = sessions_ref.get() or {}

            for user_id, user_sessions in all_sessions_data.items():
                for session_id, session_data in user_sessions.items():
                    all_sessions.append(session_data)

            # Get feedback
            feedback_ref = firebase_service.firebase_admin.db.reference('feedback')
            all_feedback_data = feedback_ref.get() or {}
            all_feedback = list(all_feedback_data.values())

        except AttributeError:
            # Fallback if firebase_admin not available directly
            logger.warning("Using alternative Firebase access method")
            from firebase_admin import db

            sessions_ref = db.reference('sessions')
            all_sessions_data = sessions_ref.get() or {}

            for user_id, user_sessions in all_sessions_data.items():
                for session_id, session_data in user_sessions.items():
                    all_sessions.append(session_data)

            feedback_ref = db.reference('feedback')
            all_feedback_data = feedback_ref.get() or {}
            all_feedback = list(all_feedback_data.values())

        # Calculate metrics
        total_conversations = len(all_sessions)

        # Count unique users
        unique_users = set()
        for session in all_sessions:
            unique_users.add(session.get('user_id'))
        active_users = len(unique_users)

        # Calculate average rating
        if all_feedback:
            avg_rating = sum(f.get('rating', 0) for f in all_feedback) / len(all_feedback)
        else:
            avg_rating = 0.0

        # Sessions in the last week
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        sessions_this_week = 0
        for session in all_sessions:
            try:
                created_at = datetime.fromisoformat(session.get('created_at', ''))
                if created_at >= cutoff_date:
                    sessions_this_week += 1
            except (ValueError, TypeError):
                continue

        # Agent usage breakdown
        agent_usage = {
            "professional_learning": 0,
            "classroom_curriculum": 0
        }
        for session in all_sessions:
            agent_id = session.get('agent_id', '')
            if agent_id in agent_usage:
                agent_usage[agent_id] += 1

        # Calculate percentages
        total_agent_sessions = sum(agent_usage.values())
        agent_usage_percent = {}
        if total_agent_sessions > 0:
            for agent_id, count in agent_usage.items():
                agent_usage_percent[agent_id] = round((count / total_agent_sessions) * 100, 1)
        else:
            agent_usage_percent = {k: 0.0 for k in agent_usage.keys()}

        # Recent activity (sessions per day for last N days)
        recent_activity = []
        for i in range(days - 1, -1, -1):
            day = datetime.utcnow() - timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)

            sessions_count = 0
            for session in all_sessions:
                try:
                    created_at = datetime.fromisoformat(session.get('created_at', ''))
                    if day_start <= created_at < day_end:
                        sessions_count += 1
                except (ValueError, TypeError):
                    continue

            recent_activity.append({
                "date": day.strftime("%Y-%m-%d"),
                "sessions": sessions_count
            })

        # Top rated sessions (if feedback exists)
        top_rated = []
        if all_feedback:
            feedback_by_session = {}
            for f in all_feedback:
                session_id = f.get('session_id')
                if session_id:
                    if session_id not in feedback_by_session:
                        feedback_by_session[session_id] = []
                    feedback_by_session[session_id].append(f.get('rating', 0))

            # Calculate average rating per session
            session_ratings = []
            for session_id, ratings in feedback_by_session.items():
                avg = sum(ratings) / len(ratings)
                session_ratings.append({
                    "session_id": session_id,
                    "avg_rating": round(avg, 2),
                    "rating_count": len(ratings)
                })

            # Sort by rating and take top 5
            session_ratings.sort(key=lambda x: x['avg_rating'], reverse=True)
            top_rated = session_ratings[:5]

        # Build response
        analytics = {
            "total_conversations": total_conversations,
            "active_users": active_users,
            "avg_rating": round(avg_rating, 2),
            "sessions_this_week": sessions_this_week,
            "agent_usage": agent_usage_percent,
            "agent_usage_counts": agent_usage,
            "recent_activity": recent_activity,
            "total_feedback_count": len(all_feedback),
            "top_rated_sessions": top_rated,
            "generated_at": datetime.utcnow().isoformat()
        }

        logger.info(f"Analytics generated for user {current_user.user_id}")
        return analytics

    except Exception as e:
        logger.error(f"Failed to generate analytics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate analytics: {str(e)}"
        )


@router.get("/summary")
async def get_analytics_summary(
    current_user: UserInfo = Depends(get_current_user),
    firebase_service: FirebaseService = Depends(get_firebase_service)
):
    """
    Get quick analytics summary (faster, fewer details).

    Returns:
        Lightweight analytics summary
    """
    try:
        from firebase_admin import db

        # Quick counts without pulling all data
        sessions_ref = db.reference('sessions')
        all_sessions_data = sessions_ref.get() or {}

        total_conversations = 0
        unique_users = set()

        for user_id, user_sessions in all_sessions_data.items():
            unique_users.add(user_id)
            total_conversations += len(user_sessions)

        feedback_ref = db.reference('feedback')
        all_feedback = feedback_ref.get() or {}

        avg_rating = 0.0
        if all_feedback:
            ratings = [f.get('rating', 0) for f in all_feedback.values()]
            avg_rating = sum(ratings) / len(ratings)

        summary = {
            "total_conversations": total_conversations,
            "active_users": len(unique_users),
            "avg_rating": round(avg_rating, 2),
            "total_feedback": len(all_feedback)
        }

        return summary

    except Exception as e:
        logger.error(f"Failed to generate analytics summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate analytics summary: {str(e)}"
        )
