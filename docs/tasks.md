# Tasks for NAU Industrial Printing Shop Digital Transformation MVP

## Domain Model & Database Schema Development

### 1. Excel Analysis and Mapping (Day 1)
- [x] Review all Excel sheets in detail, especially "QUANTIDADES"
- [ ] Document the relationships between different tables
- [ ] Identify all data types and validation rules
- [ ] Map special cases (yellow highlighted rows)
- [ ] Document business logic for waste calculation

### 2. Domain Model Design (Day 1-2)
- [ ] Create UML diagram of core entities
  - [ ] PrintType (4/0, 4/4, 2/2, etc.)
  - [ ] PrintRun (quantity ranges)
  - [ ] WasteCalculation (result object with waste, adjustment, special case flag)
  - [ ] Define relationships and multiplicity
- [ ] Review domain model with business stakeholders
- [ ] Document business rules and validations

### 3. Database Schema Design (Day 2)
- [ ] Design SQLite tables based on domain model
  - [ ] quantities (primary MVP table)
  - [ ] print_types (normalized reference table)
  - [ ] calculation_history (optional - store past calculations)
- [ ] Add appropriate indexes for query optimization
- [ ] Document schema with ERD diagram
- [ ] Define constraints and foreign keys

### 4. Data Migration Strategy (Day 3)
- [ ] Create Python script to extract data from Excel
  - [ ] Use pandas and openpyxl for extraction
  - [ ] Map Excel columns to database fields
  - [ ] Handle special cases and data cleansing
- [ ] Implement data transformation logic
- [ ] Create database initialization script
- [ ] Test data migration with subset of data
- [ ] Validate migrated data against original Excel

### 5. API Implementation (Day 3-4)
- [ ] Create Flask routes for required endpoints:
  - [ ] GET /api/print-types
  - [ ] GET /api/waste-calculation?print_type={type}&print_run={quantity}
- [ ] Implement data access layer to query SQLite database
- [ ] Add input validation
- [ ] Implement business logic for finding appropriate waste calculation
- [ ] Add error handling and appropriate status codes
- [ ] Document API with Swagger or similar (optional)

### 6. Integration & Testing (Day 4-5)
- [ ] Connect frontend to API endpoints
- [ ] Write unit tests for waste calculation logic
- [ ] Write API integration tests
- [ ] Perform manual testing with original Excel data
- [ ] Document test cases and results
- [ ] Fix bugs and edge cases

### 7. Deployment Preparation (Day 5)
- [ ] Update requirements.txt with all dependencies
- [ ] Verify database initialization scripts
- [ ] Ensure proper error handling and logging
- [ ] Create deployment instructions
- [ ] Prepare demo with sample data

## Advanced Tasks (Post-MVP)

### 8. Enhancements for Future Iterations
- [ ] Interpolation for missing print run values
- [ ] Suggestions for optimizing print runs
- [ ] User authentication for admin functions
- [ ] Data export functionality
- [ ] Reporting dashboard
- [ ] Integration with other Excel sheets (paper calculation, covers, etc.)

## Documentation Requirements

### 9. Technical Documentation
- [ ] Database schema documentation
- [ ] API documentation
- [ ] Code documentation (docstrings)
- [ ] Installation and setup guide
- [ ] Maintenance procedures

### 10. User Documentation
- [ ] User manual
- [ ] System overview
- [ ] FAQs
- [ ] Troubleshooting guide

---

## Development Environment Setup

### Required Tools
- Python 3.9+
- Git
- SQLite browser (for database inspection)
- VS Code or preferred IDE
- Excel (for reference data)

### Initial Setup
1. Clone repository
2. Run `start_app.bat` (Windows) or equivalent for your OS
3. Install requirements: `pip install -r requirements.txt`
4. Initialize database: `python init_db.py` (to be developed)

### Running the Application
1. Execute `python run.py`
2. Access application at http://localhost:5000/

---

**Note:** Prioritize Tasks 1-6 for MVP completion. Tasks 7-10 can be addressed in subsequent iterations.