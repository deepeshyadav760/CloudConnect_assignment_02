"""
CloudConnect - Base Resource and Logger Classes
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import os


class ResourceState(Enum):
    """Enum representing the lifecycle states of a resource"""
    CREATED = "created"
    STARTED = "started"
    STOPPED = "stopped"
    DELETED = "deleted"


class ResourceLogger:
    """Handles logging for resource operations"""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
    
    def log(self, resource_type, resource_name, action, details=""):
        """Log a resource operation to both console and file"""
        timestamp = datetime.now().strftime("%I:%M %p")
        log_message = f"[{timestamp}] {resource_type} '{resource_name}' {action}"
        
        if details:
            log_message += f" {details}"
        
        # Console output
        print(log_message)
        
        # File output
        log_file = os.path.join(self.log_dir, f"{resource_type.lower()}.log")
        with open(log_file, 'a') as f:
            f.write(log_message + "\n")
        
        return log_message
    
    def get_all_logs(self):
        """Retrieve all logs from the log directory"""
        all_logs = []
        if not os.path.exists(self.log_dir):
            return all_logs
        
        for filename in os.listdir(self.log_dir):
            if filename.endswith('.log'):
                filepath = os.path.join(self.log_dir, filename)
                with open(filepath, 'r') as f:
                    all_logs.extend(f.readlines())
        
        return sorted(all_logs)[-20:]  # Return last 20 entries


class Resource(ABC):
    """Abstract base class for all cloud resources"""
    
    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.state = ResourceState.CREATED
        self.logger = ResourceLogger()
        self._log_action("created", self._format_creation_details())
    
    @abstractmethod
    def _format_creation_details(self):
        """Return formatted string of resource creation details"""
        pass
    
    @abstractmethod
    def get_display_info(self):
        """Return formatted string for display"""
        pass
    
    def start(self):
        """Start the resource"""
        if self.state == ResourceState.DELETED:
            return False, "Cannot start: Resource has been deleted"
        
        if self.state == ResourceState.STARTED:
            return False, "Resource is already running"
        
        self.state = ResourceState.STARTED
        details = self._format_start_details()
        self._log_action("started", details)
        return True, f"{self.__class__.__name__} started successfully"
    
    def stop(self):
        """Stop the resource"""
        if self.state == ResourceState.DELETED:
            return False, "Cannot stop: Resource has been deleted"
        
        if self.state != ResourceState.STARTED:
            return False, "Resource is not running"
        
        self.state = ResourceState.STOPPED
        self._log_action("stopped")
        return True, f"{self.__class__.__name__} stopped successfully"
    
    def delete(self):
        """Soft delete the resource"""
        if self.state == ResourceState.DELETED:
            return False, "Resource is already deleted"
        
        if self.state == ResourceState.STARTED:
            return False, "Cannot delete: Resource must be stopped first"
        
        self.state = ResourceState.DELETED
        self._log_action("marked as deleted")
        return True, f"{self.__class__.__name__} marked as deleted"
    
    def _log_action(self, action, details=""):
        """Internal method to log actions"""
        self.logger.log(self.__class__.__name__, self.name, action, details)
    
    @abstractmethod
    def _format_start_details(self):
        """Return formatted string for start operation"""
        pass
    
    @classmethod
    @abstractmethod
    def get_type_name(cls):
        """Return the display name of this resource type"""
        pass