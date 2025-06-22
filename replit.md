# Replit.md - Trucking Document Management System

## Overview

This is a Flask-based web application designed for trucking drivers to upload and manage their required documents for brokerage company registrations. The application provides a mobile-optimized interface with Russian language support, featuring document upload functionality and a comprehensive listing of major brokerage companies in the trucking industry.

## System Architecture

### Frontend Architecture
- **Framework**: HTML5 with Bootstrap 5.3.0 for responsive design
- **Styling**: Custom CSS with CSS Grid and Flexbox for mobile-first responsive layout
- **JavaScript**: Vanilla JavaScript for file upload interactions and form validation
- **UI Components**: Bootstrap components with custom styling for trucking industry branding
- **Language**: Russian language interface with English switcher option

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Form Handling**: Flask-WTF for secure form processing and CSRF protection
- **File Management**: Werkzeug utilities for secure file uploads
- **WSGI Server**: Gunicorn for production deployment
- **API Endpoints**: RESTful endpoints for form submission and status checking
- **Telegram Integration**: python-telegram-bot library for automated document distribution

### Data Storage Solutions
- **File Storage**: Local filesystem storage in `uploads/` directory with UUID-based organization
- **Session Management**: Flask sessions with configurable secret key
- **Subscriber Storage**: JSON-based subscriber management for Telegram bot
- **Database Ready**: Flask-SQLAlchemy and psycopg2-binary dependencies included for future database integration

### Telegram Bot Integration
- **Document Distribution**: Automatic forwarding of submitted documents to subscribers
- **Subscription Management**: Bot commands for subscribing/unsubscribing users
- **Real-time Notifications**: Instant delivery of driver applications with complete document packages
- **Async Processing**: Non-blocking document transmission with error handling

## Key Components

### Application Structure
- **`app.py`**: Main Flask application with route definitions and configuration
- **`main.py`**: Application entry point for WSGI deployment
- **`forms.py`**: WTForms definitions for document upload validation
- **`templates/`**: Jinja2 HTML templates for user interface
- **`static/`**: CSS, JavaScript, and image assets
- **`uploads/`**: File storage directory for uploaded documents

### Document Management
- **Supported Formats**: PDF, images (PNG, JPG, JPEG, GIF), documents (DOC, DOCX), text files
- **File Size Limit**: 16MB maximum per file
- **Required Documents**: CDL license, DOT medical certificate, social security card, vehicle registration, insurance certificate
- **Optional Documents**: IFTA permit, MC Authority documentation

### Brokerage Company Integration
- **Company Database**: Hard-coded list of 12 major trucking brokerage companies
- **Company Information**: Names and placeholder logos for visual reference
- **Display System**: Grid-based layout showcasing available brokerage partners

## Data Flow

1. **User Access**: Driver accesses the landing page with welcome message and company overview
2. **Document Upload**: User navigates to upload form and fills out personal information
3. **File Validation**: Frontend and backend validation ensures file types and sizes are acceptable
4. **File Processing**: Secure filename generation and storage in uploads directory
5. **Confirmation**: Success/error messages displayed to user via Flask flash messaging

## External Dependencies

### Python Packages
- **Flask**: Web framework for application structure
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation and rendering
- **Flask-SQLAlchemy**: Database ORM (prepared for future use)
- **Gunicorn**: Production WSGI server
- **psycopg2-binary**: PostgreSQL adapter (prepared for future use)
- **email-validator**: Email address validation
- **Werkzeug**: WSGI utilities and secure file handling

### Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework for responsive design
- **Font Awesome 6.4.0**: Icon library for UI enhancement

## Deployment Strategy

- **Platform**: Replit autoscale deployment
- **Server**: Gunicorn WSGI server binding to 0.0.0.0:5000
- **Environment**: Python 3.11 with Nix package management
- **SSL/TLS**: OpenSSL support included in environment
- **Database**: PostgreSQL support prepared in environment
- **Proxy Handling**: ProxyFix middleware for proper header handling behind reverse proxy

## Changelog

