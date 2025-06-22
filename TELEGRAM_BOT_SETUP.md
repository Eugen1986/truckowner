# Telegram Bot Integration Guide

## Overview

This project now includes a Telegram bot that automatically receives document submissions from the website form and forwards them to subscribers. The bot provides real-time notifications when drivers submit their documents.

## Bot Features

- **Automatic Document Distribution**: When a driver submits documents through the website form, they are automatically sent to all bot subscribers
- **Subscription Management**: Users can subscribe/unsubscribe to receive notifications
- **Document Organization**: Each submission includes:
  - Driver's personal information (name, phone, email, experience)
  - All uploaded documents (driver's license, medical certificate, W9 form, vehicle registration, insurance certificate, MC Authority)
  - Submission timestamp

## Bot Commands

- `/start` - Subscribe to document notifications
- `/stop` - Unsubscribe from notifications  
- `/status` - Check subscription status

## How It Works

### For Website Users (Drivers)
1. Driver fills out the form on the website
2. Uploads required documents
3. Submits the form
4. Documents are automatically processed and sent to bot subscribers

### For Bot Subscribers (Dispatch Companies)
1. Find the bot on Telegram (username will be provided after bot setup)
2. Send `/start` command to subscribe
3. Receive instant notifications when new applications arrive
4. Get all documents and driver information directly in Telegram

## Technical Architecture

### Backend Integration
- **Form Handler**: `/api/submit` endpoint processes form submissions
- **Document Processing**: Files are validated and prepared for transmission
- **Telegram Integration**: Documents and data are sent to all subscribers
- **Backup Systems**: Email fallback and local file storage

### Bot Infrastructure
- **Subscriber Management**: Automatic storage of subscriber chat IDs
- **File Handling**: Supports all document formats (PDF, images, Word docs)
- **Error Handling**: Robust error handling and subscriber cleanup
- **Async Processing**: Non-blocking document transmission

## Deployment Requirements

### Environment Variables
- `TELEGRAM_BOT_TOKEN` - Required bot token from @BotFather

### Bot Setup Process
1. Contact @BotFather on Telegram
2. Create new bot with `/newbot` command
3. Choose bot name (e.g., "Trucking Documents Bot")
4. Choose username (e.g., "trucking_docs_bot")
5. Copy the provided token to TELEGRAM_BOT_TOKEN environment variable

### Running the Bot
The bot is automatically initialized when the Flask application starts. For active command handling, you can optionally run:

```bash
python run_bot.py
```

This enables users to interact with the bot through commands.

## Benefits

### For Dispatch Companies
- **Instant Notifications**: Receive applications immediately
- **Organized Documents**: All files clearly labeled and organized
- **Complete Information**: Full driver profile with each submission
- **No Email Dependency**: Direct Telegram delivery

### For Drivers
- **Simplified Process**: Single form submission
- **Reliable Delivery**: Multiple delivery methods (Telegram + email backup)
- **Professional Response**: Faster processing by dispatch companies

## Security Features

- **File Validation**: Only allowed file types accepted
- **Size Limits**: 16MB maximum file size
- **Spam Protection**: Honeypot fields and validation
- **Subscriber Management**: Automatic cleanup of invalid chat IDs

## Monitoring

The system includes comprehensive logging for:
- Bot initialization status
- Document submission success/failure
- Telegram delivery status
- Subscriber management events
- Error tracking and resolution