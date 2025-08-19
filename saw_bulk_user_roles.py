#!/usr/bin/env python3
"""
Arrow key navigation with visual [ ] and [*] selection
"""
import requests
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import sys
import os
import tty
import termios

console = Console()

class ArrowKeyVisualManager:
    def __init__(self):
        self.api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWdpb24iOiJ1c19lYXN0IiwianRpIjoiU2Z0enNlNldNOEJxIn0.D0R8UpCoAvEXwx8OhMpABbpkW3hbbm1PdJ3SWDUVyZQ"
        self.base_url = "https://api.probely.com"
        self.headers = {
            'Authorization': f'JWT {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.users = []
        self.roles = []
        self.selected_indices = set()
        self.current_user_index = 0
        
    def fetch_data(self):
        """Fetch users and roles from API"""
        try:
            # Fetch users
            response = requests.get(f"{self.base_url}/users/", headers=self.headers, timeout=30)
            response.raise_for_status()
            users_data = response.json()
            
            if isinstance(users_data, dict) and 'results' in users_data:
                self.users = users_data['results']
            else:
                self.users = users_data
                
            # Fetch roles
            roles_response = requests.get(f"{self.base_url}/roles/", headers=self.headers, timeout=30)
            roles_response.raise_for_status()
            roles_data = roles_response.json()
            
            if isinstance(roles_data, dict) and 'results' in roles_data:
                self.roles = roles_data['results']
            else:
                self.roles = roles_data
                
            return True
        except Exception as e:
            console.print(f"[red]❌ Error fetching data: {e}[/red]")
            return False
    
    def get_arrow_key(self):
        """Get arrow key input (cross-platform)"""
        if os.name == 'nt':  # Windows
            import msvcrt
            key = msvcrt.getch()
            if key == b'\xe0':  # Arrow key prefix on Windows
                key = msvcrt.getch()
                if key == b'H': return 'UP'
                elif key == b'P': return 'DOWN'
                elif key == b'K': return 'LEFT'
                elif key == b'M': return 'RIGHT'
            return key.decode('utf-8').lower()
        else:  # Unix/Linux/macOS
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                if ch == '\x1b':  # ESC sequence
                    next_ch = sys.stdin.read(1)
                    if next_ch == '[':
                        third_ch = sys.stdin.read(1)
                        if third_ch == 'A': return 'UP'
                        elif third_ch == 'B': return 'DOWN'
                        elif third_ch == 'C': return 'RIGHT'
                        elif third_ch == 'D': return 'LEFT'
                return ch.lower()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def display_users_table(self):
        """Display users table with current selection highlighted"""
        table = Table(title="👥 Select Users (Arrow keys to navigate, SPACE to toggle, ENTER to continue)")
        table.add_column("Select", style="cyan", no_wrap=True)
        table.add_column("Index", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Email", style="blue")
        table.add_column("Current Role", style="yellow")
        table.add_column("Billing Admin", style="red")
        table.add_column("Active", style="green")
        
        for i, user in enumerate(self.users):
            # Check if user is selected
            is_selected = i in self.selected_indices
            is_current = i == self.current_user_index
            
            # Selection indicator: [ ] for unselected, [*] for selected
            select_mark = "[*]" if is_selected else "[ ]"
            
            # Highlight current row
            if is_current:
                select_mark = f"[bold cyan]>{select_mark}[/bold cyan]"
            
            table.add_row(
                select_mark,
                str(i + 1),
                user.get('name', 'N/A')[:20] + "..." if len(user.get('name', '')) > 20 else user.get('name', 'N/A'),
                user.get('email', 'N/A')[:20] + "..." if len(user.get('email', '')) > 20 else user.get('email', 'N/A'),
                user['user_roles'][0]['role']['name'] if user.get('user_roles') else 'No role',
                "True" if user.get('billing_admin') else "False",
                "True" if user.get('active') else "False"
            )
        
        console.print(table)
        console.print(f"Total: {len(self.users)} users | Selected: {len(self.selected_indices)} users")
        
        # Show current selection
        if self.selected_indices:
            console.print(f"\n[green]✅ Currently Selected:[/green]")
            for idx in self.selected_indices:
                user = self.users[idx]
                console.print(f"   • {user.get('name', 'N/A')} ({user.get('email', 'N/A')})")
        
        console.print(f"\n[bold]Controls:[/bold] ↑↓ Arrow keys to navigate, SPACE to toggle, ENTER to continue, q to quit")
        console.print(f"[bold]Current:[/bold] Row {self.current_user_index + 1} (use SPACE to select)")
    
    def select_users_interactive(self):
        """Interactive user selection with arrow keys and SPACE"""
        console.print("\n[bold blue]🎯 User Selection[/bold blue]")
        console.print("Use ↑↓ arrow keys to navigate, SPACE to toggle selection, ENTER when done")
        console.print()
        
        while True:
            # Clear screen and display current state
            os.system('clear' if os.name != 'nt' else 'cls')
            self.display_users_table()
            
            # Get keypress
            key = self.get_arrow_key()
            
            if key == ' ':  # SPACE
                # Toggle selection of current user
                if self.current_user_index in self.selected_indices:
                    self.selected_indices.remove(self.current_user_index)
                else:
                    self.selected_indices.add(self.current_user_index)
                console.print(f"\n[green]✅ Toggled user {self.current_user_index + 1}[/green]")
                import time
                time.sleep(0.5)
            elif key == '\n' or key == '\r':  # ENTER
                if self.selected_indices:
                    console.print(f"\n[green]✅ Proceeding with {len(self.selected_indices)} selected users[/green]")
                    # Convert indices back to user objects
                    selected_users = [self.users[i] for i in self.selected_indices]
                    return selected_users
                else:
                    console.print("[yellow]⚠️  Please select at least one user first[/yellow]")
                    import time
                    time.sleep(2)
                    continue
            elif key == 'q':
                console.print("[red]❌ Cancelled[/red]")
                return None
            elif key == 'UP':
                if self.current_user_index > 0:
                    self.current_user_index -= 1
                console.print(f"[blue]📍 Moved to user {self.current_user_index + 1}[/blue]")
                import time
                time.sleep(0.3)
            elif key == 'DOWN':
                if self.current_user_index < len(self.users) - 1:
                    self.current_user_index += 1
                console.print(f"[blue]📍 Moved to user {self.current_user_index + 1}[/blue]")
                import time
                time.sleep(0.3)
            else:
                console.print(f"[yellow]Key pressed: {key}[/yellow]")
                import time
                time.sleep(0.3)
        
        return None
    
    def select_role(self):
        """Select target role"""
        console.print(f"\n[bold blue]🎭 Role Selection[/bold blue]")
        self.display_roles_table()
        
        while True:
            try:
                role_index = input(f"\nEnter role number (1-{len(self.roles)}): ")
                if role_index.lower() == 'q':
                    return None
                
                role_index = int(role_index) - 1
                if 0 <= role_index < len(self.roles):
                    return self.roles[role_index]
                else:
                    console.print(f"[red]❌ Invalid role number. Please enter 1-{len(self.roles)}[/red]")
            except ValueError:
                console.print("[red]❌ Please enter a valid number[/red]")
    
    def display_roles_table(self):
        """Display roles table"""
        table = Table(title="🎭 Available Roles")
        table.add_column("Index", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Description", style="blue")
        
        for i, role in enumerate(self.roles, 1):
            table.add_row(
                str(i),
                role.get('name', 'N/A'),
                role.get('description', 'No description')[:50] + "..." if len(role.get('description', '')) > 50 else role.get('description', 'No description')
            )
        
        console.print(table)
        console.print(f"Total: {len(self.roles)} roles")
    
    def preview_changes(self, selected_users, target_role):
        """Preview the changes that will be made"""
        console.print(f"\n[bold yellow]📋 Preview of Changes[/bold yellow]")
        
        preview_table = Table(title="Changes to be Applied")
        preview_table.add_column("User", style="green")
        preview_table.add_column("Current Role", style="red")
        preview_table.add_column("New Role", style="blue")
        
        for user in selected_users:
            current_role = "No role"
            if 'user_roles' in user and user['user_roles']:
                current_role = user['user_roles'][0].get('role', {}).get('name', 'No role')
            
            preview_table.add_row(
                user.get('name', 'N/A'),
                current_role,
                target_role.get('name', 'N/A')
            )
        
        console.print(preview_table)
        
        # Ask for confirmation
        confirm = input(f"\n🔄 Proceed with updating {len(selected_users)} users to role '{target_role.get('name')}'? (y/N): ")
        return confirm.lower() == 'y'
    
    def update_roles(self, selected_users, target_role):
        """Update the selected users' roles"""
        console.print(f"\n[blue]🔄 Sending update request for {len(selected_users)} users...[/blue]")
        
        # Prepare the update data
        update_data = []
        for user in selected_users:
            if 'user_roles' in user and user['user_roles']:
                current_user_role = user['user_roles'][0]
                user_role_id = current_user_role.get('id')
                if user_role_id:
                    update_data.append({
                        "id": user_role_id,
                        "user": {
                            "id": user.get('id'),
                            "email": user.get('email', ''),
                            "name": user.get('name', '')
                        },
                        "role": {
                            "id": target_role.get('id'),
                            "name": target_role.get('name'),
                            "description": target_role.get('description', ''),
                            "custom": target_role.get('custom', False)
                        },
                        "scope": {
                            "tier": "account"
                        }
                    })
        
        if update_data:
            try:
                response = requests.post(
                    f"{self.base_url}/user-roles/bulk/update/",
                    headers=self.headers,
                    json=update_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    console.print(f"[green]✅ Successfully updated {len(update_data)} user roles![/green]")
                    return True
                else:
                    console.print(f"[red]❌ Update failed with status {response.status_code}[/red]")
                    console.print(f"[red]Response: {response.text}[/red]")
                    return False
                    
            except Exception as e:
                console.print(f"[red]❌ Error during update: {e}[/red]")
                return False
        else:
            console.print("[yellow]⚠️  No valid user roles to update[/yellow]")
            return False
    
    def run(self):
        """Main application loop"""
        console.print(Panel.fit("🚀 Arrow Key Visual User Manager with [ ] and [*]", style="bold blue"))
        
        # Fetch data
        if not self.fetch_data():
            return
        
        # Select users interactively
        selected_users = self.select_users_interactive()
        if not selected_users:
            return
        
        # Select role
        target_role = self.select_role()
        if not target_role:
            return
        
        console.print(f"\n[green]✅ Selected role: {target_role.get('name')}[/green]")
        
        # Preview changes
        if not self.preview_changes(selected_users, target_role):
            console.print("[yellow]⚠️  Update cancelled[/yellow]")
            return
        
        # Update roles
        if self.update_roles(selected_users, target_role):
            console.print("\n[green]🎉 Role update completed successfully![/green]")
        else:
            console.print("\n[red]❌ Role update failed[/red]")

def main():
    manager = ArrowKeyVisualManager()
    manager.run()

if __name__ == "__main__":
    main()
