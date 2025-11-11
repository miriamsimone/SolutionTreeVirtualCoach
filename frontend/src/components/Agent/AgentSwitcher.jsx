import { AGENTS } from '../../utils/constants';
import AgentButton from './AgentButton';

const AgentSwitcher = ({ currentAgent, onAgentChange }) => {
  const agents = Object.values(AGENTS);

  return (
    <div className="bg-gray-50 border-b border-gray-200 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-3">
          <h2 className="text-lg font-semibold text-gray-800">Select Your Coach</h2>
          <p className="text-sm text-gray-600">Choose the coaching agent that best fits your current needs</p>
        </div>

        <div className="flex gap-4">
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
