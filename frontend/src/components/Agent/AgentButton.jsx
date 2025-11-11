import * as Icons from 'lucide-react';

const AgentButton = ({ agent, isActive, onClick }) => {
  const Icon = Icons[agent.icon];

  const activeClasses = isActive
    ? 'bg-gradient-to-r from-st-blue to-st-blue-dark text-white border-st-blue-dark shadow-lg scale-105'
    : 'bg-white text-gray-700 border-gray-300 hover:border-st-blue hover:shadow-md';

  const iconBgClasses = isActive
    ? 'bg-white/20'
    : 'bg-st-blue/10';

  const iconColorClasses = isActive
    ? 'text-white'
    : 'text-st-blue';

  return (
    <button
      onClick={onClick}
      className={`flex-1 p-5 rounded-xl border-2 transition-all duration-200 ${activeClasses}`}
    >
      <div className="flex items-center gap-3">
        <div className={`flex-shrink-0 w-12 h-12 rounded-lg ${iconBgClasses} flex items-center justify-center`}>
          {Icon && <Icon className={`w-6 h-6 ${iconColorClasses}`} />}
        </div>
        <div className="flex-1 text-left">
          <h3 className={`font-semibold text-base ${isActive ? 'text-white' : 'text-gray-800'}`}>
            {agent.name}
          </h3>
          <p className={`text-xs mt-0.5 ${isActive ? 'text-white/90' : 'text-gray-600'}`}>
            {agent.description}
          </p>
        </div>
      </div>
    </button>
  );
};

export default AgentButton;
