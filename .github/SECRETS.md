# GitHub Secrets Setup Guide

Configure the following secrets in your GitHub repository settings:

**Repository Settings → Secrets and variables → Actions → New repository secret**

## Required Secrets

### Deye Solar API Credentials
Obtain from [Deye Developer Portal](https://eu1-developer.deyecloud.com/)

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `EMAIL` | Deye developer portal email | `your-email@example.com` |
| `PASSWORD` | Deye developer portal password | `YourPassword123$` |
| `APP_ID` | Application ID from Deye portal | `202602173492014` |
| `APP_SECRET` | Application secret from Deye portal | `220ad749819468c91346a52cd66c3037` |

### Deye Device Information
Obtain from Deye mobile app

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `DEVICE_SN` | Device serial number | `2511053496` |
| `STATION_ID` | Station ID | `61831242` |

### Location Configuration

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `LATITUDE` | Location latitude | `20.238` |
| `LONGITUDE` | Location longitude | `100.001` |

### Database Configuration

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `PROD_DUCKDB_PATH` | MotherDuck database path | `md:luminos_prod` |
| `MOTHERDUCK_TOKEN` | MotherDuck access token | `eyJhxxxxx...` |

## Getting Your MotherDuck Token

1. Sign up at [MotherDuck](https://motherduck.com/)
2. Navigate to Settings → Access Tokens
3. Create a new token with read/write permissions
4. Copy the token value

## Important Notes

- **PROD_DUCKDB_PATH** should be in format: `md:database_name` (without the token)
- **MOTHERDUCK_TOKEN** should be the JWT token only (not the full connection string)
- Never commit these secrets to your repository
- Rotate secrets periodically for security
- Use GitHub organization secrets if managing multiple repositories

## Verifying Setup

After adding all secrets, test the workflow:

1. Go to **Actions** tab in your repository
2. Select **Daily ETL Pipeline**
3. Click **Run workflow** → **Run workflow** button
4. Monitor the job execution
5. Check MotherDuck database for new data in `raw` schema