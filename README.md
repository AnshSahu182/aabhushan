# API Reference

Endpoint: `/health`
- Method: GET
- Payload: none
- Response (200):
```json
{ "status": "ok", "app": "running", "database": "connected" }
```

Endpoint: `/api/rate`
- Method: POST
- Payload:
```json
{ "name": "gold", "price": 5500.0 }
```
- Response (200):
```json
{ "message": "gold price saved successfully" }
```
- Response (400):
```json
{ "error": "Missing required fields" }
```
or
```json
{ "error": "Invalid input. Price must be a number." }
```

Endpoint: `/api/rate`
- Method: GET
- Payload: none
- Response (200) example:
```json
[
  { "name": "gold", "price": 5500.0, "updated_at": "2026-02-16T12:00:00Z" }
]
```

Endpoint: `/api/calculate`
- Method: POST
- Payload:
```json
{
  "name": "Ring ABC",
  "gram": 10.5,
  "making_percent": 12.0,
  "metal": "<metal_object_id>"
}
```
- Response (200):
```json
{ "name": "Ring ABC", "price": 57750.0, "total_cost": 64780.0 }
```
- Response (400):
```json
{ "error": "Missing required fields" }
```
or
```json
{ "error": "Invalid input. Price, gram, and making_percent must be numbers." }
```

Endpoint: `/api/calculations`
- Method: GET
- Payload: none
- Response (200) example:
```json
[
  {
    "name": "Ring ABC",
    "price": 57750.0,
    "gram": 10.5,
    "making_percent": 12.0,
    "total_cost": 64780.0,
    "metal": "<ObjectId string>",
    "created_at": "2026-02-16T12:10:00Z"
  }
]
```
