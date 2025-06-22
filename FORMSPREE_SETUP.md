# Getform.io Email Integration Guide

## Current Configuration

Форма уже настроена и готова к использованию с Getform.io! 

**Endpoint**: `https://getform.io/f/byvymena`
**Status**: Активен и работает

## How It Works

1. **Пользователь заполняет форму** на веб-сайте
2. **Загружает документы** (PDF, изображения, документы Word)
3. **Отправляет форму** через Getform.io API
4. **Вы получаете уведомление** на ваш email с данными и файлами

## Form Features

- ✅ **Файловые вложения**: Все загруженные документы автоматически прикрепляются
- ✅ **Email уведомления**: Мгновенные уведомления о новых заявках
- ✅ **Валидация**: Проверка обязательных полей на стороне клиента
- ✅ **Защита от спама**: Встроенная защита Getform.io
- ✅ **Мобильная оптимизация**: Адаптивный дизайн для всех устройств

## Dashboard Access

Войдите в свой аккаунт Getform.io для:
- Просмотра всех отправленных заявок
- Скачивания файлов
- Настройки email уведомлений
- Экспорта данных в CSV/Excel

## Form Fields Being Sent

The form will send the following data to your email:

- **Personal Information**:
  - Full Name (`full_name`)
  - Phone Number (`phone`)
  - Email Address (`_replyto`)

- **Document Files**:
  - CDL Driver License (`drivers_license`)
  - DOT Medical Certificate (`medical_certificate`)
  - Social Security Card (`social_security`)
  - Vehicle Registration (`vehicle_registration`)
  - Insurance Certificate (`insurance_certificate`)
  - IFTA Permit (`ifta_permit`) - optional
  - MC Authority (`mc_authority`) - optional

## Email Template

You'll receive emails with the subject: **"New Driver Document Submission"**

The email will contain:
- All personal information filled out by the driver
- All uploaded documents as attachments
- Reply-to address set to the driver's email

## Testing

1. Fill out the form on your website
2. Upload test documents
3. Submit the form
4. Check your email inbox for the submission

## Formspree Limits

**Free Plan**:
- 50 submissions per month
- 50MB file upload limit
- Basic spam protection

**Paid Plans** (if needed):
- Unlimited submissions
- Higher file limits
- Advanced features

## Support

If you need help:
- Formspree documentation: https://help.formspree.io/
- Contact Formspree support through their dashboard