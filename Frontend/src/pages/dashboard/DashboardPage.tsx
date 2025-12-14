import { useAuthStore } from '../../store/authStore';

export const DashboardPage = () => {
  const { user, logout } = useAuthStore();

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e27] to-[#1a1f3a] px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">
              Welcome, {user?.email}!
            </h1>
            <p className="text-gray-400">Your daily FYP training plan is ready</p>
          </div>
          <button
            onClick={logout}
            className="px-4 py-2 rounded-xl bg-gray-700 text-white hover:bg-gray-600 transition-colors"
          >
            Logout
          </button>
        </div>

        <div className="bg-dark-secondary border border-gray-700 rounded-xl p-8 text-center">
          <h2 className="text-2xl font-semibold text-white mb-4">
            Dashboard Coming Soon
          </h2>
          <p className="text-gray-400">
            Your daily plans and video recommendations will appear here
          </p>
        </div>
      </div>
    </div>
  );
};
