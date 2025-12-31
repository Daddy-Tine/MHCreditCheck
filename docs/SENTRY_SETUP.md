# Sentry Error Tracking Setup Guide

## Why Sentry?

Sentry provides:
- **Free tier**: 5,000 errors/month
- **Real-time alerts**: Get notified of errors immediately
- **Error context**: See what happened, where, and why
- **Performance monitoring**: Track API response times
- **Release tracking**: See which version has issues

## Step 1: Create Sentry Account

1. Go to https://sentry.io
2. Click "Get Started"
3. Sign up with email or GitHub
4. Verify your email

## Step 2: Create Organization

1. After signup, create an organization
2. Choose a name (e.g., "Credit Check")
3. Select plan: **Developer** (free tier)

## Step 3: Create Project

1. Click "Create Project"
2. Select platform: **FastAPI**
3. Give it a name: "Credit Check API"
4. Click "Create Project"

## Step 4: Get DSN

1. After creating project, you'll see setup instructions
2. Copy the **DSN** (Data Source Name)
3. It looks like: `https://xxx@xxx.ingest.sentry.io/xxx`

## Step 5: Update Environment Variables

Add to your `backend/.env`:

```env
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
ENABLE_SENTRY=true
```

## Step 6: Verify Setup

The application automatically initializes Sentry when:
- `SENTRY_DSN` is set
- `ENABLE_SENTRY=true`

To test:
1. Trigger an error in your application
2. Check Sentry dashboard
3. You should see the error appear

## What Sentry Tracks

### Automatic Tracking

- **Unhandled exceptions**: All Python exceptions
- **API errors**: FastAPI errors
- **Database errors**: SQLAlchemy errors
- **Performance**: Slow API endpoints

### Manual Tracking

You can also track custom events:

```python
import sentry_sdk

# Track custom event
sentry_sdk.capture_message("Something important happened", level="info")

# Track exception
try:
    risky_operation()
except Exception as e:
    sentry_sdk.capture_exception(e)
```

## Dashboard Features

### Issues

View all errors grouped by:
- Error type
- Frequency
- Affected users
- First/last seen

### Performance

Monitor:
- API response times
- Slow database queries
- Endpoint performance
- Transaction traces

### Releases

Track:
- Which version has errors
- Error rate per release
- Deployment impact

## Alerts

### Set Up Alerts

1. Go to **Alerts** in dashboard
2. Click "Create Alert Rule"
3. Configure:
   - **Trigger**: When error count > threshold
   - **Action**: Email, Slack, PagerDuty, etc.
4. Save alert

### Recommended Alerts

- **Critical errors**: Any error in production
- **High error rate**: > 10 errors/minute
- **New error types**: New error appears
- **Performance degradation**: API > 1 second

## Filtering & Search

### Filter Issues

- By environment (development, production)
- By release version
- By user
- By error type
- By time range

### Search

Use Sentry's search to find:
- Specific error messages
- Errors from specific users
- Errors in specific files
- Performance issues

## Best Practices

1. **Set environment**: Use `ENVIRONMENT=production` in production
2. **Filter noise**: Ignore expected errors (404s, etc.)
3. **Use releases**: Tag deployments with version numbers
4. **Set up alerts**: Get notified of critical issues
5. **Review regularly**: Check dashboard weekly
6. **Fix high-frequency errors**: Prioritize common issues

## Configuration Options

### Sample Rate

Control how many events are sent:

```python
# In main.py (already configured)
traces_sample_rate=0.1  # 10% of transactions
```

### Environment

Set environment for filtering:

```env
ENVIRONMENT=production
```

### Release

Tag releases for tracking:

```python
sentry_sdk.init(
    release="v1.0.0",
    # ...
)
```

## Free Tier Limits

- **5,000 errors/month**
- **10,000 performance units/month**
- **1 project**
- **Unlimited team members**

### When to Upgrade

Upgrade to **Team** ($26/month) when:
- Exceeding error limits
- Need more projects
- Need advanced features
- Need longer data retention

## Troubleshooting

### Errors Not Appearing

**Check**:
1. `SENTRY_DSN` is correct
2. `ENABLE_SENTRY=true`
3. Check application logs for Sentry errors
4. Verify network connectivity

### Too Many Errors

**Solutions**:
1. Filter out expected errors (404s, etc.)
2. Reduce sample rate
3. Use error filtering rules
4. Fix common errors

### Performance Impact

**Solutions**:
1. Reduce `traces_sample_rate`
2. Filter out non-critical errors
3. Use async error reporting
4. Monitor Sentry's own performance

## Privacy & Security

### Sensitive Data

Sentry automatically filters:
- Passwords
- Credit card numbers
- API keys
- Tokens

### Custom Filtering

Add custom data scrubbing:

```python
sentry_sdk.init(
    before_send=lambda event, hint: {
        # Remove sensitive data
        **event,
        'user': None if 'sensitive' in str(event) else event.get('user')
    }
)
```

## Integration with Other Tools

### Slack

1. Go to **Settings** → **Integrations**
2. Add Slack integration
3. Configure alerts to send to Slack

### GitHub

1. Link GitHub account
2. Create issues from Sentry errors
3. Track fixes in commits

### PagerDuty

1. Add PagerDuty integration
2. Set up on-call alerts
3. Escalate critical errors

## Support

- **Sentry Docs**: https://docs.sentry.io
- **Sentry Discord**: https://discord.gg/sentry
- **Sentry Support**: support@sentry.io

## Next Steps

After setting up Sentry:
1. ✅ Test error tracking
2. ✅ Set up alerts
3. ✅ Configure filters
4. ✅ Monitor dashboard
5. ✅ Review errors regularly

