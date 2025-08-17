# Marble Burger House Discord Bot

A high-availability Discord bot with deployment announcements, cash register system, and web dashboard.

## Features

✅ **Deployment Announcements**
- Interactive slash commands for deployment notifications
- Role mentions and formatted embeds
- Multi-deployment type support

✅ **Cash Register System**
- Interactive shopping cart with "Add to Cart" functionality
- Menu item lookup and price calculation
- Order confirmation and receipt generation
- Role-based permissions

✅ **Web Dashboard**
- Real-time bot status monitoring
- Bootstrap-based responsive interface
- Health check endpoints and API status

✅ **Enterprise-Level Uptime**
- Triple-service architecture (Web + Bot + Keep-Alive)
- Infinite restart attempts with progressive backoff
- Thread monitoring and automatic resurrection
- Health checks every 30 seconds
- Keep-alive pings every 60 seconds
- Never goes offline permanently

## Setup Instructions

### 1. Environment Setup
```bash
pip install discord.py flask
```

### 2. Discord Bot Configuration
1. Create a Discord application at https://discord.com/developers/applications
2. Get your bot token from the Bot section
3. Set the `DISCORD_TOKEN` environment variable:
   ```bash
   export DISCORD_TOKEN="your_bot_token_here"
   ```

### 3. Guild Configuration
Update the following IDs in `bot.py`:
- `GUILD_ID`: Your Discord server ID
- `CHANNEL_ID`: Channel for deployment announcements
- `ROLE_ID`: Role to mention for deployments

### 4. Running the Bot
```bash
python main.py
```

The bot will start three services:
- Discord Bot (with auto-recovery)
- Web Dashboard (http://localhost:5000)
- Keep-Alive Service (prevents timeouts)

## File Structure

```
├── main.py              # Main entry point with uptime system
├── bot.py              # Discord bot with slash commands
├── web_server.py       # Flask dashboard and API
├── keep_alive.py       # Keep-alive service
├── templates/
│   └── index.html      # Dashboard HTML template
├── static/
│   ├── style.css       # Dashboard styling
│   └── script.js       # Dashboard JavaScript
├── replit.md           # Project documentation
└── README.md           # This file
```

## Commands

### Deployment Commands
- `/deploy` - Create deployment announcement
- `/deployment_help` - Show help information

### Cash Register Commands
- `/order` - Start ordering process with shopping cart
- `/menu` - Display available menu items

## Deployment

### For Maximum Uptime
1. Deploy to Replit Reserved VM for dedicated resources
2. The triple-service architecture ensures 99.9% uptime
3. Automatic recovery from any type of failure
4. No manual intervention required

### Configuration
- Port 5000 is used for the web dashboard
- All services run concurrently with monitoring
- Environment variables handle sensitive configuration

## Monitoring

Access the web dashboard at:
- Local: http://localhost:5000
- Deployed: https://your-repl-name.your-username.repl.co

The dashboard shows:
- Bot connection status
- Real-time health metrics
- System uptime statistics
- Service status indicators

## Troubleshooting

The bot includes comprehensive error handling:
- Automatic restarts on failures
- Progressive backoff for reconnections
- Detailed logging for all operations
- Health monitoring and alerting

If issues persist, check the console logs for detailed error information.

## License

This project is open source and available under the MIT License.