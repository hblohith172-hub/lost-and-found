#!/usr/bin/env python3
"""
Lost and Found Portal - Main Application
Team: Lohith, Prajwal, Manjegowda, Nithyashree, Manu
"""

import datetime
import os
import shutil
import sys
from models import Database, Item, User


CATEGORIES = [
    "Electronics",
    "Clothing",
    "Books & Stationery",
    "ID Cards & Documents",
    "Keys & Accessories",
    "Bags & Luggage",
    "Sports Equipment",
    "Money & Valuables",
    "Other",
]


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


def _validate_non_empty(prompt: str, field_name: str) -> str:
    """Prompt until a non-empty value is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"  [!] {field_name} cannot be empty. Please try again.\n")


def _select_category() -> str:
    """Display category menu and return the chosen category."""
    print("\n  Select a category:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")
    while True:
        try:
            choice = input("\n  Enter category number: ").strip()
            idx = int(choice)
            if 1 <= idx <= len(CATEGORIES):
                return CATEGORIES[idx - 1]
            else:
                print(f"  [!] Please enter a number between 1 and {len(CATEGORIES)}.")
        except ValueError:
            print("  [!] Invalid input. Please enter a number.")


def _validate_phone(prompt: str) -> str:
    """Prompt for a phone number (at least 7 digits)."""
    while True:
        value = input(prompt).strip()
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) >= 7:
            return value
        print("  [!] Please enter a valid phone number (at least 7 digits).\n")


def _display_items_table(items, title: str):
    """Display a list of items in a formatted table."""
    clear_screen()
    print_header(title)

    if not items:
        print("  No items found.\n")
        press_enter_to_continue()
        return

    print(f"  {'ID':<5} {'Type':<8} {'Title':<25} {'Category':<20} {'Location':<20} {'Status':<10} {'Contact':<20}")
    print("  " + "-" * 108)

    for item in items:
        item_id = str(item.item_id)
        item_type = item.item_type.upper()
        title_str = item.title[:24] if len(item.title) > 24 else item.title
        category = item.category[:19] if len(item.category) > 19 else item.category
        location = item.location[:19] if len(item.location) > 19 else item.location
        status = item.status[:9] if len(item.status) > 9 else item.status
        contact = item.contact_name[:19] if len(item.contact_name) > 19 else item.contact_name
        print(f"  {item_id:<5} {item_type:<8} {title_str:<25} {category:<20} {location:<20} {status:<10} {contact:<20}")

    print("  " + "-" * 108)
    print(f"  Total items: {len(items)}\n")
    press_enter_to_continue()


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
    
    def _handle_image_upload(self) -> str:
        """Handle image upload: copy image to data/images/ with validation.
        
        Returns:
            str: The path to the saved image, or empty string if no image uploaded.
        """
        print("\n--- Image Upload ---")
        image_path = input("Enter path to image file (or press Enter to skip): ").strip()
        
        if not image_path:
            return ""
        
        # Validate the file exists
        if not os.path.isfile(image_path):
            print("Error: File not found. Proceeding without image.")
            return ""
        
        # Validate file extension (allow common image formats)
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
        ext = os.path.splitext(image_path)[1].lower()
        if ext not in valid_extensions:
            print(f"Error: Invalid image format '{ext}'. Allowed formats: {', '.join(valid_extensions)}")
            return ""
        
        # Validate file size (max 10 MB)
        max_size = 10 * 1024 * 1024  # 10 MB
        file_size = os.path.getsize(image_path)
        if file_size > max_size:
            print(f"Error: File too large ({file_size / 1024 / 1024:.1f} MB). Max allowed: 10 MB.")
            return ""
        
        # Create images directory if it doesn't exist
        os.makedirs(self.db.IMAGES_DIR, exist_ok=True)
        
        # Generate unique filename using timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}{ext}"
        dest_path = os.path.join(self.db.IMAGES_DIR, filename)
        
        try:
            shutil.copy2(image_path, dest_path)
            print(f"Image uploaded successfully: {dest_path}")
            return dest_path
        except (shutil.Error, IOError) as e:
            print(f"Error copying image: {e}. Proceeding without image.")
            return ""
    
    def post_item(self, item_type: str):
        """
        Post a new lost or found item.
        
        Implements:
        - Input validation (non-empty fields, valid phone)
        - Category selection via numbered menu
        - Optional image upload with validation
        - Saves item to database and confirms
        """
        clear_screen()
        print_header(f"POST {item_type.upper()} ITEM")

        title = _validate_non_empty("  Title: ", "Title")
        description = _validate_non_empty("  Description: ", "Description")
        category = _select_category()
        location = _validate_non_empty("  Location (where it was lost/found): ", "Location")
        contact_name = _validate_non_empty("  Your Name: ", "Name")
        contact_phone = _validate_phone("  Phone Number: ")

        # Handle image upload
        image_path = self._handle_image_upload()

        items = self.db.load_items()
        new_id = self.db.get_next_item_id()

        item = Item(
            item_id=new_id,
            title=title,
            description=description,
            category=category,
            location=location,
            contact_name=contact_name,
            contact_phone=contact_phone,
            item_type=item_type,
            image_path=image_path,
            status="active",
            posted_by=self.current_user or contact_name,
        )

        items.append(item)
        self.db.save_items(items)

        print(f"\n  ✓ {item_type.capitalize()} item posted successfully! (ID: {new_id})")
        if image_path:
            print(f"  Image saved at: {image_path}")
        press_enter_to_continue()
    
    def view_all_items(self):
        """
        Display all items in a formatted table.
        
        Implements:
        - Loads all items from database
        - Displays in column-aligned table with headers
        - Shows item count
        """
        items = self.db.load_items()
        _display_items_table(items, "ALL ITEMS")
    
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
