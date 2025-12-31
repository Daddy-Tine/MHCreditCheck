# Resend Email Setup Guide

## Why Resend?

Resend provides:
- **Free tier**: 3,000 emails/month, 100 emails/day
- **Simple API**: Easy integration
- **Good deliverability**: High inbox rates
- **Domain verification**: Professional emails
- **Analytics**: Track email performance

## Step 1: Create Resend Account

1. Go to https://resend.com
2. Click "Get Started"
3. Sign up with email or GitHub
4. Verify your email

## Step 2: Get API Key

1. Go to **API Keys** in dashboard
2. Click "Create API Key"
3. Give it a name (e.g., "Credit Check Production")
4. Copy the API key (starts with `re_`)
5. **Important**: Save it now - you won't see it again!

## Step 3: Update Environment Variables

Add to your `backend/.env`:

```env
RESEND_API_KEY=re_xxxxxxxxxxxxx
EMAIL_FROM=noreply@yourdomain.com
```

## Step 4: Verify Domain (Production)

For production, you need to verify your domain:

1. Go to **Domains** in dashboard
2. Click "Add Domain"
3. Enter your domain (e.g., `yourdomain.com`)
4. Add DNS records to your domain:
   - **SPF Record**: `v=spf1 include:resend.com ~all`
   - **DKIM Record**: Copy from Resend dashboard
   - **DMARC Record**: `v=DMARC1; p=none;`
5. Wait for verification (usually < 5 minutes)

### Using Resend's Domain (Development)

For development/testing, you can use Resend's test domain:
```env
EMAIL_FROM=onboarding@resend.dev
```

**Note**: Emails from `resend.dev` are for testing only and may go to spam.

## Step 5: Test Email Sending

The application will automatically use Resend when:
- `RESEND_API_KEY` is set
- `EMAIL_FROM` is set
- `USE_SMTP=false` (default)

Test by triggering a user registration or password reset.

## Email Templates

The application includes these email functions:

### Verification Email
Sent when user registers:
```python
from app.utils.email import send_verification_email
await send_verification_email(user.email, token)
```

### Password Reset Email
Sent when user requests password reset:
```python
from app.utils.email import send_password_reset_email
await send_password_reset_email(user.email, token)
```

### Custom Email
Send any custom email:
```python
from app.utils.email import send_email
await send_email(
    to="user@example.com",
    subject="Welcome!",
    html="<h1>Welcome to Credit Check</h1>"
)
```

## Monitoring

### View Email Logs

1. Go to Resend dashboard
2. Click **Logs**
3. See all sent emails
4. Check delivery status

### Analytics

- **Delivery rate**: % of emails delivered
- **Open rate**: % of emails opened
- **Click rate**: % of links clicked
- **Bounce rate**: % of emails bounced

## Rate Limits

### Free Tier
- 3,000 emails/month
- 100 emails/day
- 10 emails/second

### Pro Tier ($20/month)
- 50,000 emails/month
- Unlimited per day
- 100 emails/second

## Troubleshooting

### Emails Not Sending

**Check**:
1. API key is correct
2. `EMAIL_FROM` is verified domain
3. Check Resend dashboard for errors
4. Review application logs

### Emails Going to Spam

**Solutions**:
1. Verify your domain (required for production)
2. Set up SPF, DKIM, DMARC records
3. Warm up your domain (send gradually)
4. Use professional email content

### API Key Invalid

**Solutions**:
1. Verify API key is correct
2. Check for extra spaces
3. Regenerate API key if needed
4. Ensure key hasn't been revoked

## Best Practices

1. **Always verify domain** for production
2. **Use professional email addresses** (noreply@, support@)
3. **Include unsubscribe links** (required by law in some regions)
4. **Monitor bounce rates** and remove invalid emails
5. **Warm up domain** gradually when starting
6. **Test emails** before sending to users

## Alternative: SMTP Fallback

If you prefer SMTP, you can use it instead:

1. Set `USE_SMTP=true` in `.env`
2. Configure SMTP settings:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

**Note**: Resend is recommended for better deliverability and simpler setup.

## Support

- **Resend Docs**: https://resend.com/docs
- **Resend Support**: support@resend.com
- **Resend Discord**: https://discord.gg/resend

