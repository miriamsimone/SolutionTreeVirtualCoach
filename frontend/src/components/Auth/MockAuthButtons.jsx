const MockAuthButtons = () => {
  return (
    <div className="space-y-3">
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-300"></div>
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-white text-gray-500">Or continue with</span>
        </div>
      </div>

      <button
        disabled
        className="w-full flex items-center justify-center gap-3 px-6 py-3 bg-gray-50 border-2 border-blue-500 rounded-lg cursor-not-allowed opacity-50"
        title="Coming soon"
      >
        <svg className="w-6 h-6" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="45" stroke="#0066FF" strokeWidth="8" fill="none"/>
          <path d="M35 30 C35 20, 50 20, 50 30 C50 40, 35 40, 35 50 C35 60, 50 60, 50 70" stroke="#0066FF" strokeWidth="8" strokeLinecap="round" fill="none"/>
        </svg>
        <span className="text-gray-600 font-medium">
          Continue with Clever
        </span>
        <span className="ml-2 text-xs text-gray-400">(Coming soon)</span>
      </button>
    </div>
  );
};

export default MockAuthButtons;
