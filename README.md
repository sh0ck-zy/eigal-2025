# Printing Shop Digital Transformation

![NAU Industrial](https://via.placeholder.com/800x200/1E3A5F/FFFFFF?text=NAU+Industrial)

## Project Overview

This project aims to digitally transform the quotation and production processes of a traditional printing shop. The current business foundation is a complex Excel file maintained by a limited number of people, which centralizes all operational knowledge.

Our goal is to convert this system into an intelligent, reliable, and scalable digital platform that is more accessible to printing operators, customers, and decision-makers.

## 📊 Excel Analysis

The current Excel-based system consists of multiple interconnected sheets that handle different aspects of the printing quotation and production planning process:

### PLANIF. MIOLOS
- Contains drawings and planning for pagination
- Helps determine how many pages per printing sheet/plan
- Critical for optimizing material usage

### C. DE CAPAS
- Tables with measurements and variants for different cover types
- Contains specifications for various finishing options
- Used to calculate cover-related costs

### QT. PAPEL
- Calculates required paper sheets, expected waste, adjustments, and total weight
- Accounts for different paper types and weights
- Essential for material cost calculations

### QT. CAPAS
- Cost calculations by cover type and finishing options
- Factors in material costs, labor, and equipment usage
- Used for pricing cover-related components

### PANTONES
- Reference data for Pantone colors that react with lamination
- Important for quality control and avoiding production issues
- Flags combinations that may cause problems

### CALCULO COMPONENTES
- Calculations for extras like fabric, cardboard, ribbon, and spiral binding
- Used for specialized products with additional components
- Crucial for accurate quotations on complex products

### QUANTIDADES
- The main table for waste calculation based on print run and type
- Contains empirical data based on historical production
- Highlights special cases that require manual attention (yellow lines)
- **This is the primary focus of our MVP**

## 🔍 Problems Identified

| Category | Problem |
| --- | --- |
| Time | Slow quotation process requiring manual table consultation |
| Scalability | Difficulty serving more clients with the same team |
| Human error | Easy to make mistakes when consulting or copying data |
| Dependency | Knowledge bottleneck with few staff members |
| Zero automation | No customer self-service capabilities |
| Repetition | Manual re-entry of data for similar requests |

## 🎯 MVP Definition

### Objective
Create a system that automates the **waste calculation based on print run and type of printing**, eliminating the need to manually consult the QUANTIDADES table.

### MVP Features
- Web interface with form:
  - Print type selection (e.g., 4/0, 4/4, 2/2...)
  - Print run quantity input
- Output:
  - Expected waste (in sheets)
  - Expected adjustment
  - Warning if special case (yellow line)

### Technical Scope
- Convert the QUANTITIES table to SQLite database
- Create a Flask API for waste calculation
- Develop a simple frontend interface for data input and results display
- Implement special case detection and alerts

## 💻 Technical Approach

### Database Structure
```sql
CREATE TABLE quantities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    print_type TEXT NOT NULL,         -- e.g., "4/0", "4/4", "2/2"
    print_run INTEGER NOT NULL,       -- quantity to be printed
    waste_amount INTEGER NOT NULL,    -- expected waste in sheets
    adjustment INTEGER,               -- any adjustments needed
    is_special_case BOOLEAN DEFAULT 0 -- flag for cases requiring attention
);
```

### API Endpoints
- `GET /api/print-types` - Returns list of available print types
- `GET /api/waste-calculation?print_type={type}&print_run={quantity}` - Returns waste calculation
- Response format:
```json
{
  "print_type": "4/4",
  "print_run": 5000,
  "waste_amount": 120,
  "adjustment": 5,
  "is_special_case": false
}
```

### Frontend Design
- Simple, clean interface with two primary inputs:
  1. Print type dropdown (populated from API)
  2. Print run quantity input
- Results section showing:
  - Calculated waste amount
  - Any adjustments
  - Visual indicator for special cases
- Responsive design for use on desktop or mobile devices

## 📋 Development Process

### Week 1 (March 31 - April 7, 2024)
- Excel analysis and data extraction
- Database schema design and implementation
- Core API development
- Learning activities and environment setup

### Week 2 (April 7 - April 14, 2024)
- Frontend development
- Integration of components
- Testing and quality assurance
- Documentation and client presentation preparation

## 🚀 Future Expansion

After successful MVP implementation, the system can be expanded to include:
- Paper calculation module
- Cover cost calculations
- Visual planning tools
- Component estimation
- Quote generation
- Customer history management

## 🧪 Testing Strategy

### Input Test Cases
| Print Type | Print Run | Expected Waste | Special Case |
|------------|-----------|----------------|--------------|
| 4/0        | 1000      | [Value from Excel] | No |
| 4/4        | 5000      | [Value from Excel] | No |
| 2/2        | 500       | [Value from Excel] | Yes |
| [Additional test cases based on Excel data] |

### Integration Tests
- Form submission to API
- Data retrieval from database
- Special case detection
- Error handling (invalid inputs, missing data)

## 👥 Team

- João
- Diogo

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript with Bootstrap
- **Version Control**: Git (GitHub)
- **Documentation**: Markdown

---

*This documentation will be updated as the project progresses.*

## License

This project is proprietary and confidential to NAU Industrial.

© 2024 NAU Industrial. All rights reserved.