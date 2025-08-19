# Snyk User Roles Bulk Update Tool

A Python CLI tool for bulk updating user roles using the Snyk API & Web (formerly Probely API). This tool provides a robust, user-friendly interface for managing multiple user role updates in a single operation.

## Features

- 🎯 **Interactive Mode**: User-friendly interface for selecting users and roles
- 🔐 **Secure API Integration**: Secure token input with environment variable support
- 📊 **Live Data Fetching**: Fetch current users, roles, and assignments from Snyk API
- ✅ **Multi-Selection Interface**: Select multiple users with intuitive checkbox interface
- 🔍 **Preview Changes**: Review all changes before execution
- 🔄 **Bulk Operations**: Update multiple user roles in a single API call
- 🛡️ **Error Handling**: Robust error handling with detailed error messages
- 🔄 **Retry Logic**: Automatic retry with exponential backoff for failed requests
- 📊 **Rich Output**: Beautiful console output with progress bars and tables
- 🧪 **Dry Run Mode**: Validate and preview changes without making actual updates
- 📝 **Template Generation**: Generate JSON templates for file-based updates
- 🎭 **Demo Mode**: Fallback to mock data when API endpoints are unavailable

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd snyk-user-roles-bulk-update
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your Snyk API token
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Required
SNYK_API_TOKEN=your_snyk_api_token_here

# Optional
SNYK_API_BASE_URL=https://api.snyk.io
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

### Getting Your Snyk API Token

1. Log in to your Snyk account
2. Go to Account Settings → API tokens
3. Create a new API token with appropriate permissions
4. Copy the token to your `.env` file

## Usage

### Command Line Interface

The tool provides several commands for different operations:

#### 1. Interactive Mode (Recommended)

```bash
# Launch interactive mode for user-friendly bulk updates
python main.py interactive
```

This interactive mode will:
- Prompt for your Snyk API token (if not set in environment)
- Fetch existing users and their current roles
- Display users in a formatted table
- Allow you to select multiple users for bulk updates
- Let you choose a new role to assign
- Preview changes before confirmation
- Execute the bulk update with progress feedback

#### 2. Bulk Update User Roles (File-based)

```bash
# Update user roles from a JSON file
python main.py update --config-file user_roles.json

# Dry run (validate without making changes)
python main.py update --config-file user_roles.json --dry-run

# Verbose output
python main.py update --config-file user_roles.json --verbose
```

#### 3. Generate Template

```bash
# Generate a template JSON file
python main.py template

# Specify custom output path
python main.py template --output my_template.json
```

#### 4. Validate User Roles

```bash
# Validate user roles without making changes
python main.py validate --config-file user_roles.json
```

### JSON File Format

Your user roles JSON file should follow this structure:

```json
{
  "user_roles": [
    {
      "id": "user_role_id_here",
      "user": {
        "id": "user_id_here"
      },
      "role": {
        "id": "role_id_here",
        "name": "Role Name",
        "permissions": [
          {
            "id": "permission_id",
            "name": "Permission Name"
          }
        ],
        "custom": true,
        "description": "Role description"
      },
      "scope": {
        "tier": "account",
        "team": {
          "id": "team_id_here",
          "name": "Team Name"
        }
      }
    }
  ]
}
```

#### Scope Tiers

- **`account`**: Account-level scope
- **`team`**: Team-level scope (requires team object)
- **`target`**: Target-level scope (requires target object)

## Interactive Features

### User-Friendly Interface

The interactive mode provides:

- **🔐 Secure Token Input**: Safely enter your API token with hidden input
- **📊 Data Visualization**: View users and roles in formatted tables
- **✅ Multi-Selection**: Choose multiple users with checkbox interface
- **🔍 Preview Changes**: See exactly what will be updated before confirming
- **⚡ Real-time Feedback**: Progress bars and status updates
- **🛡️ Error Handling**: Graceful fallback to demo mode if API is unavailable

### Demo Mode

When the Snyk API endpoints are not available (as they would be in a real implementation), the tool automatically falls back to demo mode with mock data, allowing you to test the interface and workflow.

## Examples

### Example 1: Interactive Mode (Recommended)

```bash
# Launch interactive mode
python main.py interactive

# Follow the prompts:
# 1. Enter your API token (or set SNYK_API_TOKEN environment variable)
# 2. View current user roles in a formatted table
# 3. Select users to update using checkbox interface
# 4. Choose the new role from available options
# 5. Preview changes and confirm
# 6. Watch the bulk update progress
```

