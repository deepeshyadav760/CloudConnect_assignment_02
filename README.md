# CloudConnect - Cloud Resource Manager

A modular cloud resource management system that demonstrates Object-Oriented Programming principles and design patterns. CloudConnect allows developers to create, manage, and monitor cloud resources through both CLI and GUI interfaces.

## 🎯 Features

- **Multiple Resource Types**: Support for AppService, StorageAccount, and CacheDB
- **Complete Lifecycle Management**: Create → Start → Stop → Delete
- **Activity Logging**: Automatic logging to both console and file system
- **Extensible Architecture**: Easy addition of new resource types without modifying core logic
- **Dual Interface**: Both Command-Line Interface (CLI) and Graphical User Interface (GUI)
- **Soft Deletion**: Resources are marked as deleted but metadata is retained
- **State Validation**: Prevents invalid operations with clear error messages

## 🏗️ Architecture & Design Patterns

### 1. **Abstract Factory Pattern**
The `ResourceRegistry` class implements the Factory pattern, allowing dynamic creation of different resource types without hardcoding dependencies.

```python
# Resources self-register on initialization
ResourceRegistry.register(AppService)
ResourceRegistry.register(StorageAccount)
ResourceRegistry.register(CacheDB)
```

### 2. **Template Method Pattern**
The `Resource` base class defines the skeleton of resource operations while allowing subclasses to customize specific behaviors.

### 3. **Single Responsibility Principle (SRP)**
Each class has a single, well-defined responsibility:
- `Resource`: Base lifecycle management
- `ResourceLogger`: All logging operations
- `CloudConnectManager`: Resource collection management
- `ResourceRegistry`: Type registration and lookup

### 4. **Open/Closed Principle (OCP)**
The system is open for extension (adding new resource types) but closed for modification (no changes to core classes needed).

### 5. **Liskov Substitution Principle (LSP)**
All resource subclasses can be used interchangeably through the `Resource` base class interface.

## 📁 Project Structure

```
cloudconnect/
├── base_resources.py      # Abstract Resource class and ResourceLogger
├── resources.py           # Concrete resource implementations
├── registry.py            # ResourceRegistry and CloudConnectManager
├── cli.py                 # Command-line interface
├── gui.py                 # Tkinter-based GUI
├── logs/                  # Auto-generated log files
│   ├── appservice.log
│   ├── storageaccount.log
│   └── cachedb.log
└── README.md
```

## 🚀 Installation & Usage

### Prerequisites
- Python 3.7 or higher
- tkinter (usually comes with Python)

### Running the CLI Version

```bash
python cli.py
```

### Running the GUI Version

```bash
python gui.py
```

## 📝 Resource Types

### 1. AppService
Web application hosting service with configurable runtime environment.

**Configuration:**
- `runtime`: python, nodejs, or dotnet
- `region`: EastUS, WestEurope, or CentralIndia
- `replica_count`: 1, 2, or 3 instances

### 2. StorageAccount
Cloud storage service with encryption capabilities.

**Configuration:**
- `encryption_enabled`: Boolean flag for encryption
- `access_key`: Auto-generated 32-character key
- `max_size_gb`: 50, 100, 500, or 1000 GB

### 3. CacheDB
In-memory caching database with configurable eviction policies.

**Configuration:**
- `ttl_seconds`: Time-to-live (60, 300, 600, or 3600 seconds)
- `capacity_mb`: Memory capacity (128, 256, 512, or 1024 MB)
- `eviction_policy`: LRU, FIFO, LFU, or RANDOM

## 🔄 Resource Lifecycle

```
CREATED → STARTED → STOPPED → DELETED
```

**Valid Operations:**
- CREATE: Initial state, resource is configured but not running
- START: Can only start created or stopped resources
- STOP: Can only stop started resources
- DELETE: Can only delete stopped resources (soft delete)

**Invalid Operations:**
- Starting a deleted resource ❌
- Deleting a running resource ❌
- Stopping a resource that isn't running ❌

## 📊 UML Class Diagram

