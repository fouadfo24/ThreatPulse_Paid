# EDR Security Dashboard

A simple yet comprehensive Endpoint Detection and Response (EDR) dashboard for localhost monitoring. This dashboard provides real-time monitoring of system resources, processes, network connections, file activities, and security alerts.

## Features

🔍 **Real-time System Monitoring**
- CPU, Memory, and Disk usage tracking
- Live process monitoring with resource consumption
- Network connection monitoring
- File system activity tracking

🛡️ **Security Monitoring**
- Suspicious process detection
- File system event monitoring
- Security alert generation
- Real-time threat detection

📊 **Modern Dashboard Interface**
- Responsive web-based interface
- Multiple monitoring tabs
- Real-time data updates
- Beautiful charts and progress bars

## Screenshots

The dashboard includes:
- **System Overview**: Real-time system metrics with visual progress bars
- **Process Monitor**: Live view of running processes with resource usage
- **Network Monitor**: Active network connections and their status
- **File Activity**: File system events and modifications
- **Security Alerts**: Comprehensive security event notifications

## Installation

### Prerequisites
- Python 3.7 or higher
- pip3 (Python package manager)
- Linux/Unix system (tested on Ubuntu/Debian)

### Quick Start

1. **Clone or download** the files to your local machine

2. **Run the startup script**:
   ```bash
   chmod +x start_edr.sh
   ./start_edr.sh
   ```

3. **Access the dashboard** at `http://localhost:5000`

### Manual Installation

If you prefer to install manually:

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the application
python3 app.py
```

## Usage

1. **Launch the dashboard** using the startup script or manually
2. **Open your browser** and navigate to `http://localhost:5000`
3. **Navigate through tabs** to view different monitoring aspects:
   - **Dashboard**: System overview with key metrics
   - **Processes**: Running processes and resource usage
   - **Network**: Active network connections
   - **Files**: File system activity monitoring
   - **Alerts**: Security alerts and notifications

## Security Features

### Process Monitoring
- Detects suspicious processes (netcat, telnet, etc.)
- Monitors process resource consumption
- Tracks command-line arguments

### File System Monitoring
- Monitors `/tmp` directory for file changes
- Detects modifications to sensitive files
- Tracks executable file creation

### Network Monitoring
- Lists active network connections
- Shows local and remote addresses
- Monitors connection status

### Alert System
- **High Severity**: Modifications to sensitive system files
- **Medium Severity**: Suspicious process execution, executable file creation
- **Low Severity**: General system events

## Configuration

### Monitored Directories
By default, the dashboard monitors:
- `/tmp` directory (recursively)
- System-wide processes
- All network connections

### Suspicious Processes
The system flags these process names as suspicious:
- `nc`, `netcat`, `ncat`, `socat`
- `telnet`, `wget`, `curl`
- `powershell`, `cmd`, `bash`, `sh`
- `python`, `perl`, `ruby`

### Sensitive Files
Alerts are generated for changes to:
- `/etc/passwd`
- `/etc/shadow`
- `/etc/hosts`
- Files in `/tmp`

## API Endpoints

The dashboard provides REST API endpoints:

- `GET /api/system` - System metrics (CPU, memory, disk)
- `GET /api/processes` - Running processes
- `GET /api/network` - Network connections
- `GET /api/alerts` - Security alerts
- `GET /api/file-events` - File system events
- `GET /api/suspicious-processes` - Suspicious processes

## Troubleshooting

### Common Issues

1. **Permission Errors**
   - Run with appropriate permissions for system monitoring
   - Some features may require root access

2. **Port Already in Use**
   - The dashboard runs on port 5000 by default
   - Kill existing processes: `sudo lsof -t -i:5000 | xargs kill`

3. **Dependencies Issues**
   - Ensure Python 3.7+ is installed
   - Update pip: `pip3 install --upgrade pip`

4. **No Data Showing**
   - Check console for JavaScript errors
   - Verify API endpoints are responding
   - Ensure proper permissions for system monitoring

### Performance Tips

- The dashboard auto-refreshes every 5 seconds
- File monitoring is limited to 100 recent events
- Alert history is capped at 50 items
- Consider running on a dedicated monitoring system

## Security Considerations

⚠️ **Important Security Notes**:

1. **Local Access Only**: This dashboard is designed for localhost monitoring only
2. **No Authentication**: The dashboard has no built-in authentication
3. **Development Mode**: Flask runs in debug mode - not suitable for production
4. **System Access**: The application requires system-level access for monitoring

## Dependencies

- **Flask 2.3.3**: Web framework
- **psutil 5.9.5**: System and process monitoring
- **watchdog 3.0.0**: File system monitoring
- **flask-socketio 5.3.6**: Real-time updates
- **requests 2.31.0**: HTTP requests
- **eventlet 0.33.3**: Concurrent networking

## License

This project is provided as-is for educational and monitoring purposes. Use responsibly and in accordance with your organization's security policies.

## Contributing

Feel free to enhance the dashboard with additional features:
- More sophisticated threat detection
- Custom alerting rules
- Extended monitoring capabilities
- Integration with external security tools

---

**Happy Monitoring!** 🛡️

For support or questions, please check the troubleshooting section or review the code comments for implementation details.