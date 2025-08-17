# Overview

This is a multi-functional Discord bot for Marble Burger House with deployment announcements and cash register capabilities, plus a web dashboard interface. The bot allows users to create structured deployment announcements and process restaurant orders using slash commands. It includes automatic role mentioning, formatted messages, and a Flask-based web dashboard for monitoring bot status and health in real-time.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Components

**Discord Bot Architecture**: Built using discord.py with slash command support. The bot uses a custom `MyClient` class extending `commands.Bot` with async setup hooks for command syncing. Features dual functionality with deployment announcements and cash register order processing. Commands are scoped to specific guilds for faster deployment and testing.

**High-Availability Service Design**: The application runs three services simultaneously with enterprise-level fault tolerance: Flask web server, Discord bot, and keep-alive service. The main entry point uses threading with comprehensive monitoring that restarts failed services automatically. Features include infinite restart attempts with progressive backoff, health monitoring, keep-alive pings, thread resurrection, and system status reporting to ensure 99.9% uptime.

**Configuration Management**: Environment-based configuration with hardcoded fallbacks for Discord tokens, guild/channel/role IDs. This allows for flexible deployment across different environments while maintaining development defaults.

**Real-time Status Tracking**: Global bot status dictionary shared between the Discord bot and web server, enabling real-time status updates in the dashboard without requiring database persistence. Enhanced with heartbeat monitoring and comprehensive logging for operational visibility.

**Cash Register System**: Integrated order processing functionality with menu item lookup, quantity parsing, price calculation, and receipt generation. Role-based permissions ensure only authorized users can place orders.

## Web Dashboard

**Frontend Architecture**: Bootstrap-based responsive dashboard with real-time status updates using JavaScript polling. The interface provides bot health monitoring, status indicators, and deployment statistics.

**API Design**: RESTful endpoints for bot status (`/api/status`) and health checks (`/api/health`). The status endpoint returns JSON data consumed by the dashboard's JavaScript for live updates.

**Styling Approach**: Custom CSS with dark theme gradient backgrounds and hover effects, designed to match Discord's aesthetic while maintaining professional dashboard appearance.

# External Dependencies

## Core Dependencies
- **discord.py**: Primary Discord API library for bot functionality and slash command support
- **Flask**: Web framework for the monitoring dashboard and API endpoints

## Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework for responsive dashboard layout and components
- **Font Awesome 6.4.0**: Icon library for visual elements in the dashboard interface

## Infrastructure
- **Discord API**: Integration for bot operations, slash commands, and message posting with automatic reconnection
- **Environment Variables**: Used for configuration management of Discord tokens and IDs
- **Threading**: Python threading module for concurrent execution of bot and web server
- **Fault Tolerance**: Multi-layered error handling with infinite restart attempts, progressive backoff, heartbeat monitoring, keep-alive service, thread resurrection, and comprehensive system monitoring
- **Logging**: Comprehensive logging system for monitoring bot health and troubleshooting issues