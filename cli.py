"""
CloudConnect - Command Line Interface
"""
import random
import string
from registry import CloudConnectManager, ResourceRegistry
from base_resources import ResourceLogger


class CloudConnectCLI:
    """Command-line interface for CloudConnect"""
    
    def __init__(self):
        self.manager = CloudConnectManager()
        self.logger = ResourceLogger()
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("CloudConnect - Cloud Resource Manager")
        print("="*50)
        print("1. Create Resource")
        print("2. Start Resource")
        print("3. Stop Resource")
        print("4. Delete Resource")
        print("5. View Logs")
        print("6. List All Resources")
        print("7. Exit")
        print("="*50)
    
    def get_choice(self, prompt, options):
        """Get a validated choice from user"""
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= len(options):
                    return choice
                print(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def generate_access_key(self):
        """Generate a random access key"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    def create_resource(self):
        """Handle resource creation"""
        print("\nSelect resource type:")
        types = ResourceRegistry.get_all_types()
        for i, rtype in enumerate(types, 1):
            print(f"{i}. {rtype}")
        
        choice = self.get_choice("Choice: ", types)
        resource_type = types[choice - 1]
        
        name = input("Enter resource name: ").strip()
        if not name:
            print("Resource name cannot be empty!")
            return
        
        if resource_type == "AppService":
            self._create_app_service(name)
        elif resource_type == "StorageAccount":
            self._create_storage_account(name)
        elif resource_type == "CacheDB":
            self._create_cache_db(name)
    
    def _create_app_service(self, name):
        """Create an AppService resource"""
        print("\nSelect runtime:")
        runtimes = ["python", "nodejs", "dotnet"]
        for i, rt in enumerate(runtimes, 1):
            print(f"{i}. {rt}")
        runtime = runtimes[self.get_choice("Choice: ", runtimes) - 1]
        
        print("\nSelect region:")
        regions = ["EastUS", "WestEurope", "CentralIndia"]
        for i, reg in enumerate(regions, 1):
            print(f"{i}. {reg}")
        region = regions[self.get_choice("Choice: ", regions) - 1]
        
        print("\nSelect replica count:")
        replicas = [1, 2, 3]
        for i, rep in enumerate(replicas, 1):
            print(f"{i}. {rep}")
        replica_count = replicas[self.get_choice("Choice: ", replicas) - 1]
        
        success, message = self.manager.create_resource(
            "AppService", name, 
            runtime=runtime, 
            region=region, 
            replica_count=replica_count
        )
        print(f"\n{message}")
    
    def _create_storage_account(self, name):
        """Create a StorageAccount resource"""
        print("\nEnable encryption?")
        print("1. Yes")
        print("2. No")
        encryption_enabled = self.get_choice("Choice: ", ["Yes", "No"]) == 1
        
        # Auto-generate access key for better UX
        access_key = self.generate_access_key()
        print(f"\nGenerated access key: {access_key}")
        
        print("\nSelect maximum storage size:")
        sizes = [50, 100, 500, 1000]
        for i, size in enumerate(sizes, 1):
            print(f"{i}. {size}GB")
        max_size_gb = sizes[self.get_choice("Choice: ", sizes) - 1]
        
        success, message = self.manager.create_resource(
            "StorageAccount", name,
            encryption_enabled=encryption_enabled,
            access_key=access_key,
            max_size_gb=max_size_gb
        )
        print(f"\n{message}")
    
    def _create_cache_db(self, name):
        """Create a CacheDB resource"""
        print("\nSelect TTL (Time To Live):")
        ttls = [60, 300, 600, 3600]
        ttl_labels = ["60s (1 min)", "300s (5 min)", "600s (10 min)", "3600s (1 hour)"]
        for i, label in enumerate(ttl_labels, 1):
            print(f"{i}. {label}")
        ttl_seconds = ttls[self.get_choice("Choice: ", ttl_labels) - 1]
        
        print("\nSelect capacity:")
        capacities = [128, 256, 512, 1024]
        for i, cap in enumerate(capacities, 1):
            print(f"{i}. {cap}MB")
        capacity_mb = capacities[self.get_choice("Choice: ", capacities) - 1]
        
        print("\nSelect eviction policy:")
        policies = ["LRU", "FIFO", "LFU", "RANDOM"]
        for i, policy in enumerate(policies, 1):
            print(f"{i}. {policy}")
        eviction_policy = policies[self.get_choice("Choice: ", policies) - 1]
        
        success, message = self.manager.create_resource(
            "CacheDB", name,
            ttl_seconds=ttl_seconds,
            capacity_mb=capacity_mb,
            eviction_policy=eviction_policy
        )
        print(f"\n{message}")
    
    def start_resource(self):
        """Handle resource start"""
        name = input("\nEnter resource name: ").strip()
        success, message = self.manager.start_resource(name)
        print(f"\n{message}")
    
    def stop_resource(self):
        """Handle resource stop"""
        name = input("\nEnter resource name: ").strip()
        success, message = self.manager.stop_resource(name)
        print(f"\n{message}")
    
    def delete_resource(self):
        """Handle resource deletion"""
        name = input("\nEnter resource name: ").strip()
        success, message = self.manager.delete_resource(name)
        print(f"\n{message}")
    
    def view_logs(self):
        """Display recent logs"""
        print("\n" + "="*50)
        print("Recent Activity Logs")
        print("="*50)
        logs = self.logger.get_all_logs()
        if logs:
            for log in logs:
                print(log.strip())
        else:
            print("No logs available yet.")
        print("="*50)
    
    def list_resources(self):
        """List all resources"""
        resources = self.manager.list_resources()
        print("\n" + "="*50)
        print(f"All Resources ({len(resources)})")
        print("="*50)
        if resources:
            for resource in resources:
                print(resource.get_display_info())
                print("-" * 50)
        else:
            print("No resources created yet.")
        print("="*50)
    
    def run(self):
        """Main loop for CLI"""
        print("\nWelcome to CloudConnect!")
        
        while True:
            self.display_menu()
            try:
                choice = int(input("\nEnter choice: "))
                
                if choice == 1:
                    self.create_resource()
                elif choice == 2:
                    self.start_resource()
                elif choice == 3:
                    self.stop_resource()
                elif choice == 4:
                    self.delete_resource()
                elif choice == 5:
                    self.view_logs()
                elif choice == 6:
                    self.list_resources()
                elif choice == 7:
                    print("\nThank you for using CloudConnect!")
                    break
                else:
                    print("\nInvalid choice. Please try again.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\n\nExiting CloudConnect...")
                break


if __name__ == "__main__":
    cli = CloudConnectCLI()
    cli.run()