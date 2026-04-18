# API Testing Documentation & Specifications

This documentation outlines the test cases, expected payloads (Swagger style), and current real-world outputs for the Kala platform API.

> [!WARNING]
> **Actual Output Constraints:** As the backend models and view functions are currently pending implementation, the "Actual Output" for most endpoints currently reflects the testing suite returning `404 Not Found` or `401 Unauthorized`. This documentation serves as the exact specification for when those endpoints are programmed.

---

## 1. Authentication Endpoints

### 1.1 Registered User (Buyer & Artist)
- **Method & Path:** `POST /v1/auth/register`
- **Description:** Registers a new user account. Distinct flows for Buyer and Artist.
#### Input (Swagger Format)
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "role": "buyer", // or "artist"
  "full_name": "Test User",
  "brand_name": "Test Brand" // Required if role=artist
}
```
#### Expected Output (201 Created)
```json
{
  "token": "eyJhbGciOi...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "role": "buyer"
  }
}
```
#### Actual Output
`404 NOT FOUND` - Endpoint logic pending.

---

### 1.2 User Login
- **Method & Path:** `POST /v1/auth/login`
- **Description:** Validates credentials and returns JWT bearer token.
#### Input (Swagger Format)
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
#### Expected Output (200 OK)
```json
{
  "token": "eyJhbGciOi...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "role": "buyer"
  }
}
```
#### Actual Output
`404 NOT FOUND` - Endpoint logic pending.

---

## 2. Artist Features

### 2.1 Retrieve Artist Profile
- **Method & Path:** `GET /v1/artist/profile`
- **Description:** Returns the authenticated artist's private profile.
#### Input
*Headers: `Authorization: Bearer <token>`*
#### Expected Output (200 OK)
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "full_name": "Artist Name",
  "brand_name": "Brand",
  "verification_status": "approved",
  "bio": "Description",
  "location": "City, Country"
}
```
#### Actual Output
`404 NOT FOUND`

### 2.2 Create Product
- **Method & Path:** `POST /v1/artist/products`
- **Description:** Creates a new product for the artist's catalogue.
#### Input (Swagger Format)
```json
{
  "title": "Handcrafted Vase",
  "description": "Ceramic vase.",
  "category": "Pottery",
  "price": 1200.00,
  "stock": 5,
  "materials": ["Clay"],
  "dimensions": {"width": 10, "height": 20, "unit": "cm"}
}
```
#### Expected Output (201 Created)
```json
{
  "id": "uuid",
  "title": "Handcrafted Vase",
  "price": 1200.00,
  "status": "draft",
  "images": []
}
```
#### Actual Output
`404 NOT FOUND`

### 2.3 Send Broadcast
- **Method & Path:** `POST /v1/artist/broadcasts`
- **Description:** Queues a multi-channel message to subscribers.
#### Input (Swagger Format)
```json
{
  "message": "New spring collection live!",
  "intent": "launch",
  "platforms": ["email", "instagram"]
}
```
#### Expected Output (201 Created)
```json
{
  "id": "uuid",
  "message": "New spring collection live!",
  "status": "queued",
  "sent_at": "2026-04-05T12:00:00Z"
}
```
#### Actual Output
`404 NOT FOUND`

---

## 3. Buyer Features

### 3.1 Discover Products 
- **Method & Path:** `GET /v1/products?q={query}`
- **Description:** Searches all active products.
#### Input
*Query Parameter: `q=pottery`*
#### Expected Output (200 OK)
```json
{
  "products": [
    {
      "id": "uuid",
      "title": "Handcrafted Vase",
      "price": 1200.00,
      "artist": {"brand_name": "Brand"}
    }
  ],
  "meta": {
    "total": 1,
    "limit": 20,
    "has_more": false
  }
}
```
#### Actual Output
`404 NOT FOUND`

### 3.2 Place Order (Checkout)
- **Method & Path:** `POST /v1/buyer/orders`
- **Description:** Converts current cart into a formal order.
#### Input (Swagger Format)
```json
{
  "shipping": {
    "address": {
      "full_name": "Home",
      "full_address": "123 Street",
      "city": "Mumbai",
      "state": "MH",
      "pin_code": "400001",
      "country": "India"
    }
  },
  "payment": {
    "method": "upi",
    "upi_id": "test@upi"
  }
}
```
#### Expected Output (201 Created)
```json
{
  "id": "uuid",
  "order_number": "ORD-12345",
  "status": "pending",
  "total": 1200.00,
  "tracking": [
    {"status": "pending", "timestamp": "2026-04-05T12:00:00Z"}
  ]
}
```
#### Actual Output
`404 NOT FOUND`

---

## 4. Admin Features

### 4.1 Admin Analytics Dashboard
- **Method & Path:** `GET /v1/admin/dashboard`
- **Description:** Fetches global system KPIs.
#### Input
*Headers: `Authorization: Bearer <token>`*
#### Expected Output (200 OK)
```json
{
  "kpis": {
    "total_revenue": 50000.00,
    "total_orders": 24,
    "registered_artists": 10,
    "registered_buyers": 150
  },
  "recent_orders": []
}
```
#### Actual Output
`404 NOT FOUND`

### 4.2 Verify Artist
- **Method & Path:** `POST /v1/admin/verification/{artist_id}/approve`
- **Description:** Approves a pending artist application.
#### Input
*Path Variable: `artist_id` (UUID)*
#### Expected Output (200 OK)
```json
{
  "id": "uuid",
  "verification_status": "approved",
  "is_suspended": false
}
```
#### Actual Output
`404 NOT FOUND`
