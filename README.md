# Lost and Found Portal

A Python-based Lost and Found Portal for campus.

## Team Members

| Name       | Role / Part                              |
|------------|------------------------------------------|
| **Lohith** | Project structure, models, storage, menu |
| Prajwal    | Post items, view all items               |
| Manjegowda | Image support, item details display      |
| Nithyashree| Search/filter, status updates            |
| Manu       | Contact owner, user login system         |

## How to Run

```bash
python main.py
```

## Project Structure

```
lost-and-found/
├── main.py          # Main application entry point
├── models.py        # Data models (Item, User, Database)
└── data/            # JSON storage (auto-created)
    ├── items.json   # Stores all lost/found items
    ├── users.json   # Stores user accounts
    └── images/      # Stores uploaded images
```

## Data Schema

### Item
- `item_id`: Unique identifier
- `title`: Item name
- `description`: Detailed description
- `category`: Item category (electronics, accessories, etc.)
- `location`: Where item was lost/found
- `contact_name`: Name of the poster
- `contact_phone`: Phone number
- `item_type`: "lost" or "found"
- `image_path`: Path to uploaded image (optional)
- `status`: "active", "claimed", or "resolved"
- `posted_by`: Username of the poster
- `created_at`: Timestamp

### User
- `username`: Unique username
- `phone`: Phone number
- `email`: Email address

## Features

- [x] Project setup and_Python project structure
- [x] Data models and JSON storage
- [x] Main menu system
- [ ] Post lost/found items (Prajwal)
- [ ] View all items (Prajwal)
- [ ] Image upload support (Manjegowda)
- [ ] Search and filter (Nithyashree)
- [ ] Status updates (Nithyashree)
- [ ] Contact owner (Manu)
- [ ] User login system (Manu)
