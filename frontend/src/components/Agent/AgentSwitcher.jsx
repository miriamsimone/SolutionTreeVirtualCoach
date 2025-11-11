import { AGENTS } from '../../utils/constants';
import AgentButton from './AgentButton';

const AgentSwitcher = ({ currentAgent, onAgentChange }) => {
  const agents = Object.values(AGENTS);

  return (
    <div className="bg-white border-b border-gray-200 p-4 shadow-sm">
      <div className="max-w-4xl mx-auto">
        <div className="flex gap-3">
          {agents.map((agent) => (
            <AgentButton
              key={agent.id}
              agent={agent}
              isActive={currentAgent === agent.id}
              onClick={() => onAgentChange(agent.id)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default AgentSwitcher;