```
┌─────────────────────┐
│     Resource        │ (Abstract)
├─────────────────────┤
│ - name              │
│ - config            │
│ - state             │
│ - logger            │
├─────────────────────┤
│ + start()           │
│ + stop()            │
│ + delete()          │
│ + get_display_info()│
└──────────┬──────────┘
           │
    ┌──────┴──────┬──────────────┐
    │             │              │
┌───▼──────┐ ┌───▼──────┐ ┌────▼─────┐
│AppService│ │Storage   │ │ CacheDB  │
│          │ │Account   │ │          │
└──────────┘ └──────────┘ └──────────┘

┌──────────────────────┐
│ ResourceRegistry     │ (Singleton)
├──────────────────────┤
│ - _registry: dict    │
├──────────────────────┤
│ + register()         │
│ + get_resource_class()│
│ + get_all_types()    │
└──────────────────────┘

┌──────────────────────┐
│ CloudConnectManager  │
├──────────────────────┤
│ - resources: dict    │
├──────────────────────┤
│ + create_resource()  │
│ + start_resource()   │
│ + stop_resource()    │
│ + delete_resource()  │
│ + list_resources()   │
└──────────────────────┘

┌──────────────────────┐
│ ResourceLogger       │
├──────────────────────┤
│ - log_dir: str       │
├──────────────────────┤
│ + log()              │
│ + get_all_logs()     │
└──────────────────────┘
```

## 🎨 Design Decisions

### 1. **Soft Deletion**
Resources are not removed from the system upon deletion. Instead, they're marked as DELETED and their metadata is retained for audit purposes. This allows tracking of all resources ever created.

### 2. **Auto-Generated Access Keys**
For StorageAccount resources, access keys are automatically generated to improve user experience and ensure key strength.

### 3. **Structured Configuration Options**
Rather than free-form input, users select from predefined options. This reduces errors and ensures valid configurations.

### 4. **Separate Logging per Resource Type**
Each resource type writes to its own log file (e.g., `appservice.log`), making it easier to track specific resource types.

### 5. **State-Based Operation Validation**
All lifecycle operations check the current state before proceeding, providing clear error messages for invalid operations.

## 🔧 Extending CloudConnect

Adding a new resource type is straightforward:

```python
# 1. Create a new resource class
class Database(Resource):
    def __init__(self, name, db_type, storage_gb):
        config = {'db_type': db_type, 'storage_gb': storage_gb}
        super().__init__(name, config)
    
    def _format_creation_details(self):
        return f"with {self.config['db_type']}, {self.config['storage_gb']}GB"
    
    def _format_start_details(self):
        return f"database engine started"
    
    def get_display_info(self):
        return f"Database: {self.name}\n  Type: {self.config['db_type']}\n  State: {self.state.value}"
    
    @classmethod
    def get_type_name(cls):
        return "Database"

# 2. Register the new resource type
ResourceRegistry.register(Database)
```

That's it! No changes to existing code required.

## 📈 Example Usage

### CLI Example
```
CloudConnect - Cloud Resource Manager
1. Create Resource
2. Start Resource
3. Stop Resource
4. Delete Resource
5. View Logs
6. List All Resources
7. Exit

Enter choice: 1
Select resource type:
1. AppService
2. StorageAccount
3. CacheDB
Choice: 1

Enter resource name: my-web-app
Select runtime:
1. python
2. nodejs
3. dotnet
Choice: 1

Select region:
1. EastUS
2. WestEurope
3. CentralIndia
Choice: 2

Select replica count:
1. 1
2. 2
3. 3
Choice: 2

AppService created successfully!
```

## 🧪 Testing Scenarios

1. **Happy Path**: Create → Start → Stop → Delete
2. **Invalid Start**: Try starting a deleted resource
3. **Invalid Delete**: Try deleting a running resource
4. **Duplicate Names**: Try creating resources with duplicate names
5. **Log Verification**: Verify all operations are logged correctly

## 🎓 Learning Outcomes

This project demonstrates:
- Object-Oriented Programming (OOP) principles
- SOLID design principles
- Design patterns (Factory, Template Method, Registry)
- State management
- Input validation
- Logging and monitoring
- GUI development with Tkinter
- Extensible architecture design

## 📝 Assumptions

1. Resource names must be unique across all types
2. Only one resource can be managed at a time through the interfaces
3. Log files are stored locally in the `logs/` directory
4. No authentication or authorization is implemented
5. Resources don't consume actual cloud resources (simulation only)
6. The system runs as a single-user application

## 🤝 Contributing

To add new features or resource types:
1. Extend the `Resource` abstract class
2. Implement all required abstract methods
3. Register your new resource type
4. Update the CLI/GUI to support creation of the new type

## 📄 License

This project is created for educational purposes.

---

**Author:** [Your Name]  
**Course:** Cloud Computing / Software Engineering  
**Date:** November 2025