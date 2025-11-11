import { Menu, LogOut, User } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

const Header = ({ onMenuToggle }) => {
  const { user, signOut } = useAuth();

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch (err) {
      console.error('Error signing out:', err);
    }
  };

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Left: Logo and Menu */}
          <div className="flex items-center gap-4">
            <button
              onClick={onMenuToggle}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors lg:hidden"
            >
              <Menu className="w-5 h-5 text-gray-600" />
            </button>

            <div className="flex items-center gap-3">
              <div className="text-3xl">📚</div>
              <div>
                <h1 className="text-xl font-bold text-st-blue-dark">Solution Tree</h1>
                <p className="text-xs text-gray-600 hidden sm:block">Virtual Coach</p>
              </div>
            </div>
          </div>

          {/* Right: User Info */}
          <div className="flex items-center gap-4">
            {user && (
              <>
                <div className="hidden sm:flex items-center gap-3">
                  {user.photoURL ? (
                    <img
                      src={user.photoURL}
                      alt={user.displayName}
                      className="w-8 h-8 rounded-full"
                    />
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-st-green flex items-center justify-center text-white">
                      <User className="w-5 h-5" />
                    </div>
                  )}
                  <div className="text-sm">
                    <p className="font-medium text-gray-800">{user.displayName}</p>
                    <p className="text-xs text-gray-600">{user.email}</p>
                  </div>
                </div>

                <button
                  onClick={handleSignOut}
                  className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                  title="Sign out"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="hidden sm:inline">Sign Out</span>
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
