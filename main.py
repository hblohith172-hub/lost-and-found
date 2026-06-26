#!/usr/bin/env python3
"""
Lost and Found Portal - Main Application
Team: Lohith, Prajwal, Manjegowda, Nithyashree, Manu
"""

import os
import shutil
import sys
from models import Database, Item, User


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50 + "\n")


def press_enter_to_continue():
    """Wait for user to press Enter."""
    input("\nPress Enter to continue...")


class LostAndFoundApp:
    """Main application class for the Lost and Found Portal."""
    
    def __init__(self):
        self.db = Database()
        self.current_user = None
    
    def display_menu(self):
        """Display the main menu."""
        clear_screen()
        user_display = f" | Logged in as: {self.current_user}" if self.current_user else " | Not logged in"
        print(f"\n{'=' * 50}")
        print(f"  LOST AND FOUND PORTAL{user_display}")
        print("=" * 50)
        print("\n  1. Post a Lost Item")
        print("  2. Post a Found Item")
        print("  3. View All Items")
        print("  4. Search Items")
        print("  5. Update Item Status")
        print("  6. Contact Owner")
        print("  7. Login / Register")
        print("  0. Exit")
        print("\n" + "-" * 50)
    
    def run(self):
        """Main application loop."""
        while True:
            self.display_menu()
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self.post_item("lost")
            elif choice == "2":
                self.post_item("found")
            elif choice == "3":
                self.view_all_items()
            elif choice == "4":
                self.search_items()
            elif choice == "5":
                self.update_status()
            elif choice == "6":
                self.contact_owner()
            elif choice == "7":
                self.login_menu()
            elif choice == "0":
                print("\nThank you for using Lost and Found Portal!")
                break
            else:
                print("\nInvalid option. Please try again.")
                press_enter_to_continue()
    
    def post_item(self, item_type: str):
        """Post a new lost or found item."""
        # TODO: Implement by Prajwal
        clear_screen()
        print_header(f"POST {item_type.upper()} ITEM")
        print("Feature coming soon - implemented by Prajwal")
        press_enter_to_continue()
    
    def view_all_items(self):
        """Display all items."""
        # TODO: Implement by Prajwal
        clear_screen()
        print_header("ALL ITEMS")
        print("Feature coming soon - implemented by Prajwal")
        press_enter_to_continue()
    
    def search_items(self):
        """Search and filter items."""
        # TODO: Implement by Nithyashree
        clear_screen()
        print_header("SEARCH ITEMS")
        print("Feature coming soon - implemented by Nithyashree")
        press_enter_to_continue()
    
    def update_status(self):
        """Update item status."""
        # TODO: Implement by Nithyashree
        clear_screen()
        print_header("UPDATE ITEM STATUS")
        print("Feature coming soon - implemented by Nithyashree")
        press_enter_to_continue()
    
    def contact_owner(self):
        """Contact the owner of an item."""
        # TODO: Implement by Manu
        clear_screen()
        print_header("CONTACT OWNER")
        print("Feature coming soon - implemented by Manu")
        press_enter_to_continue()
    
    def login_menu(self):
        """User login/register menu."""
        # TODO: Implement by Manu
        clear_screen()
        print_header("LOGIN / REGISTER")
        print("Feature coming soon - implemented by Manu")
        press_enter_to_continue()


def main():
    """Entry point for the application."""
    app = LostAndFoundApp()
    app.run()


if __name__ == "__main__":
    main()
