# Daily Reminder System

This repository contains a GitHub Actions workflow that sends daily morning and evening reminders via WeChat's webhook.

## Features

- Sends a "Good Morning" message at 9:00 AM (UTC+8) every day
- Sends a "Good Night" message at 10:00 PM (UTC+8) every day
- Uses WeChat's webhook API to deliver messages
- Can be manually triggered for testing

## Setup Instructions

### 1. Fork or Clone this Repository

Make sure you have your own copy of this repository in your GitHub account.

### 2. Set Up WeChat Webhook

1. Create a WeChat Work group chat
2. Add a webhook to the group (through the group settings)
3. Copy the webhook key (the part after `key=` in the URL)

### 3. Add the Webhook Key as a Secret

1. Go to your repository on GitHub
2. Navigate to Settings > Secrets and variables > Actions
3. Click "New repository secret"
4. Name: `WEBHOOK_KEY`
5. Value: Paste your webhook key
6. Click "Add secret"

### 4. Enable GitHub Actions

Make sure GitHub Actions is enabled for your repository:

1. Go to Settings > Actions > General
2. Under "Actions permissions", select "Allow all actions and reusable workflows"
3. Click "Save"

## Usage

### Automatic Execution

The workflow will automatically run at:
- 9:00 AM (UTC+8) every day for the morning message
- 10:00 PM (UTC+8) every day for the evening message

### Manual Testing

You can manually trigger the workflow to test it:

1. Go to the "Actions" tab in your repository
2. Select the "Daily Reminders" workflow
3. Click "Run workflow"
4. Choose either "morning" or "evening" from the dropdown
5. Click "Run workflow"

## Customization

To customize the messages:

1. Edit the `scripts/send_reminder.py` file
2. Modify the message content in the `if message_type == "morning":` and `elif message_type == "evening":` sections
3. Commit and push your changes

## Troubleshooting

If you encounter any issues:

1. Check the workflow run logs in the Actions tab
2. Ensure your webhook key is correctly set as a secret
3. Verify that the WeChat webhook is still active