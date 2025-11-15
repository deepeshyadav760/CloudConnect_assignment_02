"""
CloudConnect - Concrete Resource Implementations
"""
from base_resources import Resource


class AppService(Resource):
    """Web application hosting service"""
    
    def __init__(self, name, runtime, region, replica_count):
        config = {
            'runtime': runtime,
            'region': region,
            'replica_count': replica_count
        }
        super().__init__(name, config)
    
    def _format_creation_details(self):
        return (f"with {self.config['runtime']} runtime, "
                f"{self.config['replica_count']} replicas in {self.config['region']}")
    
    def _format_start_details(self):
        return f"in {self.config['region']}"
    
    def get_display_info(self):
        return (f"AppService: {self.name}\n"
                f"  Runtime: {self.config['runtime']}\n"
                f"  Region: {self.config['region']}\n"
                f"  Replicas: {self.config['replica_count']}\n"
                f"  State: {self.state.value}")
    
    @classmethod
    def get_type_name(cls):
        return "AppService"


class StorageAccount(Resource):
    """Cloud storage service"""
    
    def __init__(self, name, encryption_enabled, access_key, max_size_gb):
        config = {
            'encryption_enabled': encryption_enabled,
            'access_key': access_key,
            'max_size_gb': max_size_gb
        }
        super().__init__(name, config)
    
    def _format_creation_details(self):
        encryption = "with encryption" if self.config['encryption_enabled'] else "without encryption"
        return f"{encryption}, max size {self.config['max_size_gb']}GB"
    
    def _format_start_details(self):
        return f"with access key {self.config['access_key'][:8]}..."
    
    def get_display_info(self):
        return (f"StorageAccount: {self.name}\n"
                f"  Encryption: {'Enabled' if self.config['encryption_enabled'] else 'Disabled'}\n"
                f"  Access Key: {self.config['access_key'][:12]}...\n"
                f"  Max Size: {self.config['max_size_gb']}GB\n"
                f"  State: {self.state.value}")
    
    @classmethod
    def get_type_name(cls):
        return "StorageAccount"


class CacheDB(Resource):
    """In-memory caching database service"""
    
    def __init__(self, name, ttl_seconds, capacity_mb, eviction_policy):
        config = {
            'ttl_seconds': ttl_seconds,
            'capacity_mb': capacity_mb,
            'eviction_policy': eviction_policy
        }
        super().__init__(name, config)
    
    def _format_creation_details(self):
        return (f"with {self.config['eviction_policy']} eviction, "
                f"{self.config['capacity_mb']}MB capacity, "
                f"TTL {self.config['ttl_seconds']}s")
    
    def _format_start_details(self):
        return f"with {self.config['eviction_policy']} policy"
    
    def get_display_info(self):
        return (f"CacheDB: {self.name}\n"
                f"  TTL: {self.config['ttl_seconds']} seconds\n"
                f"  Capacity: {self.config['capacity_mb']}MB\n"
                f"  Eviction Policy: {self.config['eviction_policy']}\n"
                f"  State: {self.state.value}")
    
    @classmethod
    def get_type_name(cls):
        return "CacheDB"