- June 21, 2025. Initial Flask application setup with mobile landing page
- June 21, 2025. Converted to static HTML site with embedded CSS/JS for simple deployment
- June 21, 2025. Complete redesign with modern light theme using Oswald font, converted all text to English including forms and buttons
- June 21, 2025. Updated welcome message with detailed owner-operator information, payment details, and app features. Changed "Upload Documents" to "Conclude Agreements"
- June 21, 2025. Converted to dark theme with owner photo integration
- June 21, 2025. Integrated document upload form directly into main page without redirects
- June 21, 2025. Configured Formspree.io integration for email form submissions with file attachments
- June 21, 2025. Migrated to Getform.io email service for reliable document submission handling
- June 21, 2025. Created static HTML version for Netlify deployment with all assets embedded
- June 21, 2025. Removed header navigation and converted all blue UI elements to gray theme (#888888) for consistent styling
- June 21, 2025. Added testimonial quote from Zafar Safarov with professional left-aligned styling
- June 21, 2025. Integrated "Download App" button and section with Google Play/App Store links
- June 21, 2025. Centered all text content throughout the landing page for better visual balance
- June 21, 2025. Converted all error messages and form feedback to English language
- June 21, 2025. Optimized page spacing by reducing section paddings from 80px to 40px for better content density
- June 21, 2025. Switched form submission from Netlify Forms to Getform.io for reliable email delivery
- June 21, 2025. Added mobile camera support with capture="environment" attribute for document photography
- June 21, 2025. Fixed double-click issue in file upload areas to prevent multiple dialog boxes
- June 21, 2025. Migrated from external email services (Getform.io, Formspree) to Netlify Forms for reliable form submission handling on static deployment
- June 21, 2025. Configured final Getform.io endpoint (byvymena) for production form submissions with file upload support
- June 22, 2025. Converted entire design from dark theme to modern light theme with improved contrast and accessibility
- June 22, 2025. Added language switcher with Russian as default language and English as secondary option
- June 22, 2025. Translated all content to Russian for default experience with English translations via data attributes
- June 22, 2025. Updated document requirements: removed CDL requirement from driver's license, removed IFTA permit and social security forms, added W9 form as required document
- June 22, 2025. Implemented comprehensive Telegram bot integration for automated document distribution to subscribers
- June 22, 2025. Migrated form submission from external services (Getform.io) to internal Replit server with /api/submit endpoint for Telegram integration
- June 22, 2025. Fixed critical import errors preventing app startup - resolved python-telegram-bot package conflicts with graceful fallback
- June 22, 2025. Changed language switcher from fixed floating position to absolute positioning within hero section
- June 22, 2025. Updated company logo blocks to black background with white logos for improved visual contrast
- June 22, 2025. Repositioned language switcher to prevent text overlap and improved mobile responsiveness
- June 22, 2025. Standardized button widths for "Start Working" and "Download App" buttons with consistent 220px width on desktop and full-width on mobile
- June 22, 2025. Unified line-height for all titles and headings to 1.0 for consistent compact spacing throughout the website
- June 22, 2025. Prepared Railway.com deployment configuration with railway.json, Procfile, pyproject.toml, and comprehensive documentation
- June 22, 2025. Configured dynamic PORT binding for Railway deployment and production environment detection
- June 22, 2025. Created detailed deployment guides (README.md, RAILWAY_DEPLOYMENT.md) with step-by-step instructions for GitHub integration
- June 22, 2025. Fixed Railway deployment issues by removing problematic pyproject.toml, creating nixpacks.toml configuration, and using standard requirements.txt for dependencies
- June 22, 2025. Resolved uv sync conflicts with Railway Nixpacks by switching to traditional pip install approach with proper dependency management

## User Preferences

Preferred communication style: Simple, everyday language.
Preferred deployment: Static HTML files for simplicity and portability.
Language preference: Full English text throughout the application including all forms, buttons, and content.
Design preference: Modern minimalist light theme with Oswald font, similar to etlgroupllc.com style.
Content preference: Detailed owner-operator guidance including maintenance advice, payment schedules, and app functionality.