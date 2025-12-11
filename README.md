# Zygolysis — Python RPG Simulation Engine

**Zygolysis** is a modular, data-driven RPG/CYOA engine built in Python, designed as a backend simulation framework for complex character, item, and combat systems.

The engine uses a **SQLite relational database** for structured entity storage, **Tkinter/ttk GUI tools** for dynamic content creation, and extensive **OOP architecture** for clean, extensible game logic. Characters, items, and stats are defined through authoring tools that expand high-level inputs into detailed stat structures and serialize them directly to the database.

Combat is handled through a **derived-stat rules engine**, including **body-part-level HP pools**, standardized stat calculations, and equipment-based modifiers. The system is architected to integrate with a **Unity/C# front-end via sockets**, enabling real-time communication between Python logic and external 3D interfaces.

---

## 🚀 Technical Highlights

- **Python OOP architecture** for characters, items, combat rules, and simulation flow  
- **SQLite-backed data models** for scalable, structured, locacl and global entity storage  
- **Tkinter/ttk GUI editors** for characters and items with dynamic, type-dependent validation  
- **Data-driven stat framework:** core attributes → substats → derived combat + gameplay metrics  
- **Body-part combat model** enabling targeted damage, equipment interaction, and multivariable interactions over with a near unlimited number of characters an entities  
- **Modular backend design** engineered for front-end integration via sockets  
- **Clear separation of concerns** between content creation, persistence, and runtime execution  

---

## 🎯 Professional Applicability

This project demonstrates practical engineering skills relevant to research, software development, and computational modeling:

- Backend system architecture  
- Relational database modeling  
- GUI/UX development for internal tools  
- Scalable simulation design  
- Python for applied engineering and scientific workflows  
- Data-driven game engine architecture

---

## 🧩 Features

- Character creator GUI with:
  - Attribute inputs  
  - Personality traits  
  - Automatic expansion of base traits into usable interactable features

- Item creator GUI with:
  - Weapon/armor/accessory schemas  
  - Dynamic forms that change based on item type  
  - Validation through comboboxes and flag variables  

- Backend simulation engine:
  - Object generation from database entries  
  - HP systems for individual body regions  
  - Attack logic and stat-driven outcomes  

---

## 🔧 Planned Extensions

- Socket-based communication layer for Unity/C#  
- 3D skeleton frame integration for physical combat visualization  
- Additional item and ability
