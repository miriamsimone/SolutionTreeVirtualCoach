import { useChat } from '../hooks/useChat';
import AgentSwitcher from '../components/Agent/AgentSwitcher';
import ChatWindow from '../components/Chat/ChatWindow';
// import CitationTest from '../components/Chat/CitationTest'; // Uncomment to test citations

const ChatPage = () => {
  const { currentAgent, switchAgent, clearMessages } = useChat();

  const handleAgentChange = (newAgentId) => {
    if (newAgentId !== currentAgent) {
      const confirmed = window.confirm(
        'Switching agents will start a new conversation. Continue?'
      );

      if (confirmed) {
        clearMessages();
        switchAgent(newAgentId);
      }
    }
  };

  return (
    <div className="flex flex-col h-full">
      <AgentSwitcher currentAgent={currentAgent} onAgentChange={handleAgentChange} />
      <ChatWindow />
    </div>
  );
};

export default ChatPage;
