# How to Make an API Key - Complete Tutorial

## Overview

This tutorial will guide you through the complete process of creating an API key for the Storylinez platform. API keys are essential for accessing the Storylinez API and SDK, allowing you to integrate Storylinez's powerful content creation capabilities into your applications.

## Prerequisites

- A Storylinez account with access to the dashboard
- Developer clearance (required for API access)
- Access to the Settings page in your Storylinez dashboard

## Step-by-Step Guide

### Step 1: Accessing the Settings Page

1. **Log into your Storylinez account**
   - Go to [https://app.storylinezads.com](https://app.storylinezads.com)
   - Click "Sign In" and enter your credentials
   - You'll be redirected to your dashboard

2. **Navigate to Settings**
   - Click on your profile icon in the top right corner
   - Select "Settings" from the dropdown menu
   - Or directly navigate to `/settings` in your browser

### Step 2: Understanding Developer Clearance

Before creating API keys, you need developer clearance:

1. **Check Your Developer Status**
   - In the Settings page, navigate to the "Developer" tab
   - Look for the "API Keys" section
   - If you don't have clearance, you'll see a "Request Developer Access" button

2. **Request Developer Access (if needed)**
   - Click "Request Developer Access"
   - Fill out the access request form with:
     - **Reason for API access**: Explain why you need API access
     - **Use case**: Describe what you plan to build
     - **Contact email**: Your preferred contact email
     - **Organization size**: Select your organization size
     - **Industry**: Choose your industry category
     - **Expected usage**: Describe your expected API usage patterns
   - Submit the request
   - Wait for approval (typically 1-3 business days)

### Step 3: Creating Your API Key

Once you have developer clearance:

1. **Navigate to API Keys Section**
   - In Settings, click on the "Developer" tab
   - Scroll to the "API Keys" section
   - Click "Create New API Key"

2. **Configure Your API Key**
   - **Name**: Give your API key a descriptive name (e.g., "Production App", "Testing Environment")
   - **Description**: Add a detailed description of what this key will be used for
   - **Allowed Methods**: Select the HTTP methods your application will use:
     - `GET` - For reading data
     - `POST` - For creating new resources
     - `PUT` - For updating existing resources
     - `DELETE` - For removing resources
   - **Expiration**: Set an expiration time (optional but recommended for security)
   - **Admin Access**: Check this if you need admin-level permissions (use carefully)

3. **Generate the API Key**
   - Click "Create API Key"
   - **IMPORTANT**: Copy both the API Key and API Secret immediately
   - The API Secret will only be shown once and cannot be retrieved later
   - Store both values securely

### Step 4: Managing Your API Keys

#### Viewing API Keys
- All your API keys are listed in the "API Keys" section
- You can see:
  - Key name and description
  - Creation date
  - Last used date
  - Expiration status
  - Usage statistics (requests made)

#### Editing API Keys
- Click the "Edit" button (pencil icon) next to any API key
- You can modify:
  - Name and description
  - Allowed methods
  - Admin access
  - Expiration date
- Click "Save Changes" to apply

#### Rotating API Keys
- For security, you can rotate (regenerate) the secret for any API key
- Click the "Rotate" button next to your API key
- A new secret will be generated
- **Important**: Update your applications with the new secret immediately

#### Viewing Usage Statistics
- Click the "View Usage" button to see detailed usage statistics
- View information like:
  - Total requests made
  - Requests by time period (today, this week, this month)
  - Request methods used
  - Recent request history

#### Deleting API Keys
- Click the "Delete" button (trash icon) next to the API key you want to remove
- Confirm the deletion
- **Warning**: This action cannot be undone

### Step 5: Storing Your API Credentials Securely

#### Environment Variables (Recommended)
Create a `.env` file in your project:

```env
STORYLINEZ_API_KEY=api_your_key_here
STORYLINEZ_API_SECRET=your_secret_here
STORYLINEZ_ORG_ID=your_org_id_here
```

#### Configuration Files
Store in a secure configuration file:

```json
{
  "api_key": "api_your_key_here",
  "api_secret": "your_secret_here",
  "org_id": "your_org_id_here"
}
```

#### Important Security Notes
- Never commit API credentials to version control
- Use environment variables in production
- Rotate keys regularly
- Monitor usage for any suspicious activity
- Set appropriate expiration dates

### Step 6: Testing Your API Key

#### Using curl
```bash
curl -X GET "https://api.storylinezads.com/status" \
  -H "X-API-Key: your_api_key_here" \
  -H "X-API-Secret: your_api_secret_here"
```

#### Using Python
```python
import requests

headers = {
    'X-API-Key': 'your_api_key_here',
    'X-API-Secret': 'your_api_secret_here'
}

response = requests.get('https://api.storylinezads.com/status', headers=headers)
print(response.json())
```

## Common Issues and Solutions

### Issue: "Request Developer Access" button not appearing
**Solution**: Make sure you're logged in and have access to the Settings page. Contact support if the issue persists.

### Issue: API key creation fails
**Solution**: 
- Check that you have developer clearance
- Ensure all required fields are filled
- Try refreshing the page and attempting again

### Issue: API key not working in requests
**Solution**:
- Verify you're using the correct API key and secret
- Check that the key hasn't expired
- Ensure you have the right permissions (allowed methods)
- Verify the endpoint URL is correct

### Issue: Lost API secret
**Solution**: 
- API secrets cannot be retrieved once lost
- Use the "Rotate" feature to generate a new secret
- Update your applications with the new secret

## Best Practices

1. **Use Descriptive Names**: Name your API keys clearly to identify their purpose
2. **Set Expiration Dates**: Implement key rotation for better security
3. **Monitor Usage**: Regularly check usage statistics for unusual activity
4. **Principle of Least Privilege**: Only grant necessary permissions
5. **Secure Storage**: Never expose API credentials in client-side code
6. **Regular Rotation**: Rotate keys periodically for enhanced security
7. **Documentation**: Document what each API key is used for

## Rate Limiting

- Each API key has default rate limits to ensure fair usage
- You can view your current rate limits in the API key details
- Contact support if you need higher rate limits for production use

## Next Steps

Once you have your API key:
1. Read the [API Documentation](https://docs.storylinezads.com)
2. Install the [Storylinez SDK](https://docs.storylinezads.com/sdk)
3. Follow the [SDK Usage Tutorial](./5_how_to_use_sdk.md)
4. Explore the [API Reference](https://docs.storylinezads.com/api)

## Support

If you encounter any issues:
- Check the [FAQ](https://docs.storylinezads.com/faq)
- Review the [API Documentation](https://docs.storylinezads.com)
- Contact support through the dashboard
- Check our [knowledge base](https://docs.storylinezads.com) for detailed guides

---

*Last updated: January 2025*
