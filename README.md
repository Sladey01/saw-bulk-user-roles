# SAW Bulk User Roles Tool

A powerful interactive tool for managing user roles in Snyk API & Web (formerly Probely) with visual selection and arrow key navigation.

## ✨ Features

- **🎯 Interactive User Selection**: Navigate with arrow keys, select with SPACE
- **👁️ Visual Selection Indicators**: Clear `[ ]` and `[*]` indicators
- **🚀 Bulk Role Updates**: Update multiple users simultaneously
- **🔑 Real API Integration**: Works with actual Snyk API & Web (formerly Probely)
- **📱 Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your API token**:
   - Edit `config.py` with your Snyk API & Web token
   - Or set environment variables

3. **Run the tool**:
   ```bash
   python saw_bulk_user_roles.py
   ```

## 🎮 How to Use

### Navigation
- **↑↓ Arrow Keys**: Move between users
- **SPACE**: Toggle selection (`[ ]` ↔ `[*]`)
- **ENTER**: Continue to role selection
- **q**: Quit

### Selection
- **Single User**: Navigate with arrows, press SPACE to select
- **Multiple Users**: Select multiple users, then update all at once
- **Visual Feedback**: See `[ ]` for unselected, `[*]` for selected

### Role Updates
1. Select users with arrow keys + SPACE
2. Choose target role from available options
3. Preview changes before applying
4. Confirm to update all selected users

## 📁 Project Structure

```
saw-bulk-user-roles/
├── saw_bulk_user_roles.py # Main interactive tool
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Configuration

### API Details
This tool uses the **Snyk API & Web** (formerly Probely API) for user role management:
- **Endpoint**: `https://api.probely.com`
- **API Reference**: [Snyk API & Web Documentation](https://developers.probely.com/api/reference/)
- **Authentication**: JWT token-based authentication

### How Configuration Works
The tool uses a two-file configuration system:
- **`config.py`** - Handles the logic and loads your settings
- **`.env`** - Stores your actual API token (never committed to git)

### Quick Setup (Recommended)
1. **Copy the template**:
   ```bash
   cp env.example .env
   ```

2. **Edit `.env` with your actual token**:
   ```bash
   nano .env
   ```
   Your `.env` file should look like:
   ```bash
   PROBELY_API_TOKEN=your_actual_token_here
   PROBELY_API_BASE_URL=https://api.probely.com
   ```

3. **Run the tool**:
   ```bash
   python saw_bulk_user_roles.py
   ```

### Getting Your API Token
1. Log in to your Snyk account
2. Go to Account Settings → API tokens
3. Create a new API token with user role management permissions
4. **Never commit your actual token to version control!**

### Why This Setup?
- ✅ **Secure**: Your token stays local and private
- ✅ **Convenient**: No need to set environment variables manually
- ✅ **Standard**: Follows Python development best practices
- ✅ **Flexible**: Easy to manage different tokens for different environments

## 📋 Requirements

- Python 3.7+
- `requests` - HTTP API calls
- `rich` - Beautiful terminal output

## 🎯 Use Cases

- **Bulk Role Management**: Update multiple users to the same role
- **Role Auditing**: Review current user roles across your organization
- **User Onboarding**: Quickly assign roles to new team members
- **Role Changes**: Update user permissions as responsibilities change
- **Security Assessment**: Manage user access for security testing environments

## 🔒 Security

- API tokens are stored in configuration files
- No sensitive data is logged or displayed
- All API calls use HTTPS
- Role updates require confirmation before applying

## 🚨 Important Notes

- **Owner Role**: Cannot be assigned or removed via API (Snyk API & Web restriction)
- **Permissions**: Ensure your API token has sufficient permissions for user role management
- **Backup**: Always review changes before applying bulk updates

## 🆘 Troubleshooting

### Common Issues
- **Arrow Keys Not Working**: Ensure terminal supports ANSI escape sequences
- **API Errors**: Check your Snyk API & Web token and permissions
- **Selection Issues**: Use SPACE to toggle, not ENTER

### Configuration Issues
- **"API token required" error**: Make sure you have created `.env` from `env.example`
- **"Module not found" error**: Install dependencies with `pip install -r requirements.txt`
- **"Authentication failed" error**: Verify your API token is correct and has proper permissions

### Alternative Setup (Advanced Users)
If you prefer to use environment variables directly instead of `.env`:
```bash
export PROBELY_API_TOKEN="your_token_here"
export PROBELY_API_BASE_URL="https://api.probely.com"
python saw_bulk_user_roles.py
```

## 🔌 API Endpoints

This tool uses the following Snyk API & Web endpoints:

- **`GET /users/`** - Fetch all users and their current roles
- **`GET /roles/`** - Fetch available roles in your organization
- **`POST /user-roles/bulk/update/`** - Bulk update user roles

For detailed API documentation, visit: [Snyk API & Web Reference](https://developers.probely.com/api/reference/)

## 📝 License

This tool is provided as-is for educational and administrative purposes.