### Example 2: Bulk Update Multiple User Roles (File-based)

1. **Prepare your data file:**
   ```json
   {
     "user_roles": [
       {
         "id": "ur_123456789abc",
         "user": {"id": "u_987654321def"},
         "role": {
           "id": "r_abcdef123456",
           "name": "Developer",
           "permissions": [
             {"id": "read", "name": "Read Access"},
             {"id": "write", "name": "Write Access"}
           ],
           "custom": false,
           "description": "Developer role with read/write access"
         },
         "scope": {
           "tier": "team",
           "team": {"id": "t_team123456", "name": "Engineering"}
         }
       }
     ]
   }
   ```

2. **Run the update:**
   ```bash
   python main.py update --config-file user_roles.json
   ```

### Example 3: Dry Run Validation

```bash
python main.py update --config-file user_roles.json --dry-run
```

This will validate your data without making any actual changes to your Snyk account.

### Example 4: Generate and Use Template

```bash
# Generate template
python main.py template --output my_roles.json

# Edit the template with your data
# Then validate
python main.py validate --config-file my_roles.json

# Finally update
python main.py update --config-file my_roles.json
```

## Error Handling

The tool provides comprehensive error handling:

- **Validation Errors**: Detailed validation of input data
- **API Errors**: Proper handling of HTTP errors and API responses
- **Network Errors**: Automatic retry with exponential backoff
- **Data Errors**: Clear error messages for malformed data

## Security Features

- **Environment Variables**: Secure storage of API tokens
- **Input Validation**: Comprehensive validation of all input data
- **HTTPS Only**: Enforces secure connections
- **Token Masking**: API tokens are never logged or displayed

## Development

### Project Structure

```
snyk-user-roles-bulk-update/
├── config.py          # Configuration management
├── models.py          # Pydantic data models
├── snyk_client.py     # Snyk API client
├── main.py            # CLI interface
├── requirements.txt   # Python dependencies
├── env.example        # Environment variables template
└── README.md          # This file
```

### Adding New Features

1. **Extend Models**: Add new fields to the Pydantic models in `models.py`
2. **Update Client**: Modify the API client in `snyk_client.py`
3. **Add Commands**: Extend the CLI interface in `main.py`

### Testing

```bash
# Run with sample data
python main.py template --output test_data.json
python main.py validate --config-file test_data.json
```

## Troubleshooting

### Common Issues

1. **Authentication Error**: Check your API token in the `.env` file
2. **Validation Errors**: Use the `validate` command to check your data format
3. **Network Errors**: Check your internet connection and firewall settings
4. **Permission Errors**: Ensure your API token has the required permissions

### Debug Mode

Enable verbose logging for detailed debugging:

```bash
python main.py update --config-file user_roles.json --verbose
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the Snyk API documentation
3. Open an issue in the repository
4. Contact Snyk support for API-related issues

## API Reference

This tool is designed to work with the [Snyk API & Web (formerly Probely) API](https://developers.probely.com/api/reference/). The tool automatically tries multiple endpoint paths to find the correct ones for your Snyk account:

### Primary Endpoints
- **Bulk Update**: `POST /user-roles/bulk/update/`
- **User Roles**: Multiple paths including `/user-roles/`, `/v1/user-roles/`, `/api/v1/user-roles/`
- **Users**: Multiple paths including `/users/`, `/v1/users/`, `/api/v1/users/`
- **Roles**: Multiple paths including `/roles/`, `/v1/roles/`, `/api/v1/roles/`

### API Documentation
- **Full API Reference**: [Snyk API & Web Reference](https://developers.probely.com/api/reference/)
- **User Roles Section**: [User Roles API](https://developers.probely.com/api/reference/#tag/User-Roles)
- **User Management Section**: [User Management API](https://developers.probely.com/api/reference/#tag/User-Management)
- **Roles & Permissions Section**: [Roles & Permissions API](https://developers.probely.com/api/reference/#tag/Roles-%26-Permissions)

### Note on Endpoints
The tool automatically tries multiple endpoint variations because Snyk API & Web may use different paths depending on your account type, plan, or API version. If the real API endpoints are not available, the tool gracefully falls back to demo mode with realistic mock data.

## Changelog

### Version 1.0.0
- Initial release
- Bulk update functionality
- Comprehensive validation
- Rich CLI interface
- Template generation
- Error handling and retry logic
