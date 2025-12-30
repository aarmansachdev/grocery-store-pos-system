 Grocery Store Point-of-Sale System

A comprehensive Point-of-Sale (POS) system built in Python featuring barcode validation, inventory management, membership tier processing, and coupon handling. This project demonstrates advanced object-oriented programming, data validation, and business logic implementation.

## Project Overview

This full-stack POS system simulates a complete grocery store checkout experience, from scanning barcodes to applying discounts and updating inventory. The system processes binary barcodes (UPC-A format), validates them through multiple security checks, manages product inventory, handles customer memberships with tiered benefits, and processes various coupon types.

## Key Features

###  Barcode Processing System
- **Binary to numeric conversion** for UPC-A barcodes (95-bit to 12-digit)
- **Multi-layer validation** including guard patterns, module parity, and checksum verification
- **Automatic error recovery** with barcode inversion for misread scans
- **Security modulo check** to ensure data integrity
- Support for **product, coupon, and membership barcodes**

### Inventory Management
- Real-time inventory tracking and updates
- Product database with pricing and stock information
- Automatic quantity decrementation on purchase
- Persistent storage with CSV file management
- Out-of-stock detection and validation

###  Membership Tier System
- **Four membership levels:** Member, Silver, Gold, Platinum
- **Tiered discount rates:** 0%, 1%, 5%, 10% respectively
- **Points multipliers:** 1x, 1.1x, 1.5x, 2x for loyalty rewards
- Automatic points accumulation on purchases
- Membership database with persistent storage

### Coupon System
- **Two coupon types:** Percentage-based and fixed-amount discounts
- Expiration date validation
- Minimum purchase requirements
- Automatic discount calculation and application
- Multiple coupon support with validation

### Shopping Cart & Checkout
- Dynamic cart management with item addition
- Subtotal and total calculation with all discounts applied
- Membership and coupon integration
- Order of operations for discount stacking
- Complete transaction processing

##  System Architecture

```
POS System
├── Barcode Processing Layer
│   └── BarcodeProcessor: Validates and converts barcodes
├── Data Management Layer
│   ├── ProductDatabase: Manages inventory
│   ├── MemberDatabase: Handles memberships
│   └── CouponDatabase: Stores coupons
├── Business Logic Layer
│   ├── Product: Product information and stock
│   ├── Member: Base and tiered memberships
│   ├── Coupon: Discount processing
│   └── ShoppingCart: Cart management
├── Backend Layer
│   └── StoreBackend: Coordinates databases
└── Frontend Layer
    └── POSSystem: Main checkout interface
```

## Technical Implementation

### Barcode Validation Algorithm

The system implements comprehensive UPC-A barcode validation:

1. **Length Validation:** Ensures 95-bit binary format
2. **Guard Pattern Check:** Validates LEFT (101), CENTER (01010), and RIGHT (101) guards
3. **Module Extraction:** Separates 6 left and 6 right modules (7 bits each)
4. **Parity Check:** 
   - Left modules: odd number of 1s, starts with 0, ends with 1
   - Right modules: even number of 1s, starts with 1, ends with 0
5. **Modulo-10 Checksum:**
   ```
   - Sum odd-position digits × 3
   - Add even-position digits
   - Check digit = (next multiple of 10) - sum
   ```

### Object-Oriented Design

**Inheritance Hierarchy:**
```python
Member (base)
├── SilverMember
├── GoldMember
└── PlatinumMember

Coupon (base)
├── PercentDiscountCoupon
└── FixedDiscountCoupon
```

**Key Design Patterns:**
- **Database Pattern:** Separate database classes for data persistence
- **Factory Pattern:** Barcode type identification and object creation
- **Strategy Pattern:** Different discount calculation strategies
- **Single Responsibility:** Each class handles one aspect of the system

### Data Flow

```
Binary Barcode (95 bits)
    ↓ [Validate]
Numeric Barcode (12 digits)
    ↓ [Identify Type]
Product/Coupon/Member Object
    ↓ [Add to Cart]
Shopping Cart
    ↓ [Calculate Total]
Final Price (with discounts)
    ↓ [Checkout]
Update Databases (inventory, memberships)
```

## 📁 File Structure

```
grocery-store-pos-system/
├── README.md
├── main.py                 # Main entry point and demonstration
├── pos.py                  # POS system orchestration
├── barcode.py             # Barcode validation and conversion
├── cart.py                # Shopping cart logic
├── product.py             # Product class
├── member.py              # Member classes with inheritance
├── coupon.py              # Coupon classes with inheritance
├── database.py            # Database management classes
└── store_backend.py       # Backend coordinator
```

## Key Technical Highlights

