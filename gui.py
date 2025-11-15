"""
CloudConnect - Graphical User Interface using Tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
from registry import CloudConnectManager, ResourceRegistry
from base_resources import ResourceLogger


class CloudConnectGUI:
    """Graphical User Interface for CloudConnect"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CloudConnect - Cloud Resource Manager")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        self.manager = CloudConnectManager()
        self.logger = ResourceLogger()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI components"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="☁️ CloudConnect Resource Manager",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Actions
        left_frame = tk.LabelFrame(
            main_frame,
            text="Actions",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Action buttons
        btn_style = {'font': ('Arial', 10), 'width': 20, 'pady': 8}
        
        tk.Button(
            left_frame,
            text="➕ Create Resource",
            command=self.show_create_dialog,
            bg='#27ae60',
            fg='white',
            **btn_style
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="▶️ Start Resource",
            command=self.start_resource,
            bg='#3498db',
            fg='white',
            **btn_style
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="⏹️ Stop Resource",
            command=self.stop_resource,
            bg='#e67e22',
            fg='white',
            **btn_style
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="🗑️ Delete Resource",
            command=self.delete_resource,
            bg='#e74c3c',
            fg='white',
            **btn_style
        ).pack(pady=5)
        
        tk.Button(
            left_frame,
            text="🔄 Refresh View",
            command=self.refresh_resources,
            bg='#95a5a6',
            fg='white',
            **btn_style
        ).pack(pady=5)
        
        # Right panel - Resources and Logs
        right_frame = tk.Frame(main_frame, bg='#f0f0f0')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Resources list
        resources_frame = tk.LabelFrame(
            right_frame,
            text="Resources",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        resources_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Treeview for resources
        tree_frame = tk.Frame(resources_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.resource_tree = ttk.Treeview(
            tree_frame,
            columns=('Name', 'Type', 'State', 'Config'),
            show='headings',
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            height=8
        )
        
        tree_scroll_y.config(command=self.resource_tree.yview)
        tree_scroll_x.config(command=self.resource_tree.xview)
        
        # Configure columns
        self.resource_tree.heading('Name', text='Resource Name')
        self.resource_tree.heading('Type', text='Type')
        self.resource_tree.heading('State', text='State')
        self.resource_tree.heading('Config', text='Configuration')
        
        self.resource_tree.column('Name', width=150)
        self.resource_tree.column('Type', width=120)
        self.resource_tree.column('State', width=80)
        self.resource_tree.column('Config', width=250)
        
        tree_scroll_y.pack(side='right', fill='y')
        tree_scroll_x.pack(side='bottom', fill='x')
        self.resource_tree.pack(side='left', fill='both', expand=True)
        
        # Logs section
        logs_frame = tk.LabelFrame(
            right_frame,
            text="Activity Logs",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        logs_frame.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            logs_frame,
            height=10,
            font=('Courier', 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap='word'
        )
        self.log_text.pack(fill='both', expand=True)
        
        # Refresh initial view
        self.refresh_resources()
        self.refresh_logs()
    
    def show_create_dialog(self):
        """Show resource creation dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Resource")
        dialog.geometry("500x600")
        dialog.configure(bg='#ecf0f1')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        tk.Label(
            dialog,
            text="Create New Resource",
            font=('Arial', 16, 'bold'),
            bg='#ecf0f1'
        ).pack(pady=20)
        
        # Resource name
        tk.Label(dialog, text="Resource Name:", bg='#ecf0f1', font=('Arial', 10)).pack()
        name_entry = tk.Entry(dialog, width=40, font=('Arial', 10))
        name_entry.pack(pady=5)
        
        # Resource type
        tk.Label(dialog, text="Resource Type:", bg='#ecf0f1', font=('Arial', 10)).pack(pady=(15, 5))
        resource_type_var = tk.StringVar()
        types = ResourceRegistry.get_all_types()
        resource_type_combo = ttk.Combobox(
            dialog,
            textvariable=resource_type_var,
            values=types,
            state='readonly',
            width=38,
            font=('Arial', 10)
        )
        resource_type_combo.pack()
        resource_type_combo.current(0)
        
        # Configuration frame
        config_frame = tk.Frame(dialog, bg='#ecf0f1')
        config_frame.pack(fill='both', expand=True, pady=20, padx=20)
        
        config_widgets = {}
        
        def update_config_options(*args):
            """Update configuration options based on selected resource type"""
            for widget in config_frame.winfo_children():
                widget.destroy()
            config_widgets.clear()
            
            rtype = resource_type_var.get()
            
            if rtype == "AppService":
                tk.Label(config_frame, text="Runtime:", bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
                runtime_var = tk.StringVar()
                runtime_combo = ttk.Combobox(
                    config_frame,
                    textvariable=runtime_var,
                    values=["python", "nodejs", "dotnet"],
                    state='readonly',
                    width=25
                )
                runtime_combo.grid(row=0, column=1, pady=5)
                runtime_combo.current(0)
                config_widgets['runtime'] = runtime_var
                
                tk.Label(config_frame, text="Region:", bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
                region_var = tk.StringVar()
                region_combo = ttk.Combobox(
                    config_frame,
                    textvariable=region_var,
                    values=["EastUS", "WestEurope", "CentralIndia"],
                    state='readonly',
                    width=25
                )
                region_combo.grid(row=1, column=1, pady=5)
                region_combo.current(0)
                config_widgets['region'] = region_var
                
                tk.Label(config_frame, text="Replica Count:", bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=5)
                replica_var = tk.IntVar(value=1)
                replica_spin = tk.Spinbox(config_frame, from_=1, to=3, textvariable=replica_var, width=27)
                replica_spin.grid(row=2, column=1, pady=5)
                config_widgets['replica_count'] = replica_var
            
            elif rtype == "StorageAccount":
                tk.Label(config_frame, text="Encryption:", bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
                encryption_var = tk.BooleanVar(value=True)
                tk.Checkbutton(
                    config_frame,
                    text="Enable Encryption",
                    variable=encryption_var,
                    bg='#ecf0f1'
                ).grid(row=0, column=1, sticky='w', pady=5)
                config_widgets['encryption_enabled'] = encryption_var
                
                tk.Label(config_frame, text="Max Size (GB):", bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
                size_var = tk.StringVar()
                size_combo = ttk.Combobox(
                    config_frame,
                    textvariable=size_var,
                    values=[50, 100, 500, 1000],
                    state='readonly',
                    width=25
                )
                size_combo.grid(row=1, column=1, pady=5)
                size_combo.current(1)
                config_widgets['max_size_gb'] = size_var
                
                # Auto-generate access key
                access_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                tk.Label(config_frame, text="Access Key:", bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=5)
                key_label = tk.Label(config_frame, text=access_key[:16] + "...", bg='#ecf0f1', font=('Courier', 9))
                key_label.grid(row=2, column=1, sticky='w', pady=5)
                config_widgets['access_key'] = access_key
            
            elif rtype == "CacheDB":
                tk.Label(config_frame, text="TTL (seconds):", bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
                ttl_var = tk.StringVar()
                ttl_combo = ttk.Combobox(
                    config_frame,
                    textvariable=ttl_var,
                    values=[60, 300, 600, 3600],
                    state='readonly',
                    width=25
                )
                ttl_combo.grid(row=0, column=1, pady=5)
                ttl_combo.current(1)
                config_widgets['ttl_seconds'] = ttl_var
                
                tk.Label(config_frame, text="Capacity (MB):", bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
                capacity_var = tk.StringVar()
                capacity_combo = ttk.Combobox(
                    config_frame,
                    textvariable=capacity_var,
                    values=[128, 256, 512, 1024],
                    state='readonly',
                    width=25
                )
                capacity_combo.grid(row=1, column=1, pady=5)
                capacity_combo.current(1)
                config_widgets['capacity_mb'] = capacity_var
                
                tk.Label(config_frame, text="Eviction Policy:", bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=5)
                policy_var = tk.StringVar()
                policy_combo = ttk.Combobox(
                    config_frame,
                    textvariable=policy_var,
                    values=["LRU", "FIFO", "LFU", "RANDOM"],
                    state='readonly',
                    width=25
                )
                policy_combo.grid(row=2, column=1, pady=5)
                policy_combo.current(0)
                config_widgets['eviction_policy'] = policy_var
        
        resource_type_var.trace('w', update_config_options)
        update_config_options()
        
        def create_resource():
            """Create the resource with provided configuration"""
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Resource name cannot be empty!")
                return
            
            rtype = resource_type_var.get()
            kwargs = {}
            
            for key, widget in config_widgets.items():
                if key == 'access_key':
                    kwargs[key] = widget  # Already a string
                elif isinstance(widget, tk.BooleanVar):
                    kwargs[key] = widget.get()
                elif isinstance(widget, tk.IntVar):
                    kwargs[key] = widget.get()
                else:
                    value = widget.get()
                    try:
                        kwargs[key] = int(value)
                    except ValueError:
                        kwargs[key] = value
            
            success, message = self.manager.create_resource(rtype, name, **kwargs)
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.refresh_resources()
                self.refresh_logs()
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#ecf0f1')
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Create",
            command=create_resource,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=12,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10),
            width=12,
            pady=5
        ).pack(side='left', padx=5)
    
    def get_selected_resource(self):
        """Get the currently selected resource name"""
        selection = self.resource_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a resource first!")
            return None
        
        item = self.resource_tree.item(selection[0])
        return item['values'][0]
    
    def start_resource(self):
        """Start the selected resource"""
        name = self.get_selected_resource()
        if not name:
            return
        
        success, message = self.manager.start_resource(name)
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
        
        self.refresh_resources()
        self.refresh_logs()
    
    def stop_resource(self):
        """Stop the selected resource"""
        name = self.get_selected_resource()
        if not name:
            return
        
        success, message = self.manager.stop_resource(name)
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
        
        self.refresh_resources()
        self.refresh_logs()
    
    def delete_resource(self):
        """Delete the selected resource"""
        name = self.get_selected_resource()
        if not name:
            return
        
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
            return
        
        success, message = self.manager.delete_resource(name)
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
        
        self.refresh_resources()
        self.refresh_logs()
    
    def refresh_resources(self):
        """Refresh the resource list"""
        # Clear existing items
        for item in self.resource_tree.get_children():
            self.resource_tree.delete(item)
        
        # Add resources
        resources = self.manager.list_resources()
        for resource in resources:
            config_str = ", ".join([f"{k}: {v}" for k, v in list(resource.config.items())[:2]])
            self.resource_tree.insert('', 'end', values=(
                resource.name,
                resource.__class__.__name__,
                resource.state.value,
                config_str
            ))
    
    def refresh_logs(self):
        """Refresh the log display"""
        self.log_text.delete('1.0', tk.END)
        logs = self.logger.get_all_logs()
        for log in logs:
            self.log_text.insert(tk.END, log)
        self.log_text.see(tk.END)


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = CloudConnectGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()