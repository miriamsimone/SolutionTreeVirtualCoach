"""
Basic tests for backend validation.
"""
import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    try:
        from app.config import Settings, get_settings
        print("✓ Config imports successful")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False

    try:
        from app.models.schemas import (
            ChatRequest, ChatResponse, Citation,
            SessionCreate, SessionResponse, AgentType
        )
        print("✓ Schema imports successful")
    except Exception as e:
        print(f"✗ Schema import failed: {e}")
        return False

    try:
        from app.utils.logging import setup_logging, get_logger
        from app.utils.prompts import format_context_for_prompt, build_conversation_history
        print("✓ Utils imports successful")
    except Exception as e:
        print(f"✗ Utils import failed: {e}")
        return False

    return True


def test_schemas():
    """Test Pydantic schema validation."""
    print("\nTesting schemas...")

    from app.models.schemas import (
        ChatRequest, ChatResponse, Citation,
        AgentType, SessionCreate, FeedbackRequest
    )

    try:
        # Test ChatRequest
        chat_req = ChatRequest(
            query="Test question",
            agent_id=AgentType.PROFESSIONAL_LEARNING
        )
        assert chat_req.query == "Test question"
        assert chat_req.agent_id == AgentType.PROFESSIONAL_LEARNING
        print("✓ ChatRequest validation works")
    except Exception as e:
        print(f"✗ ChatRequest validation failed: {e}")
        return False

    try:
        # Test Citation
        citation = Citation(
            id="cite_1",
            source_title="Test Book",
            page_number=42,
            chunk_text="Test content",
            relevance_score=0.95
        )
        assert citation.relevance_score == 0.95
        print("✓ Citation validation works")
    except Exception as e:
        print(f"✗ Citation validation failed: {e}")
        return False

    try:
        # Test ChatResponse
        chat_resp = ChatResponse(
            response="Test response",
            citations=[citation],
            agent_used=AgentType.CLASSROOM_CURRICULUM,
            session_id="test-session",
            message_id="test-message"
        )
        assert len(chat_resp.citations) == 1
        print("✓ ChatResponse validation works")
    except Exception as e:
        print(f"✗ ChatResponse validation failed: {e}")
        return False

    try:
        # Test SessionCreate
        session_create = SessionCreate(
            agent_id=AgentType.PROFESSIONAL_LEARNING,
            title="Test Session"
        )
        assert session_create.title == "Test Session"
        print("✓ SessionCreate validation works")
    except Exception as e:
        print(f"✗ SessionCreate validation failed: {e}")
        return False

    try:
        # Test FeedbackRequest
        feedback = FeedbackRequest(
            message_id="msg-123",
            session_id="session-123",
            rating=5,
            comment="Great!"
        )
        assert feedback.rating == 5
        print("✓ FeedbackRequest validation works")
    except Exception as e:
        print(f"✗ FeedbackRequest validation failed: {e}")
        return False

    try:
        # Test validation failure (rating out of range)
        invalid_feedback = FeedbackRequest(
            message_id="msg-123",
            session_id="session-123",
            rating=10  # Should fail - max is 5
        )
        print("✗ FeedbackRequest validation should have failed for rating > 5")
        return False
    except Exception:
        print("✓ FeedbackRequest validation correctly rejects invalid ratings")

    return True


def test_config():
    """Test configuration."""
    print("\nTesting configuration...")

    from app.config import Settings

    try:
        # Test agent configs exist
        settings = Settings(
            openai_api_key="test-key",
            pinecone_api_key="test-key",
            pinecone_environment="test",
            pinecone_index_name="test",
            firebase_credentials_path="/tmp/test.json",
            firebase_database_url="https://test.firebaseio.com"
        )

        assert "professional_learning" in settings.agent_configs
        assert "classroom_curriculum" in settings.agent_configs
        print("✓ Both agents configured")

        # Check agent configs have required fields
        pl_config = settings.agent_configs["professional_learning"]
        assert "name" in pl_config
        assert "description" in pl_config
        assert "metadata_filter" in pl_config
        assert "system_prompt" in pl_config
        print("✓ Professional Learning agent config complete")

        cc_config = settings.agent_configs["classroom_curriculum"]
        assert "name" in cc_config
        assert "description" in cc_config
        assert "metadata_filter" in cc_config
        assert "system_prompt" in cc_config
        print("✓ Classroom Curriculum agent config complete")

        # Check default values
        assert settings.max_conversation_history == 5
        assert settings.pinecone_top_k == 5
        print("✓ Default configuration values set correctly")

    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

    return True


def test_prompt_utils():
    """Test prompt utility functions."""
    print("\nTesting prompt utilities...")

    from app.utils.prompts import format_context_for_prompt, build_conversation_history
    from app.models.schemas import Citation, Message
    from datetime import datetime

    try:
        # Test format_context_for_prompt
        citations = [
            Citation(
                id="cite_1",
                source_title="Book 1",
                page_number=10,
                chunk_text="Content from book 1",
                relevance_score=0.9
            ),
            Citation(
                id="cite_2",
                source_title="Book 2",
                chunk_text="Content from book 2",
                relevance_score=0.8
            )
        ]

        context = format_context_for_prompt(citations)
        assert "Book 1" in context
        assert "Book 2" in context
        assert "Page: 10" in context
        print("✓ format_context_for_prompt works")

    except Exception as e:
        print(f"✗ format_context_for_prompt failed: {e}")
        return False

    try:
        # Test build_conversation_history
        messages = [
            Message(role="user", content="Question 1", timestamp=datetime.utcnow()),
            Message(role="assistant", content="Answer 1", timestamp=datetime.utcnow()),
            Message(role="user", content="Question 2", timestamp=datetime.utcnow()),
            Message(role="assistant", content="Answer 2", timestamp=datetime.utcnow()),
        ]

        history = build_conversation_history(messages, max_history=2)
        assert len(history) == 4  # 2 pairs
        assert history[0]["role"] == "user"
        assert history[0]["content"] == "Question 1"
        print("✓ build_conversation_history works")

    except Exception as e:
        print(f"✗ build_conversation_history failed: {e}")
        return False

    try:
        # Test with more messages than max_history
        messages = [
            Message(role="user", content=f"Q{i}", timestamp=datetime.utcnow())
            for i in range(20)
        ]

        history = build_conversation_history(messages, max_history=3)
        assert len(history) == 6  # Should only keep last 3 pairs
        print("✓ build_conversation_history respects max_history limit")

    except Exception as e:
        print(f"✗ build_conversation_history max_history test failed: {e}")
        return False

    return True


def test_agent_types():
    """Test agent type enum."""
    print("\nTesting agent types...")

    from app.models.schemas import AgentType

    try:
        assert AgentType.PROFESSIONAL_LEARNING.value == "professional_learning"
        assert AgentType.CLASSROOM_CURRICULUM.value == "classroom_curriculum"
        print("✓ Agent type enum values correct")

        # Test string conversion
        agent_from_string = AgentType("professional_learning")
        assert agent_from_string == AgentType.PROFESSIONAL_LEARNING
        print("✓ Agent type string conversion works")

    except Exception as e:
        print(f"✗ Agent type test failed: {e}")
        return False

    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("RUNNING BACKEND VALIDATION TESTS")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Schemas", test_schemas),
        ("Configuration", test_config),
        ("Prompt Utils", test_prompt_utils),
        ("Agent Types", test_agent_types),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:20s} {status}")

    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
