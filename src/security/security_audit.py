import os
import psutil
import re
import socket
import json

class SecurityAudit:
    def __init__(self):
        self.audit_results = {
            "password_strength": None,
            "open_ports": [],
            "file_permissions": {},
            "system_info": {}
        }

    def check_password_strength(self, password):
        """
        Check the strength of a password.

        Parameters:
        - password: The password to check.

        Returns:
        - A boolean indicating if the password is strong.
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def scan_open_ports(self):
        """
        Scan for open ports on the local machine.

        Returns:
        - A list of open ports.
        """
        open_ports = []
        for port in range(1, 65535):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('127.0.0.1', port)) == 0:
                    open_ports.append(port)
        return open_ports

    def check_file_permissions(self, file_paths):
        """
        Check the permissions of specified files.

        Parameters:
        - file_paths: A list of file paths to check.

        Returns:
        - A dictionary with file paths and their permissions.
        """
        permissions = {}
        for path in file_paths:
            if os.path.exists(path):
                permissions[path] = oct(os.stat(path).st_mode)[-3:]
            else:
                permissions[path] = "File does not exist"
        return permissions

    def gather_system_info(self):
        """
        Gather basic system information.

        Returns:
        - A dictionary with system information.
        """
        self.audit_results["system_info"] = {
            "CPU": psutil.cpu_percent(interval=1),
            "Memory": psutil.virtual_memory().percent,
            "Disk": psutil.disk_usage('/').percent,
            "Uptime": psutil.boot_time()
        }

    def run_audit(self, password, file_paths):
        """
        Run the security audit.

        Parameters:
        - password: The password to check for strength.
        - file_paths: A list of file paths to check permissions.
        """
        # Check password strength
        self.audit_results["password_strength"] = self.check_password_strength(password)

        # Scan for open ports
        self.audit_results["open_ports"] = self.scan_open_ports()

        # Check file permissions
        self.audit_results["file_permissions"] = self.check_file_permissions(file_paths)

        # Gather system information
        self.gather_system_info()

    def print_audit_results(self):
        """Print the audit results in a readable format."""
        print(json.dumps(self.audit_results, indent=4))

if __name__ == "__main__":
    # Example usage
    password_to_check = "StrongP@ssw0rd!"
    files_to_check = ["/etc/passwd", "/etc/shadow", "/var/log/syslog"]

    auditor = SecurityAudit()
    auditor.run_audit(password_to_check, files_to_check)
    auditor.print_audit_results()
