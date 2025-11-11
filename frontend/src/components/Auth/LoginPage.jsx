import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import GoogleAuthButton from './GoogleAuthButton';
import MockAuthButtons from './MockAuthButtons';

const LoginPage = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-st-blue-light via-white to-st-green/20">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-st-blue border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/chat" replace />;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-st-blue-light via-white to-st-green/20 px-4">
      <div className="max-w-md w-full">
        {/* Logo and Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="text-4xl">📚</div>
            <div>
              <h1 className="text-3xl font-bold text-st-blue-dark">Solution Tree</h1>
              <p className="text-sm text-gray-600">Virtual Coach</p>
            </div>
          </div>
          <p className="text-gray-600 mt-4">
            Transform education worldwide to ensure learning for all
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-100">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
            Welcome Back
          </h2>

          <p className="text-gray-600 mb-6 text-center text-sm">
            Sign in to access your AI-powered PLC coaching assistants
          </p>

          <div className="space-y-4">
            <GoogleAuthButton />
            <MockAuthButtons />
          </div>

          {/* Info Section */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="space-y-3 text-sm text-gray-600">
              <div className="flex items-start gap-2">
                <span className="text-st-green">✓</span>
                <span>Access specialized coaching agents</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-st-green">✓</span>
                <span>Get guidance grounded in PLC best practices</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-st-green">✓</span>
                <span>Save and review your coaching sessions</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 mt-6">
          By signing in, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
