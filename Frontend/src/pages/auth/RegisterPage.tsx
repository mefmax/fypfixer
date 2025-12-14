import { RegisterForm } from '../../components/auth/RegisterForm';

export const RegisterPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0a0e27] to-[#1a1f3a] px-4">
      <div className="w-full max-w-md">
        <RegisterForm />
      </div>
    </div>
  );
};
