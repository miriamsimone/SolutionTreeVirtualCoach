const AgentButton = ({ agent, isActive, onClick }) => {
  const activeClasses = isActive
    ? 'bg-gradient-to-r from-st-blue to-st-blue-dark text-white border-st-blue-dark shadow-lg scale-105'
    : 'bg-white text-gray-700 border-gray-300 hover:border-st-blue hover:shadow-md';

  return (
    <button
      onClick={onClick}
      className={`flex-1 p-4 rounded-lg border-2 transition-all duration-200 ${activeClasses}`}
    >
      <div className="flex flex-col items-center gap-2 text-center">
        <span className="text-3xl">{agent.icon}</span>
        <h3 className={`font-semibold text-sm ${isActive ? 'text-white' : 'text-gray-800'}`}>
          {agent.name}
        </h3>
        <p className={`text-xs ${isActive ? 'text-white/90' : 'text-gray-600'}`}>
          {agent.description}
        </p>
      </div>
    </button>
  );
};

export default AgentButton;
