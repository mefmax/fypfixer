import React from 'react';
import { Link } from 'react-router-dom';

export const TermsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white">
      <div className="max-w-3xl mx-auto px-4 py-12">
        <Link to="/" className="text-orange-500 hover:text-orange-400 mb-8 inline-block">
          ← Back to FYPGlow
        </Link>

        <h1 className="text-3xl font-bold text-orange-500 mb-2">Terms of Service</h1>
        <p className="text-gray-400 mb-8">Last updated: December 23, 2025</p>

        <div className="prose prose-invert prose-orange max-w-none space-y-6">
          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">1. Agreement to Terms</h2>
            <p className="text-gray-300 leading-relaxed">
              By accessing or using FYPGlow ("Service"), you agree to be bound by these Terms of Service.
              If you disagree with any part of these terms, you may not access the Service.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">2. Description of Service</h2>
            <p className="text-gray-300 leading-relaxed">
              FYPGlow is a web application designed to help users improve their TikTok For You Page (FYP)
              recommendations. The Service provides personalized daily action plans, category-based content
              recommendations, and progress tracking features.
            </p>
            <p className="text-gray-300 leading-relaxed mt-4">
              FYPGlow is not affiliated with, endorsed by, or sponsored by TikTok or ByteDance.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">3. Account Registration</h2>
            <p className="text-gray-300 leading-relaxed">To use FYPGlow, you must:</p>
            <ul className="list-disc list-inside text-gray-300 mt-2 space-y-1">
              <li>Sign in using your TikTok account</li>
              <li>Be at least 13 years of age (or the minimum age in your country)</li>
              <li>Provide accurate and complete information</li>
              <li>Maintain the security of your account</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">4. Acceptable Use</h2>
            <p className="text-gray-300 leading-relaxed">You agree NOT to:</p>
            <ul className="list-disc list-inside text-gray-300 mt-2 space-y-1">
              <li>Use the Service for any illegal purpose</li>
              <li>Violate TikTok's Terms of Service while using our recommendations</li>
              <li>Attempt to manipulate or abuse the Service</li>
              <li>Share your account credentials with others</li>
              <li>Use automated tools to access the Service</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">5. Intellectual Property</h2>
            <p className="text-gray-300 leading-relaxed">
              The Service and its original content, features, and functionality are owned by FYPGlow
              and are protected by international copyright, trademark, and other intellectual property laws.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">6. Third-Party Services</h2>
            <p className="text-gray-300 leading-relaxed">
              FYPGlow integrates with TikTok for authentication. Your use of TikTok is governed by
              TikTok's own Terms of Service and Privacy Policy. We are not responsible for TikTok's
              practices or policies.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">7. Disclaimers</h2>
            <p className="text-gray-300 leading-relaxed">
              THE SERVICE IS PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND. We do not guarantee that
              the Service will improve your TikTok recommendations, be uninterrupted or error-free,
              or that results will meet your expectations.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">8. Limitation of Liability</h2>
            <p className="text-gray-300 leading-relaxed">
              TO THE MAXIMUM EXTENT PERMITTED BY LAW, FYPGLOW SHALL NOT BE LIABLE FOR ANY INDIRECT,
              INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES RESULTING FROM YOUR USE OF THE SERVICE.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">9. Changes to Terms</h2>
            <p className="text-gray-300 leading-relaxed">
              We reserve the right to modify these terms at any time. We will notify users of significant
              changes by posting a notice on our website. Continued use of the Service after changes
              constitutes acceptance of the new terms.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-white mt-8 mb-4">10. Contact Us</h2>
            <p className="text-gray-300 leading-relaxed">
              If you have questions about these Terms, please contact us at:{' '}
              <a href="mailto:hello@fypglow.com" className="text-orange-500 hover:text-orange-400">
                hello@fypglow.com
              </a>
            </p>
          </section>
        </div>

        <div className="mt-12 pt-8 border-t border-gray-800">
          <Link to="/privacy" className="text-orange-500 hover:text-orange-400">
            Privacy Policy →
          </Link>
        </div>
      </div>
    </div>
  );
};
