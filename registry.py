"""
CloudConnect - Resource Registry and Manager
"""
from resources import AppService, StorageAccount, CacheDB


class ResourceRegistry:
    """Registry for managing resource types - implements Factory pattern"""
    
    _registry = {}
    
    @classmethod
    def register(cls, resource_class):
        """Register a new resource type"""
        cls._registry[resource_class.get_type_name()] = resource_class
        return resource_class
    
    @classmethod
    def get_resource_class(cls, type_name):
        """Get a resource class by its type name"""
        return cls._registry.get(type_name)
    
    @classmethod
    def get_all_types(cls):
        """Get all registered resource types"""
        return list(cls._registry.keys())


# Auto-register all resource types
ResourceRegistry.register(AppService)
ResourceRegistry.register(StorageAccount)
ResourceRegistry.register(CacheDB)


class CloudConnectManager:
    """Main manager for CloudConnect resources"""
    
    def __init__(self):
        self.resources = {}
    
    def create_resource(self, resource_type, name, **kwargs):
        """Create a new resource"""
        if name in self.resources:
            return False, f"Resource '{name}' already exists"
        
        resource_class = ResourceRegistry.get_resource_class(resource_type)
        if not resource_class:
            return False, f"Unknown resource type: {resource_type}"
        
        try:
            resource = resource_class(name, **kwargs)
            self.resources[name] = resource
            return True, f"{resource_type} created successfully!"
        except Exception as e:
            return False, f"Error creating resource: {str(e)}"
    
    def get_resource(self, name):
        """Get a resource by name"""
        return self.resources.get(name)
    
    def start_resource(self, name):
        """Start a resource"""
        resource = self.get_resource(name)
        if not resource:
            return False, f"Resource '{name}' not found"
        
        return resource.start()
    
    def stop_resource(self, name):
        """Stop a resource"""
        resource = self.get_resource(name)
        if not resource:
            return False, f"Resource '{name}' not found"
        
        return resource.stop()
    
    def delete_resource(self, name):
        """Delete a resource"""
        resource = self.get_resource(name)
        if not resource:
            return False, f"Resource '{name}' not found"
        
        return resource.delete()
    
    def list_resources(self):
        """List all resources"""
        return list(self.resources.values())
    
    def get_resource_names(self):
        """Get list of all resource names"""
        return list(self.resources.keys())