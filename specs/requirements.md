**Technical Requirements** 

**Technology Stack** 

| Component  | Technology |
| :---- | :---- |
| Programming Language  | Python 3.11+ |
| Web Framework  | FastAPI |
| Database  | MongoDB (local instance) |
| ODM  | PyMongo |
| Containerization  | Docker & Docker Compose |
| Testing Framework  | pytest \+ pytest-cov |
| API Documentation  | OpenAPI 3.0 / Swagger UI |

**API Endpoints Required** 

Implement the following RESTful endpoints for the 'vehicles' collection: 

| Method  | Endpoint  | Description |
| :---- | :---- | :---- |
| GET  | /api/v1/vehicles  | List all vehicles (with pagination) |
| GET  | /api/v1/vehicles/{id}  | Get a single vehicle by ID |
| POST  | /api/v1/vehicles  | Create a new vehicle |
| PUT  | /api/v1/vehicles/{id}  | Update an existing vehicle |
| DELETE  | /api/v1/vehicles/{id}  | Delete a vehicle |
| GET  | /health  | Health check endpoint |

**Data Model: Vehicle Entity** 

The 'vehicles' collection must contain the following minimum attributes, designed for a Mexican  truck transportation company:  

| Field Name  | Data Type  | Description |
| :---- | :---- | :---- |
| \_id  | ObjectId  | MongoDB auto-generated unique identifier |
| placa  | String  | Mexican license plate (format validation  required) |
| numero\_economico  | String  | Internal fleet number (unique) |
| marca  | String  | Vehicle brand (e.g., Kenworth, Freightliner,  International) |
| modelo  | String  | Vehicle model |
| anno  | Integer  | Year of manufacture (1990-current year) |
| tipo\_vehiculo  | Enum  | Type: TRACTOR\_TRUCK, RIGID\_TRUCK,  TRAILER, DOLLY |
| capacidad\_carga\_kg  | Float  | Load capacity in kilograms |
| numero\_serie  | String  | VIN (Vehicle Identification Number) |
| estado\_vehiculo  | Enum  | Status: ACTIVE, IN\_MAINTENANCE,  OUT\_OF\_SERVICE |
| fecha\_alta  | DateTime  | Date vehicle was added to fleet |
| ultima\_verificacion  | DateTime  | Last inspection/verification date |
| poliza\_seguro  | String  | Insurance policy number |
| vigencia\_seguro  | Date  | Insurance expiration date |

**Optional Attributes** 

• kilometraje\_actual (Integer): Current odometer reading   
• tipo\_combustible (Enum): DIESEL, NATURAL\_GAS, ELECTRIC   
• rendimiento\_km\_litro (Float): Fuel efficiency   
• gps\_id (String): GPS tracker identifier   
• base\_operativa (String): Home base/terminal location 

**Required Project Structure** 

Your repository must follow this SDD-compliant structure: 

project-root/ ├── specs/ │ ├── constitution.md │ ├── spec.md │ ├──  plan.md │ ├── data-model.md │ ├── tasks.md │ └── contracts/ │ └──  openapi.yaml ├── src/ │ └── \[implementation code\] ├── tests/ │ └── \[test  files\] ├── docker-compose.yml ├── Dockerfile ├── README.md └── prompts-log.md 