#!/usr/bin/env python3
"""
Lost and Found Portal - Data Models
Team: Lohith, Prajwal, Manjegowda, Nithyashree, Manu
"""

import json
import os
from datetime import datetime
from typing import Optional, List


class Item:
    """Represents a lost or found item."""
    
    def __init__(self, item_id: int, title: str, description: str, 
                 category: str, location: str, contact_name: str,
                 contact_phone: str, item_type: str, image_path: str = "",
                 status: str = "active", posted_by: str = ""):
        self.item_id = item_id
        self.title = title
        self.description = description
        self.category = category
        self.location = location
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.item_type = item_type  # "lost" or "found"
        self.image_path = image_path
        self.status = status  # "active", "claimed", "resolved"
        self.posted_by = posted_by
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "location": self.location,
            "contact_name": self.contact_name,
            "contact_phone": self.contact_phone,
            "item_type": self.item_type,
            "image_path": self.image_path,
            "status": self.status,
            "posted_by": self.posted_by,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        item = cls(
            item_id=data["item_id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            location=data["location"],
            contact_name=data["contact_name"],
            contact_phone=data["contact_phone"],
            item_type=data["item_type"],
            image_path=data.get("image_path", ""),
            status=data.get("status", "active"),
            posted_by=data.get("posted_by", "")
        )
        item.created_at = data.get("created_at", datetime.now().isoformat())
        return item
    
    def __str__(self) -> str:
        img_status = " [IMG]" if self.image_path else ""
        return f"[{self.item_id}] [{self.item_type.upper()}] {self.title}{img_status} | Status: {self.status} | Location: {self.location}"


class User:
    """Represents a user of the portal."""
    
    def __init__(self, username: str, phone: str = "", email: str = ""):
        self.username = username
        self.phone = phone
        self.email = email
    
    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "phone": self.phone,
            "email": self.email
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            username=data["username"],
            phone=data.get("phone", ""),
            email=data.get("email", "")
        )


class Database:
    """Simple JSON-based storage for items and users."""
    
    DATA_DIR = "data"
    ITEMS_FILE = "data/items.json"
    USERS_FILE = "data/users.json"
    IMAGES_DIR = "data/images"
    
    def __init__(self):
        self._ensure_data_dir()
    
    def _ensure_data_dir(self) -> None:
        """Create data directories if they don't exist."""
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.IMAGES_DIR, exist_ok=True)
        # Initialize empty files if they don't exist
        for file_path in [self.ITEMS_FILE, self.USERS_FILE]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
    
    def save_items(self, items: List[Item]) -> None:
        """Save list of items to JSON."""
        with open(self.ITEMS_FILE, 'w') as f:
            json.dump([item.to_dict() for item in items], f, indent=2)
    
    def load_items(self) -> List[Item]:
        """Load all items from JSON."""
        try:
            with open(self.ITEMS_FILE, 'r') as f:
                data = json.load(f)
                return [Item.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_users(self, users: List[User]) -> None:
        """Save list of users to JSON."""
        with open(self.USERS_FILE, 'w') as f:
            json.dump([user.to_dict() for user in users], f, indent=2)
    
    def load_users(self) -> List[User]:
        """Load all users from JSON."""
        try:
            with open(self.USERS_FILE, 'r') as f:
                data = json.load(f)
                return [User.from_dict(user) for user in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def get_next_item_id(self) -> int:
        """Get next available item ID."""
        items = self.load_items()
        if not items:
            return 1
        return max(item.item_id for item in items) + 1
