// Dashboard JavaScript for real-time bot status updates

class DeploymentBotDashboard {
    constructor() {
        this.statusInterval = null;
        this.init();
    }

    init() {
        console.log('🚀 Initializing Deployment Bot Dashboard');
        this.startStatusPolling();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Refresh button if added later
        document.addEventListener('DOMContentLoaded', () => {
            console.log('✅ Dashboard loaded');
        });

        // Handle visibility change to pause/resume polling
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopStatusPolling();
            } else {
                this.startStatusPolling();
            }
        });
    }

    startStatusPolling() {
        // Initial load
        this.updateStatus();
        
        // Poll every 5 seconds
        this.statusInterval = setInterval(() => {
            this.updateStatus();
        }, 5000);
    }

    stopStatusPolling() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
            this.statusInterval = null;
        }
    }

    async updateStatus() {
        try {
            const response = await fetch('/api/status');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const status = await response.json();
            this.renderStatus(status);
        } catch (error) {
            console.error('❌ Error fetching bot status:', error);
            this.renderError();
        }
    }

    renderStatus(status) {
        // Update status indicator in navbar
        const statusIndicator = document.getElementById('status-indicator');
        if (status.is_ready) {
            statusIndicator.innerHTML = '<i class="fas fa-circle me-1"></i>Online';
            statusIndicator.className = 'badge bg-success';
        } else {
            statusIndicator.innerHTML = '<i class="fas fa-circle me-1"></i>Offline';
            statusIndicator.className = 'badge bg-danger pulse';
        }

        // Update bot status card
        this.updateElement('bot-status', status.is_ready ? 
            '<span class="badge bg-success">Online</span>' : 
            '<span class="badge bg-danger">Offline</span>'
        );

        this.updateElement('bot-user', status.user || 'Not logged in');
        this.updateElement('guild-count', status.guild_count || '0');
        this.updateElement('total-deployments', status.total_deployments || '0');

        // Update last deployment
        this.renderLastDeployment(status.last_deployment);
    }

    renderLastDeployment(deployment) {
        const container = document.getElementById('last-deployment');
        
        if (!deployment) {
            container.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-clock fa-2x mb-2"></i>
                    <p>No deployments created yet</p>
                </div>
            `;
            return;
        }

        const timestamp = new Date(deployment.timestamp).toLocaleString();
        
        container.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <div class="deployment-detail">
                        <strong>👑 Host:</strong>
                        <span>${this.escapeHtml(deployment.host)}</span>
                    </div>
                    <div class="deployment-detail">
                        <strong>🤝 Co-Host:</strong>
                        <span>${this.escapeHtml(deployment.cohost)}</span>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="deployment-detail">
                        <strong>📅 When:</strong>
                        <span>${this.escapeHtml(deployment.when)}</span>
                    </div>
                    <div class="deployment-detail">
                        <strong>🎁 Promotional:</strong>
                        <span>${deployment.promotional}</span>
                    </div>
                </div>
            </div>
            <div class="row mt-2">
                <div class="col-12">
                    <div class="deployment-detail">
                        <strong>📍 Channel:</strong>
                        <span>#${this.escapeHtml(deployment.channel)}</span>
                    </div>
                    <div class="deployment-detail">
                        <strong>🕒 Created:</strong>
                        <span>${timestamp}</span>
                    </div>
                </div>
            </div>
        `;
    }

    renderError() {
        // Update status indicator to show error
        const statusIndicator = document.getElementById('status-indicator');
        statusIndicator.innerHTML = '<i class="fas fa-exclamation-circle me-1"></i>Error';
        statusIndicator.className = 'badge bg-warning';

        // Update status elements to show error state
        this.updateElement('bot-status', '<span class="badge bg-warning">Connection Error</span>');
        this.updateElement('bot-user', 'Unable to fetch');
        this.updateElement('guild-count', 'N/A');
        this.updateElement('total-deployments', 'N/A');
    }

    updateElement(id, content) {
        const element = document.getElementById(id);
        if (element) {
            element.innerHTML = content;
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DeploymentBotDashboard();
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    console.log('👋 Dashboard closing');
});
