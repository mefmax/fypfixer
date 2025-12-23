import React from 'react';
import { Link } from 'react-router-dom';

export const PrivacyPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">
      <div className="max-w-3xl mx-auto px-4 py-12">
        <Link to="/" className="text-orange-500 hover:text-orange-400 mb-8 inline-block">
          ← Back to FYPGlow
        </Link>

        <h1 className="text-3xl font-bold text-orange-500 mb-2">Privacy Policy</h1>
        <p className="text-gray-400 mb-8">Last updated: December 23, 2025</p>

        <div className="prose prose-invert prose-orange max-w-none space-y-6">
          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">1. Introduction</h2>
            <p className="text-gray-300 leading-relaxed">
              FYPGlow ("we", "our", or "us") respects your privacy and is committed to protecting
              your personal data. This Privacy Policy explains how we collect, use, and protect
              your information when you use our Service.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">2. Information We Collect</h2>

            <h3 className="text-lg font-medium text-white mt-6 mb-3">2.1 Information from TikTok</h3>
            <p className="text-gray-300 leading-relaxed">When you sign in with TikTok, we receive:</p>
            <ul className="list-disc list-inside text-gray-300 mt-2 space-y-1">
              <li><strong>TikTok User ID</strong> (open_id) — A unique identifier for your account</li>
              <li><strong>Display Name</strong> — Your TikTok username</li>
              <li><strong>Avatar URL</strong> — Your profile picture</li>
            </ul>

            <p className="text-gray-300 leading-relaxed mt-4">
              We request only the <code className="bg-gray-800 px-1 rounded">user.info.basic</code> scope
              and do NOT access your TikTok videos, followers, messages, or watch history.
            </p>

            <h3 className="text-lg font-medium text-white mt-6 mb-3">2.2 Information We Generate</h3>
            <p className="text-gray-300 leading-relaxed">When you use FYPGlow, we create and store:</p>
            <ul className="list-disc list-inside text-gray-300 mt-2 space-y-1">
              <li>Selected categories — Your chosen content preferences</li>
              <li>Progress data — Completed actions, streaks, and achievements</li>
              <li>Usage statistics — When you use the app</li>
            </ul>

            <h3 className="text-lg font-medium text-white mt-6 mb-3">2.3 Information We Do NOT Collect</h3>
            <ul className="list-disc list-inside text-gray-300 mt-2 space-y-1">
              <li>Email address (unless you join our waitlist)</li>
              <li>Phone number</li>
              <li>Location data</li>
              <li>Payment information</li>
              <li>Your TikTok browsing or viewing history</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">3. How We Use Your Information</h2>
            <p className="text-gray-300 leading-relaxed">We use your information to:</p>
            <ul className="list-disc list-inside text-gray-300 mt-2 space-y-1">
              <li>Authenticate you via TikTok</li>
              <li>Display your profile in the app</li>
              <li>Save your category preferences</li>
              <li>Track your progress and streaks</li>
              <li>Improve our Service</li>
            </ul>
            <p className="text-gray-300 leading-relaxed mt-4">
              We do NOT sell your data, use it for advertising, or share it with other users.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">4. Data Storage and Security</h2>
            <ul className="list-disc list-inside text-gray-300 mt-2 space-y-1">
              <li>Your data is stored on secure servers in the United States</li>
              <li>We use industry-standard encryption (HTTPS/TLS)</li>
              <li>We implement access controls and security measures</li>
              <li>We do not store your TikTok access tokens long-term</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">5. Data Retention</h2>
            <p className="text-gray-300 leading-relaxed">
              We retain your data for as long as your account is active. You may request deletion
              of your data at any time by contacting us.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">6. Your Rights</h2>
            <p className="text-gray-300 leading-relaxed">You have the right to:</p>
            <ul className="list-disc list-inside text-gray-300 mt-2 space-y-1">
              <li><strong>Access</strong> — Request a copy of your data</li>
              <li><strong>Correction</strong> — Update inaccurate information</li>
              <li><strong>Deletion</strong> — Request deletion of your data</li>
              <li><strong>Portability</strong> — Receive your data in a portable format</li>
            </ul>
            <p className="text-gray-300 leading-relaxed mt-4">
              To exercise these rights, contact us at{' '}
              <a href="mailto:hello@fypglow.com" className="text-orange-500 hover:text-orange-400">
                hello@fypglow.com
              </a>
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">7. Children's Privacy</h2>
            <p className="text-gray-300 leading-relaxed">
              FYPGlow is not intended for children under 13. We do not knowingly collect data from
              children. If you believe we have collected data from a child, please contact us immediately.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">8. International Users</h2>
            <p className="text-gray-300 leading-relaxed">
              If you are accessing FYPGlow from outside the United States, please be aware that
              your data may be transferred to and processed in the United States.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">9. Changes to This Policy</h2>
            <p className="text-gray-300 leading-relaxed">
              We may update this Privacy Policy from time to time. We will notify you of significant
              changes by posting a notice on our website.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">10. Contact Us</h2>
            <p className="text-gray-300 leading-relaxed">
              If you have questions about this Privacy Policy, please contact us at:{' '}
              <a href="mailto:hello@fypglow.com" className="text-orange-500 hover:text-orange-400">
                hello@fypglow.com
              </a>
            </p>
          </section>
        </div>

        <div className="mt-12 pt-8 border-t border-gray-800">
          <Link to="/terms" className="text-orange-500 hover:text-orange-400">
            ← Terms of Service
          </Link>
        </div>
      </div>
    </div>
  );
};
