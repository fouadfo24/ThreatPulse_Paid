from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import psutil
import threading
import time
import json
import os
import socket
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'edr_dashboard_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for monitoring
alerts = []
file_events = []
network_connections = []
suspicious_processes = []

# Known suspicious process names and patterns
SUSPICIOUS_PROCESSES = [
    'nc', 'netcat', 'ncat', 'socat', 'telnet', 'wget', 'curl',
    'powershell', 'cmd', 'bash', 'sh', 'python', 'perl', 'ruby'
]

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        
    def on_modified(self, event):
        if not event.is_directory:
            self.log_file_event('modified', event.src_path)
    
    def on_created(self, event):
        if not event.is_directory:
            self.log_file_event('created', event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.log_file_event('deleted', event.src_path)
    
    def log_file_event(self, action, path):
        global file_events
        event_data = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'path': path,
            'size': self.get_file_size(path) if action != 'deleted' else 0
        }
        file_events.append(event_data)
        
        # Keep only last 100 events
        if len(file_events) > 100:
            file_events.pop(0)
        
        # Check for suspicious file activities
        self.check_suspicious_file_activity(event_data)
    
    def get_file_size(self, path):
        try:
            return os.path.getsize(path)
        except:
            return 0
    
    def check_suspicious_file_activity(self, event_data):
        global alerts
        suspicious_paths = ['/etc/passwd', '/etc/shadow', '/etc/hosts', '/tmp']
        suspicious_extensions = ['.exe', '.bat', '.ps1', '.sh', '.py']
        
        path = event_data['path']
        
        # Check for modifications to sensitive files
        if any(sus_path in path for sus_path in suspicious_paths):
            alert = {
                'timestamp': datetime.now().isoformat(),
                'type': 'File Activity',
                'severity': 'High',
                'message': f'Suspicious file activity: {event_data["action"]} {path}',
                'details': event_data
            }
            alerts.append(alert)
        
        # Check for executable files
        if any(path.endswith(ext) for ext in suspicious_extensions):
            alert = {
                'timestamp': datetime.now().isoformat(),
                'type': 'File Activity',
                'severity': 'Medium',
                'message': f'Executable file {event_data["action"]}: {path}',
                'details': event_data
            }
            alerts.append(alert)

def get_system_info():
    """Get current system information"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu': cpu_percent,
            'memory': {
                'used': memory.used,
                'total': memory.total,
                'percent': memory.percent
            },
            'disk': {
                'used': disk.used,
                'total': disk.total,
                'percent': (disk.used / disk.total) * 100
            },
            'boot_time': psutil.boot_time()
        }
    except Exception as e:
        return {'error': str(e)}

def get_running_processes():
    """Get list of running processes"""
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'cmdline']):
            try:
                proc_info = proc.info
                processes.append({
                    'pid': proc_info['pid'],
                    'name': proc_info['name'],
                    'username': proc_info['username'],
                    'cpu_percent': proc_info['cpu_percent'],
                    'memory_percent': proc_info['memory_percent'],
                    'cmdline': ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else ''
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        return {'error': str(e)}
    
    return processes

def get_network_connections():
    """Get network connections"""
    connections = []
    try:
        for conn in psutil.net_connections():
            if conn.status == 'ESTABLISHED':
                connections.append({
                    'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else '',
                    'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else '',
                    'status': conn.status,
                    'pid': conn.pid
                })
    except Exception as e:
        return {'error': str(e)}
    
    return connections

def monitor_processes():
    """Monitor for suspicious processes"""
    global suspicious_processes, alerts
    
    while True:
        try:
            current_processes = get_running_processes()
            if isinstance(current_processes, list):
                for proc in current_processes:
                    if any(sus_name in proc['name'].lower() for sus_name in SUSPICIOUS_PROCESSES):
                        sus_proc = {
                            'timestamp': datetime.now().isoformat(),
                            'pid': proc['pid'],
                            'name': proc['name'],
                            'username': proc['username'],
                            'cmdline': proc['cmdline']
                        }
                        
                        # Check if this process is already in our suspicious list
                        if not any(sp['pid'] == proc['pid'] for sp in suspicious_processes):
                            suspicious_processes.append(sus_proc)
                            
                            # Create alert
                            alert = {
                                'timestamp': datetime.now().isoformat(),
                                'type': 'Process',
                                'severity': 'Medium',
                                'message': f'Suspicious process detected: {proc["name"]} (PID: {proc["pid"]})',
                                'details': sus_proc
                            }
                            alerts.append(alert)
        
        except Exception as e:
            print(f"Error monitoring processes: {e}")
        
        time.sleep(5)  # Check every 5 seconds

def monitor_network():
    """Monitor network connections"""
    global network_connections
    
    while True:
        try:
            connections = get_network_connections()
            if isinstance(connections, list):
                network_connections = connections
        except Exception as e:
            print(f"Error monitoring network: {e}")
        
        time.sleep(10)  # Check every 10 seconds

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/system')
def api_system():
    return jsonify(get_system_info())

@app.route('/api/processes')
def api_processes():
    return jsonify(get_running_processes())

@app.route('/api/network')
def api_network():
    return jsonify(get_network_connections())

@app.route('/api/alerts')
def api_alerts():
    global alerts
    # Keep only last 50 alerts
    if len(alerts) > 50:
        alerts = alerts[-50:]
    return jsonify(alerts)

@app.route('/api/file-events')
def api_file_events():
    return jsonify(file_events)

@app.route('/api/suspicious-processes')
def api_suspicious_processes():
    return jsonify(suspicious_processes)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'msg': 'Connected to EDR Dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def start_monitoring():
    """Start all monitoring threads"""
    # Start process monitoring
    process_thread = threading.Thread(target=monitor_processes, daemon=True)
    process_thread.start()
    
    # Start network monitoring
    network_thread = threading.Thread(target=monitor_network, daemon=True)
    network_thread.start()
    
    # Start file system monitoring
    event_handler = FileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/tmp', recursive=True)  # Monitor /tmp directory
    observer.start()
    
    print("EDR monitoring started...")

if __name__ == '__main__':
    start_monitoring()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)