### 1. Barcode Security & Validation
- Multi-layer validation prevents invalid scans from entering the system
- Automatic barcode inversion handles upside-down scans
- Modulo-10 checksum ensures data integrity
- Binary to numeric conversion with error handling

### 2. Membership Tier System
```python
class Member:
    points_multiplier = 1
    discount_rate = 0

class PlatinumMember(Member):
    points_multiplier = 2      # 2x points earning
    discount_rate = 0.1        # 10% discount on purchases
```

### 3. Discount Stacking Logic
1. Calculate subtotal from items
2. Apply membership discount
3. Apply coupon discount (if applicable)
4. Return final total

### 4. Database Persistence
- CSV-based storage for products, members, and coupons
- Automatic file updates on transaction completion
- Separate "updated" files to preserve original data
- Error handling for missing or corrupted data

### 5. Error Recovery
- Barcode validation failures trigger automatic inversion retry
- Invalid barcodes are skipped without crashing the system
- Out-of-stock items are handled gracefully
- Expired coupons are automatically rejected

##  Skills Demonstrated

### Object-Oriented Programming
- Class inheritance and polymorphism
- Encapsulation with private attributes
- Method overriding for specialized behavior
- Abstract base classes for common interfaces

### Data Structures & Algorithms
- Dictionary-based lookups for O(1) barcode identification
- Binary string manipulation and validation
- Checksum algorithm implementation
- List comprehensions for efficient data processing

### File I/O & Data Persistence
- CSV file reading and writing
- Data serialization and deserialization
- State management across sessions
- File path handling and error management

### Software Engineering
- Modular design with separation of concerns
- DRY (Don't Repeat Yourself) principles
- Comprehensive error handling
- Code documentation with docstrings
- Unit testing with doctests

### Business Logic Implementation
- Complex discount calculation logic
- Multi-criteria validation systems
- Transaction processing workflows
- Inventory management algorithms

## 🚀 Usage Example

```python
from pos import POSSystem

# Initialize POS system
pos = POSSystem(
    'db-data/inventory.csv',
    'db-data/memberships.csv',
    'db-data/coupons.csv'
)

# Process scanned barcodes
pos.scan('cart-data/scan_1_binary.txt')

# View current cart
print(pos.get_current_cart())

# Complete checkout
total = pos.checkout()
print(f"Total: ${total:.2f}")
```

## 📊 Sample Transaction Flow

```
1. Scan binary barcode: 10100110010010011011110101010111010...
   → Validates ✓
   → Converts to: 012345678905
   → Identifies as: Product

2. Lookup product: Milk ($2.99)
   → Add to cart

3. Scan membership: 257274767454
   → Identifies as: Gold Member (5% discount)
   → Add to cart

4. Scan coupon: 149234073227
   → Validates expiration date
   → Checks minimum purchase requirement
   → Add 15% discount coupon

5. Calculate total:
   → Subtotal: $2.99
   → Gold discount (5%): -$0.15
   → Coupon (15%): -$0.43
   → Final total: $2.41

6. Checkout:
   → Update inventory (Milk: 150 → 149)
   → Add membership points (+10 points)
   → Save to database
```

##  Testing

The system includes comprehensive doctests for all components

## 💼 Business Value

This project demonstrates the ability to:
- Design and implement complex business systems
- Handle real-world data validation requirements
- Manage state and persistence in applications
- Apply object-oriented design principles effectively
- Build scalable, maintainable code architecture
- Implement security and error handling best practices

## 🎯 Learning Outcomes

Through this project, I gained expertise in:
- Barcode encoding/decoding algorithms
- Multi-tier system architecture design
- Database management and file I/O operations
- Complex discount and pricing logic
- Object-oriented inheritance and polymorphism
- Error handling and edge case management
- Test-driven development with doctests


## 📈 System Specifications

**Supported Barcode Types:**
- UPC-A (95-bit binary, 12-digit numeric)
- Product codes (starting with 0)
- Coupon codes (starting with 1)
- Membership IDs (starting with 2)

**Membership Tiers:**
| Tier | Discount | Points Multiplier |
|------|----------|------------------|
| Member | 0% | 1x |
| Silver | 1% | 1.1x |
| Gold | 5% | 1.5x |
| Platinum | 10% | 2x |

**Coupon Types:**
- Percentage Discount: X% off total
- Fixed Discount: $X off total
- Minimum purchase requirements supported
- Expiration date validation

## 👤 Author

Aarman Sachdev
- Data Science Major, Business Analytics Minor | UC San Diego

## 📝 Course Context

This project was completed as part of DSC 20 (Programming and Data Structures) at UC San Diego, demonstrating practical application of object-oriented programming concepts in a real-world business context.


**Note**: This is an educational project demonstrating software engineering principles. For production use, additional features like secure payment processing, real-time database systems, and regulatory compliance would be required.
