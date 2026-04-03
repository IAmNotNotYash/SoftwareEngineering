# Kala Platform — Database Schema Documentation

## Overview

Kala is an artisan marketplace connecting independent artists (sellers) with buyers. The platform supports three personas — **Artist**, **Buyer**, and **Admin** — each with distinct data needs. This document describes every table in the database schema, its purpose, the frontend functionality it supports, its column-level details, and how it interacts with other tables.

The schema is designed around the following core domains:

- **Identity & Authentication** — Users, Artist Profiles, Buyer Profiles
- **Commerce** — Products, Product Images, Cart, Orders, Order Items, Order Tracking
- **Catalogues** — Catalogues, Catalogue Products, Catalogue Stats, Catalogue Views, Catalogue Likes
- **Social & Discovery** — Follows, Posts, Reviews
- **Communication** — Broadcasts
- **Analytics** — Artist Revenue Trend, Platform Revenue Trend, Analytics Snapshots

------
## 1. USERS

### Purpose

`USERS` is the central identity table for the entire platform. Every person who interacts with the system — whether a buyer browsing products, an artist selling crafts, or an admin managing the platform — has exactly one row in this table. It stores only authentication-critical fields; all persona-specific data lives in separate profile tables (`ARTIST_PROFILES`, `BUYER_PROFILES`) linked by `user_id`.

### Frontend Functionality Served

- **Login page** (`/auth/login`) — email/password authentication
- **Register page** (`/auth/register`) — account creation with role selection (buyer or artist)
- **Admin: Artists page** (`/admin/artists`) — suspension toggle (`is_suspended`)
- **Admin: Buyers page** (`/admin/buyers`) — suspension toggle
- **All authenticated routes** — JWT or session token is tied to the user's `id` and `role`

### Columns

| Column          | Type         | Constraints      | Description                                                  |
| --------------- | ------------ | ---------------- | ------------------------------------------------------------ |
| `id`            | UUID         | PK               | Universally unique identifier for the user. Used as the foreign key target across the entire schema. |
| `email`         | VARCHAR(255) | UNIQUE, NOT NULL | The user's login email. Must be unique across all roles. Indexed for fast lookup during authentication. |
| `password_hash` | VARCHAR(255) | NOT NULL         | Bcrypt or Argon2 hash of the user's password. Never stored in plaintext. |
| `role`          | ENUM         | NOT NULL         | One of `buyer`, `artist`, or `admin`. Controls which views and API routes the user can access. |
| `is_suspended`  | BOOLEAN      | DEFAULT false    | Set to `true` by an admin to revoke platform access without deleting the account. Suspended users cannot log in. |
| `created_at`    | TIMESTAMP    | NOT NULL         | Account creation timestamp. Used for "Joined" displays and cohort analytics. |
| `updated_at`    | TIMESTAMP    | NOT NULL         | Last modification timestamp. Automatically updated on any row change. |

### Relationships

- **One-to-one** with `ARTIST_PROFILES` via `artist_profiles.user_id`
- **One-to-one** with `BUYER_PROFILES` via `buyer_profiles.user_id`
- **One-to-many** with `ADDRESSES` — a user can have multiple saved addresses
- **One-to-many** with `PAYMENT_METHODS` — a user can have multiple saved payment methods
- **Referenced by** `ARTIST_PROFILES.verified_by` — the admin user who approved/rejected an artist

### Design Notes

The `role` field is intentionally stored here rather than derived from the presence of a profile row. This makes authorization middleware simple: a single query to `USERS` reveals whether the request is from a buyer, artist, or admin without needing joins. A user can only have one role; an artist cannot also be a buyer on the same account.

------

## 2. ARTIST_PROFILES

### Purpose

Stores all public-facing and platform-operational data for users with the `artist` role. This includes their brand identity (name, bio, images), their verification status with the admin, and denormalised follower counts for fast display. An artist profile is created at registration but remains in `pending` verification status until an admin reviews and approves it.

### Frontend Functionality Served

- **Artist Dashboard** (`/artist/dashboard`) — brand name displayed in header
- **Buyer: Artist Page** (`/buyer/artist/:id`) — full profile: name, location, bio, cover image, profile image, follower count, follow button
- **Buyer: Dashboard** (`/buyer/dashboard`) — "Discover Creators" cards (name, category/location, avatar, followers)
- **Admin: Verification Queue** (`/admin/verification`) — name, email, join date, status management
- **Admin: Artists Table** (`/admin/artists`) — brand name, verified status, suspended status
- **Navbar** (`ArtistNavbar.vue`) — brand name in logo area
- **Product/Catalogue attribution** — `brand_name` shown on all product and catalogue cards

### Columns

| Column                | Type         | Constraints                 | Description                                                  |
| --------------------- | ------------ | --------------------------- | ------------------------------------------------------------ |
| `id`                  | UUID         | PK                          | Profile identifier. Distinct from `user_id` to allow profile data to be queried independently. |
| `user_id`             | UUID         | FK → USERS.id, UNIQUE       | Links to the authentication record. UNIQUE enforces one profile per user. |
| `brand_name`          | VARCHAR(150) | NOT NULL                    | The artist's public brand name (e.g., "Luna Ceramics"). Displayed everywhere products and catalogues appear. |
| `full_name`           | VARCHAR(150) | NOT NULL                    | The artist's legal/personal name. Used in admin tables and verification documents. |
| `location`            | VARCHAR(150) | NULLABLE                    | City and region (e.g., "Jaipur, Rajasthan"). Displayed on the artist's public profile page. |
| `bio`                 | TEXT         | NULLABLE                    | Long-form description of the artist's practice, process, and background. Displayed on the buyer-facing artist profile page. |
| `profile_image_url`   | VARCHAR(500) | NULLABLE                    | URL of the artist's avatar/headshot. Shown in navbar, product cards, catalogue headers, and the "Discover Creators" section. |
| `cover_image_url`     | VARCHAR(500) | NULLABLE                    | URL of the wide banner image shown at the top of the artist's public profile page. |
| `verification_status` | ENUM         | NOT NULL, DEFAULT 'pending' | One of `pending`, `approved`, `rejected`. Artists cannot publish catalogues or products until `approved`. |
| `rejection_reason`    | VARCHAR(500) | NULLABLE                    | Optional explanation provided by the admin when setting status to `rejected`. Surfaced to the artist after rejection. |
| `verified_at`         | TIMESTAMP    | NULLABLE                    | Timestamp of the approval or rejection action.               |
| `verified_by`         | UUID         | FK → USERS.id, NULLABLE     | The admin user who performed the verification action.        |
| `created_at`          | TIMESTAMP    | NOT NULL                    | Profile creation time, corresponding to artist registration. |
| `updated_at`          | TIMESTAMP    | NOT NULL                    | Last time any profile field was modified.                    |

### Relationships

- **Belongs to** `USERS` (one-to-one via `user_id`)
- **Verified by** `USERS` (many-to-one via `verified_by` — the admin user)
- **Has many** `PRODUCTS` — all products the artist has listed
- **Has many** `CATALOGUES` — all catalogues the artist has created
- **Has many** `POSTS` — all stories and insight articles the artist has written
- **Has many** `BROADCASTS` — all subscriber messages sent
- **Has many** `FOLLOWS` — all buyer-follow relationships targeting this artist
- **Has many** `ORDERS` — all orders received (denormalised `artist_id` on the order)
- **Has many** `ARTIST_REVENUE_TREND` rows — monthly time-series performance data
- **Has many** `ANALYTICS_SNAPSHOTS` — AI-generated summaries for this artist

### Design Notes

`follower_count` is not stored as a column here; it is computed from `COUNT(FOLLOWS WHERE artist_id = ?)` or maintained via a counter cache. The displayed follower count on the frontend (e.g., "1,240 Followers") comes from this count. Storing it denormalised would require careful cache invalidation on every follow/unfollow.

------

## 3. BUYER_PROFILES

### Purpose

Stores buyer-specific personal information beyond what is in `USERS`. Buyers are the consumers of the platform: they browse, follow artists, add items to cart, place orders, and leave reviews. This table is lightweight because most buyer-specific data (addresses, payment methods, orders) lives in dedicated tables.

### Frontend Functionality Served

- **Buyer Profile Page** (`/buyer/profile`) — full name, phone, join date, KPI stats
- **Admin: Buyers Table** (`/admin/buyers`) — name, email (from USERS), order count
- **Order confirmation** — buyer name in admin order list
- **Checkout** — buyer's name associated with the order

### Columns

| Column       | Type         | Constraints           | Description                                                  |
| ------------ | ------------ | --------------------- | ------------------------------------------------------------ |
| `id`         | UUID         | PK                    | Profile identifier.                                          |
| `user_id`    | UUID         | FK → USERS.id, UNIQUE | Links to the authentication record. UNIQUE enforces one buyer profile per user. |
| `full_name`  | VARCHAR(150) | NOT NULL              | The buyer's display name. Shown in admin tables and on the profile page. |
| `phone`      | VARCHAR(20)  | NULLABLE              | Contact phone number. Displayed on the buyer's profile page. |
| `created_at` | TIMESTAMP    | NOT NULL              | Profile creation timestamp, represents when the buyer registered. |
| `updated_at` | TIMESTAMP    | NOT NULL              | Last profile modification time.                              |

### Relationships

- **Belongs to** `USERS` (one-to-one via `user_id`)
- **Has many** `FOLLOWS` — artists this buyer follows
- **Has many** `CART_ITEMS` — current shopping cart contents
- **Has many** `ORDERS` — all historical orders placed
- **Has many** `REVIEWS` — all reviews and comments written
- **Has many** `CATALOGUE_VIEWS` — view tracking records
- **Has many** `CATALOGUE_LIKES` — likes given to catalogues

------

## 4. ADDRESSES

### Purpose

Stores one or more shipping addresses for a user (buyer or artist). Buyers use addresses at checkout. The platform supports multiple saved addresses, with one designated as the default. During checkout, the selected address is snapshotted onto the `ORDERS` table so that address changes do not retroactively affect historical orders.

### Frontend Functionality Served

- **Checkout page** (`/buyer/checkout`) — "Home Address" card and "+ Add New Address" option
- **Buyer Profile page** (`/buyer/profile`) — "Default Shipping Address" display section with Edit button
- **Order Details** (in `buyer/Orders.vue`) — shipping address shown when "View Details" is expanded

### Columns

| Column         | Type         | Constraints               | Description                                                  |
| -------------- | ------------ | ------------------------- | ------------------------------------------------------------ |
| `id`           | UUID         | PK                        | Address identifier.                                          |
| `user_id`      | UUID         | FK → USERS.id             | The user who owns this address.                              |
| `label`        | VARCHAR(50)  | NULLABLE                  | Human-readable label such as "Home", "Work", or "Studio". Displayed in the address selector at checkout. |
| `full_address` | TEXT         | NOT NULL                  | Street address, building number, or any unstructured address line. |
| `city`         | VARCHAR(100) | NOT NULL                  | City name.                                                   |
| `state`        | VARCHAR(100) | NOT NULL                  | State or province.                                           |
| `pin_code`     | VARCHAR(20)  | NOT NULL                  | Postal/PIN code.                                             |
| `country`      | VARCHAR(100) | NOT NULL, DEFAULT 'India' | Country name.                                                |
| `is_default`   | BOOLEAN      | DEFAULT false             | If `true`, this address is pre-selected at checkout. Only one address per user should have this set to `true`. |
| `created_at`   | TIMESTAMP    | NOT NULL                  | When this address was added.                                 |

### Relationships

- **Belongs to** `USERS` (many-to-one via `user_id`)

### Design Notes

At order placement, the full address details are serialised as JSON into `ORDERS.shipping_address_snapshot`. This means this table represents the user's current address book, while the snapshot represents the truth at time of purchase. If a buyer updates their home address, their past order records are unaffected.

------

## 5. PAYMENT_METHODS

### Purpose

Stores saved payment instruments (credit/debit cards) for users. UPI payments are typically session-based and not stored. This table allows returning buyers to check out faster by selecting a saved card. Sensitive card details are never stored raw — only the last 4 digits and expiry for display purposes. The actual payment token would be held by a payment gateway (e.g., Razorpay, Stripe).

### Frontend Functionality Served

- **Checkout page** (`/buyer/checkout`) — "Credit / Debit Card" and "UPI" payment options; card form fields
- **Buyer Profile page** (`/buyer/profile`) — "Payment Method" section showing card type, last 4 digits, and expiry

### Columns

| Column         | Type        | Constraints   | Description                                                  |
| -------------- | ----------- | ------------- | ------------------------------------------------------------ |
| `id`           | UUID        | PK            | Payment method identifier.                                   |
| `user_id`      | UUID        | FK → USERS.id | The user who owns this payment method.                       |
| `card_type`    | VARCHAR(50) | NOT NULL      | Card network name: "Visa", "MasterCard", "RuPay", etc. Displayed on the profile page. |
| `last_4`       | VARCHAR(4)  | NOT NULL      | Last four digits of the card number. Used for display only (e.g., "•••• 4242"). |
| `expiry_month` | VARCHAR(2)  | NOT NULL      | Two-digit expiry month (e.g., "12").                         |
| `expiry_year`  | VARCHAR(4)  | NOT NULL      | Four-digit expiry year (e.g., "2028").                       |
| `is_default`   | BOOLEAN     | DEFAULT false | If `true`, this card is pre-selected at checkout.            |
| `created_at`   | TIMESTAMP   | NOT NULL      | When this payment method was saved.                          |

### Relationships

- **Belongs to** `USERS` (many-to-one via `user_id`)

### Design Notes

A `payment_gateway_token` column (VARCHAR) should be added in production to store the tokenised reference from the payment gateway. This table as designed is sufficient for the frontend's display and selection requirements but should be extended before real transactions are processed.

------

## 6. FOLLOWS

### Purpose

Models the relationship between a buyer and an artist when the buyer chooses to follow the artist. Following gives buyers access to the artist's feed on their dashboard (new catalogues, stories) and adds the artist to the buyer's "Following" page. This is a simple many-to-many join table with no tier differentiation (the earlier tier concept of Follower/Fan/Patron has been removed).

### Frontend Functionality Served

- **Buyer: Artist Profile page** (`/buyer/artist/:id`) — Follow/Following toggle button, follower count display
- **Buyer: Following page** (`/buyer/following`) — full list of followed artists with unfollow functionality
- **Buyer: Dashboard** (`/buyer/dashboard`) — "New Catalogue from Your Creators" section only shows catalogues from followed artists
- **Artist: Subscribers page** (`/artist/sendouts`) — total follower count displayed in the audience overview

### Columns

| Column       | Type      | Constraints             | Description                                                  |
| ------------ | --------- | ----------------------- | ------------------------------------------------------------ |
| `id`         | UUID      | PK                      | Follow relationship identifier.                              |
| `buyer_id`   | UUID      | FK → BUYER_PROFILES.id  | The buyer who initiated the follow.                          |
| `artist_id`  | UUID      | FK → ARTIST_PROFILES.id | The artist being followed.                                   |
| `created_at` | TIMESTAMP | NOT NULL                | When the follow relationship was created. Used for sorting "recently followed" lists. |

### Constraints

- A composite UNIQUE constraint on `(buyer_id, artist_id)` prevents duplicate follows.

### Relationships

- **Belongs to** `BUYER_PROFILES` (many-to-one via `buyer_id`)
- **Belongs to** `ARTIST_PROFILES` (many-to-one via `artist_id`)

### Design Notes

The follower count shown on artist profile pages should be computed as `SELECT COUNT(*) FROM FOLLOWS WHERE artist_id = ?`. For high-traffic artists, a denormalised counter cache column on `ARTIST_PROFILES` can be maintained via database triggers or application-level logic.

------

## 7. PRODUCTS

### Purpose

The central commerce entity. Represents a single handcrafted product that an artist lists for sale on the platform. Products exist independently of catalogues — they can be browsed in the global products listing and also grouped into catalogues. A product has a single price (the earlier multi-tier pricing model has been removed).

### Frontend Functionality Served

- **Buyer: Products page** (`/buyer/products`) — grid of all products with search and category filter
- **Buyer: Product Details page** (`/buyer/product/:id`) — full product view with gallery, description, materials, dimensions, stock status, add to cart
- **Buyer: Dashboard** (`/buyer/dashboard`) — "Trending Handcrafts" product grid
- **Buyer: Artist page** (`/buyer/artist/:id`) — "Artworks by [Artist]" product grid
- **Buyer: Catalogue page** (`/buyer/catalogue/:id`) — "Pieces in this Catalogue" product grid
- **Artist: Products page** (`/artist/products`) — artist's own product management grid
- **Artist: New Catalogue builder** (`/artist/newcatalogue`) — product selection step
- **Cart and Checkout** — product details referenced in cart items and order items

### Columns

| Column        | Type          | Constraints             | Description                                                  |
| ------------- | ------------- | ----------------------- | ------------------------------------------------------------ |
| `id`          | UUID          | PK                      | Product identifier.                                          |
| `artist_id`   | UUID          | FK → ARTIST_PROFILES.id | The artist who owns and listed this product.                 |
| `title`       | VARCHAR(200)  | NOT NULL                | Product name displayed on cards and detail pages (e.g., "Handcrafted Ceramic Vase"). |
| `description` | TEXT          | NULLABLE                | Long-form description of the product, its story, and intended use. Displayed on the product detail page. |
| `materials`   | TEXT          | NULLABLE                | Materials used in the product (e.g., "Stoneware clay, speckled matte glaze interior"). |
| `dimensions`  | VARCHAR(200)  | NULLABLE                | Size information (e.g., "12in Height x 6in Diameter (approximate)"). |
| `price`       | DECIMAL(10,2) | NOT NULL                | The single sale price for this product in INR.               |
| `category`    | VARCHAR(100)  | NULLABLE                | Product category used for filtering (e.g., "Home Decor", "Fine Art", "Jewelry"). Displayed as a badge on product cards. |
| `in_stock`    | BOOLEAN       | DEFAULT true            | Controls whether the "Add to Cart" button is active. Displayed as "In Stock" or "Sold Out" on the detail page. |
| `is_deleted`  | BOOLEAN       | DEFAULT false           | Soft-delete flag. Deleted products are hidden from buyers but their historical order records are preserved. |
| `created_at`  | TIMESTAMP     | NOT NULL                | When the product was first listed.                           |
| `updated_at`  | TIMESTAMP     | NOT NULL                | Last modification time.                                      |

### Relationships

- **Belongs to** `ARTIST_PROFILES` (many-to-one via `artist_id`)
- **Has many** `PRODUCT_IMAGES` — the gallery of images for this product
- **Has many** `CATALOGUE_PRODUCTS` — associations to catalogues this product appears in
- **Has many** `ORDER_ITEMS` — records of this product being purchased
- **Has many** `CART_ITEMS` — current cart instances of this product
- **Has many** `REVIEWS` (polymorphic via `target_type = 'product'`) — buyer reviews

------

## 8. PRODUCT_IMAGES

### Purpose

Stores the ordered gallery of images for a product. The product detail page displays a primary large image with thumbnail alternatives that the buyer can click through. One image is marked as primary and is used as the thumbnail on product cards throughout the platform.

### Frontend Functionality Served

- **Buyer: Product Details page** (`/buyer/product/:id`) — main image display and thumbnail row
- **Buyer: Products page** — product card thumbnail (primary image)
- **Artist: Products page** (`/artist/products`) — product card gallery header image
- **Cart, Checkout, Orders** — `is_primary` image shown as the product thumbnail

### Columns

| Column       | Type         | Constraints      | Description                                                  |
| ------------ | ------------ | ---------------- | ------------------------------------------------------------ |
| `id`         | UUID         | PK               | Image record identifier.                                     |
| `product_id` | UUID         | FK → PRODUCTS.id | The product this image belongs to.                           |
| `image_url`  | VARCHAR(500) | NOT NULL         | Full URL to the image asset (hosted on a CDN or object storage like S3). |
| `is_primary` | BOOLEAN      | DEFAULT false    | If `true`, this image is used as the card thumbnail and the default main image on the detail page. Each product should have exactly one primary image. |
| `sort_order` | INT          | DEFAULT 0        | Integer controlling the display sequence of thumbnails. Lower values appear first. |
| `created_at` | TIMESTAMP    | NOT NULL         | When this image was uploaded.                                |

### Relationships

- **Belongs to** `PRODUCTS` (many-to-one via `product_id`)

------

## 9. CATALOGUES

### Purpose

A catalogue is a curated, visually themed collection of products created by an artist. It functions as a mini-storefront or editorial drop — artists compose them with a title, philosophy statement, artist note, cover image, and colour theme, then publish them to their subscribers. Buyers can browse catalogues from artists they follow or discover them on the platform. Catalogues are a core differentiator of the Kala platform.

### Frontend Functionality Served

- **Artist: Catalogues page** (`/artist/catalogues`) — grid of all catalogues with status badges and stats
- **Artist: New Catalogue builder** (`/artist/newcatalogue`) — 4-step form: details (title, narrative), visuals (cover photo, theme), products, launch settings
- **Buyer: Dashboard** (`/buyer/dashboard`) — "New Catalogue from Your Creators" story-card grid
- **Buyer: Catalogue page** (`/buyer/catalogue/:id`) — full catalogue view with hero image, philosophy, artist note, and product grid
- **Artist: Subscribers/Broadcasts** (`/artist/sendouts`) — catalogues listed for broadcast attachment

### Columns

| Column            | Type         | Constraints             | Description                                                  |
| ----------------- | ------------ | ----------------------- | ------------------------------------------------------------ |
| `id`              | UUID         | PK                      | Catalogue identifier.                                        |
| `artist_id`       | UUID         | FK → ARTIST_PROFILES.id | The artist who created this catalogue.                       |
| `title`           | VARCHAR(200) | NOT NULL                | The catalogue's display name (e.g., "The Earth Tones Collection"). |
| `narrative`       | TEXT         | NULLABLE                | Tagline or brand narrative set during creation. Sets the mood for the catalogue. |
| `cover_photo_url` | VARCHAR(500) | NULLABLE                | URL of the full-bleed hero image displayed at the top of the catalogue page and on catalogue cards. |
| `theme`           | ENUM         | DEFAULT 'earth'         | Visual colour theme applied to the catalogue page. One of `warm`, `earth`, `cool`, `dark`. |
| `launch_intent`   | ENUM         | DEFAULT 'live'          | The catalogue's commercial intent: `live` (immediate sale), `preview` (exclusive preview), `preorder` (pre-order only). |
| `status`          | ENUM         | DEFAULT 'draft'         | Lifecycle status: `draft` (not visible to buyers), `live` (publicly visible), `ended` (no longer active). |
| `philosophy`      | TEXT         | NULLABLE                | A longer editorial statement about the collection's concept and inspiration. Displayed in the catalogue's body section. |
| `artist_note`     | TEXT         | NULLABLE                | A personal note from the artist about this specific collection. Displayed as a pull-quote block. |
| `published_at`    | TIMESTAMP    | NULLABLE                | When the catalogue was first set to `live`. Used for sorting "newest catalogues". |
| `created_at`      | TIMESTAMP    | NOT NULL                | When the catalogue record was first created (may be in draft). |
| `updated_at`      | TIMESTAMP    | NOT NULL                | Last modification timestamp.                                 |

### Relationships

- **Belongs to** `ARTIST_PROFILES` (many-to-one via `artist_id`)
- **Has many** `CATALOGUE_PRODUCTS` — the products included in this catalogue
- **Has one** `CATALOGUE_STATS` — denormalised performance metrics
- **Has many** `CATALOGUE_VIEWS` — individual view events
- **Has many** `CATALOGUE_LIKES` — individual like events
- **Has many** `BROADCASTS` — broadcasts that link to this catalogue
- **Has many** `REVIEWS` (polymorphic via `target_type = 'catalogue'`)

------

## 10. CATALOGUE_PRODUCTS

### Purpose

The join table connecting catalogues and products. A product can appear in multiple catalogues, and a catalogue contains multiple products. This table also stores a `sort_order` to control the display sequence of products within a specific catalogue.

### Frontend Functionality Served

- **Artist: New Catalogue builder** (`/artist/newcatalogue`) — Step 3 (Products): visual selection grid with checkboxes
- **Buyer: Catalogue page** (`/buyer/catalogue/:id`) — "Pieces in this Catalogue" product grid, in the order defined by `sort_order`

### Columns

| Column         | Type | Constraints        | Description                                                  |
| -------------- | ---- | ------------------ | ------------------------------------------------------------ |
| `id`           | UUID | PK                 | Join record identifier.                                      |
| `catalogue_id` | UUID | FK → CATALOGUES.id | The catalogue this association belongs to.                   |
| `product_id`   | UUID | FK → PRODUCTS.id   | The product being included in the catalogue.                 |
| `sort_order`   | INT  | DEFAULT 0          | Controls the left-to-right, top-to-bottom display order of products within the catalogue. |

### Constraints

- Composite UNIQUE on `(catalogue_id, product_id)` prevents a product from being added to the same catalogue twice.

### Relationships

- **Belongs to** `CATALOGUES` (many-to-one via `catalogue_id`)
- **Belongs to** `PRODUCTS` (many-to-one via `product_id`)

------

## 11. CATALOGUE_STATS

### Purpose

A denormalised summary table that caches aggregate performance metrics for each catalogue. Rather than running expensive `COUNT` and `SUM` queries across `ORDERS`, `CATALOGUE_VIEWS`, and `CATALOGUE_LIKES` on every page load, this table is updated incrementally (via triggers or background jobs) and read directly. This is essential for the artist's catalogue grid, which must display revenue, order count, reach, and likes for every card simultaneously.

### Frontend Functionality Served

- **Artist: Catalogues page** (`/artist/catalogues`) — the stat bar on each catalogue card: `₹ revenue`, `📦 orders`, `👁 reach`, `❤ likes`

### Columns

| Column          | Type          | Constraints                | Description                                                  |
| --------------- | ------------- | -------------------------- | ------------------------------------------------------------ |
| `id`            | UUID          | PK                         | Stats record identifier.                                     |
| `catalogue_id`  | UUID          | FK → CATALOGUES.id, UNIQUE | One stats row per catalogue. UNIQUE enforces this.           |
| `total_views`   | INT           | DEFAULT 0                  | Total number of view events recorded in `CATALOGUE_VIEWS`.   |
| `total_likes`   | INT           | DEFAULT 0                  | Total number of like events recorded in `CATALOGUE_LIKES`.   |
| `total_revenue` | DECIMAL(12,2) | DEFAULT 0                  | Sum of `ORDER_ITEMS.price_at_purchase * quantity` for items from this catalogue's products. |
| `total_orders`  | INT           | DEFAULT 0                  | Count of distinct orders containing at least one product from this catalogue. |
| `last_updated`  | TIMESTAMP     | NOT NULL                   | When the stats were last recalculated. Useful for debugging stale data. |

### Relationships

- **Belongs to** `CATALOGUES` (one-to-one via `catalogue_id`)

### Design Notes

This table is read-heavy and write-occasionally. Updates are triggered by: a new `CATALOGUE_VIEWS` row being inserted, a `CATALOGUE_LIKES` row being inserted or deleted, or an `ORDER` being placed containing a product from this catalogue.

------

## 12. CATALOGUE_VIEWS

### Purpose

Records individual page view events when a buyer loads a catalogue. Used as the source of truth for the `total_views` counter in `CATALOGUE_STATS` and for time-series analytics (e.g., "views this week" charts). Anonymous views (unauthenticated users) can be recorded with a null `buyer_id`.

### Frontend Functionality Served

- **Buyer: Catalogue page** (`/buyer/catalogue/:id`) — triggers a view event on page load
- **Artist: Catalogues page** — `👁 reach` stat derived from this table
- **Artist: Analytics** — view trend over time charts

### Columns

| Column         | Type      | Constraints                      | Description                                                  |
| -------------- | --------- | -------------------------------- | ------------------------------------------------------------ |
| `id`           | UUID      | PK                               | View event identifier.                                       |
| `catalogue_id` | UUID      | FK → CATALOGUES.id               | Which catalogue was viewed.                                  |
| `buyer_id`     | UUID      | FK → BUYER_PROFILES.id, NULLABLE | The buyer who viewed it. Null for anonymous/unauthenticated views. |
| `viewed_at`    | TIMESTAMP | NOT NULL                         | Exact timestamp of the view event.                           |

### Relationships

- **Belongs to** `CATALOGUES` (many-to-one via `catalogue_id`)
- **Belongs to** `BUYER_PROFILES` (many-to-one, nullable, via `buyer_id`)

------

## 13. CATALOGUE_LIKES

### Purpose

Records when a buyer "likes" a catalogue. Unlike views, likes are a deliberate buyer action and are unique per buyer per catalogue (a buyer cannot like the same catalogue twice). The like count contributes to `CATALOGUE_STATS.total_likes` and is used as a social signal in analytics and potential algorithmic ranking.

### Frontend Functionality Served

- **Buyer: Catalogue page** — like/unlike button (not yet implemented in the provided frontend, but the data model supports it)
- **Artist: Catalogues page** — `❤ likes` stat on catalogue cards
- **Artist: Analytics** — engagement metrics

### Columns

| Column         | Type      | Constraints            | Description                   |
| -------------- | --------- | ---------------------- | ----------------------------- |
| `id`           | UUID      | PK                     | Like event identifier.        |
| `catalogue_id` | UUID      | FK → CATALOGUES.id     | The catalogue that was liked. |
| `buyer_id`     | UUID      | FK → BUYER_PROFILES.id | The buyer who liked it.       |
| `liked_at`     | TIMESTAMP | NOT NULL               | When the like was given.      |

### Constraints

- Composite UNIQUE on `(catalogue_id, buyer_id)` ensures a buyer can only like a catalogue once.

### Relationships

- **Belongs to** `CATALOGUES` (many-to-one via `catalogue_id`)
- **Belongs to** `BUYER_PROFILES` (many-to-one via `buyer_id`)

------

## 14. POSTS

### Purpose

Represents the editorial content that artists publish to the platform — both **Stories** (artist-facing creation via `/artist/story`) and **Insights** (buyer-facing cultural/historical articles about their craft). Both content types share the same data structure (title, body, cover image) and are differentiated only by the `type` enum. Posts are the primary vehicle for artists to build a narrative around their brand and products.

### Frontend Functionality Served

- **Artist: New Story composer** (`/artist/story`) — title, cover image upload, rich body text, publish action
- **Buyer: Dashboard** (`/buyer/dashboard`) — "Behind the Art: History & Culture" insight cards (image, artist, title, excerpt)
- **Buyer: Insight detail page** (`/buyer/insight/:id`) — full article render with hero image, lead paragraph, headings, blockquotes, inline images
- **Admin: Dashboard** — "active stories" KPI count

### Columns

| Column            | Type         | Constraints             | Description                                                  |
| ----------------- | ------------ | ----------------------- | ------------------------------------------------------------ |
| `id`              | UUID         | PK                      | Post identifier.                                             |
| `artist_id`       | UUID         | FK → ARTIST_PROFILES.id | The artist who authored this post.                           |
| `type`            | ENUM         | NOT NULL                | `story` (personal studio updates) or `insight` (cultural/craft educational articles). Controls routing and display context. |
| `title`           | VARCHAR(300) | NOT NULL                | The post title. Displayed on cards and as the article heading. |
| `body`            | TEXT         | NOT NULL                | Full article body. Stored as Markdown or HTML. Rendered on the detail page with support for paragraphs, headings, blockquotes, and inline images. |
| `cover_image_url` | VARCHAR(500) | NULLABLE                | URL of the hero image shown at the top of the article and on the card thumbnail. |
| `is_published`    | BOOLEAN      | DEFAULT false           | If `false`, the post is in draft and not visible to buyers.  |
| `published_at`    | TIMESTAMP    | NULLABLE                | When the post was first published. Displayed as "Published X days ago". |
| `created_at`      | TIMESTAMP    | NOT NULL                | When the draft was first saved.                              |
| `updated_at`      | TIMESTAMP    | NOT NULL                | Last edit timestamp.                                         |

### Relationships

- **Belongs to** `ARTIST_PROFILES` (many-to-one via `artist_id`)

### Design Notes

An `excerpt` field is not stored separately — the frontend derives it by truncating `body`. Alternatively, a `excerpt` VARCHAR column can be added for artist-controlled teaser text on cards.

------

## 15. REVIEWS

### Purpose

Stores buyer-written reviews and comments on both products and catalogues. Uses a polymorphic pattern where `target_type` specifies whether the review is about a product or catalogue, and `target_id` holds the UUID of that entity. Reviews include an optional numeric `rating` (1–5) and a free-text body. They are the source of the **sentiment analysis** that feeds the artist's AI-generated analytics summary.

### Frontend Functionality Served

- **Buyer: Product Details page** — buyer can leave a review (UI to be added; data model is ready)
- **Buyer: Catalogue page** — buyer can comment on a catalogue
- **Artist: Analytics / Dashboard** — AI sentiment summary generated from review body texts
- **Artist: Subscribers page** — engagement quality signals

### Columns

| Column        | Type      | Constraints            | Description                                                  |
| ------------- | --------- | ---------------------- | ------------------------------------------------------------ |
| `id`          | UUID      | PK                     | Review identifier.                                           |
| `buyer_id`    | UUID      | FK → BUYER_PROFILES.id | The buyer who wrote this review.                             |
| `target_type` | ENUM      | NOT NULL               | `product` or `catalogue`. Specifies which entity is being reviewed. |
| `target_id`   | UUID      | NOT NULL               | The UUID of the product or catalogue being reviewed. Not a formal FK (polymorphic). |
| `rating`      | INT       | NULLABLE, CHECK (1–5)  | Star rating from 1 to 5. Nullable so that comments without ratings are supported. |
| `body`        | TEXT      | NOT NULL               | The text of the review or comment. Used for sentiment analysis. |
| `is_deleted`  | BOOLEAN   | DEFAULT false          | Soft-delete flag allowing moderation without destroying the record. |
| `created_at`  | TIMESTAMP | NOT NULL               | When the review was submitted.                               |
| `updated_at`  | TIMESTAMP | NOT NULL               | Last edit timestamp (buyers may be allowed to edit within a window). |

### Relationships

- **Belongs to** `BUYER_PROFILES` (many-to-one via `buyer_id`)
- **Polymorphically associated** with `PRODUCTS` or `CATALOGUES` via `target_type` + `target_id`

### Design Notes

Because `target_id` is polymorphic, a database-level foreign key constraint cannot be applied. Application-level validation must ensure `target_id` refers to a valid record of the type specified by `target_type`. An index on `(target_type, target_id)` is essential for efficiently fetching all reviews for a given product or catalogue.

------

## 16. ORDERS

### Purpose

The central transaction record. An order is created when a buyer completes checkout. It captures the full financial and logistical details of the transaction — buyer, artist, status, totals, and snapshots of the shipping address and payment method at the time of purchase. The snapshot pattern means the order record is self-contained and does not depend on the buyer's current address or payment records for historical accuracy.

### Frontend Functionality Served

- **Buyer: Orders page** (`/buyer/orders`) — full order list with status badges, item thumbnails, totals, tracking and details expandables
- **Buyer: Checkout page** (`/buyer/checkout`) — order is created on "Pay & Place Order"; success state shown
- **Artist: Orders page** (`/artist/orders`) — Kanban board showing orders received by this artist
- **Admin: Orders page** (`/admin/orders`) — full platform order table with search and status filter
- **Admin: Dashboard** — recent orders list and total order KPI
- **Admin: Analytics** — revenue and order trend charts

### Columns

| Column                      | Type          | Constraints                 | Description                                                  |
| --------------------------- | ------------- | --------------------------- | ------------------------------------------------------------ |
| `id`                        | UUID          | PK                          | Order identifier. Displayed as human-readable order number (e.g., "ORD-99382") via a separate sequence or prefix. |
| `buyer_id`                  | UUID          | FK → BUYER_PROFILES.id      | The buyer who placed the order.                              |
| `artist_id`                 | UUID          | FK → ARTIST_PROFILES.id     | The artist whose products are in this order. Denormalised for fast admin and artist queries. |
| `status`                    | ENUM          | NOT NULL, DEFAULT 'pending' | Order lifecycle: `pending`, `processing`, `shipped`, `delivered`, `cancelled`. |
| `subtotal`                  | DECIMAL(10,2) | NOT NULL                    | Sum of all order item totals before shipping.                |
| `shipping_cost`             | DECIMAL(10,2) | NOT NULL                    | Shipping fee applied to this order.                          |
| `total`                     | DECIMAL(10,2) | NOT NULL                    | `subtotal + shipping_cost`. The amount charged to the buyer. |
| `shipping_address_snapshot` | JSON          | NOT NULL                    | Complete address details captured at checkout time. Preserves the delivery address even if the buyer updates their address book later. |
| `payment_snapshot`          | JSON          | NOT NULL                    | Payment method details (card type, last 4, method type) captured at checkout. For record-keeping only. |
| `created_at`                | TIMESTAMP     | NOT NULL                    | When the order was placed.                                   |
| `updated_at`                | TIMESTAMP     | NOT NULL                    | Last status update time.                                     |

### Relationships

- **Belongs to** `BUYER_PROFILES` (many-to-one via `buyer_id`)
- **Belongs to** `ARTIST_PROFILES` (many-to-one via `artist_id`)
- **Has many** `ORDER_ITEMS` — the individual products in this order
- **Has many** `ORDER_TRACKING_EVENTS` — the chronological history of status changes

### Design Notes

The current schema assumes one artist per order. If the platform evolves to support multi-artist carts (a buyer buys from two artists in one checkout), the `artist_id` column would need to move to `ORDER_ITEMS` and the order itself would not be artist-scoped. For the current implementation, multi-artist carts are not supported.

------

## 17. ORDER_ITEMS

### Purpose

Each row represents one product line in an order. Stores a snapshot of the product's details (title, image, artist name, price) at the time of purchase, preventing changes to the product's current listing from affecting historical order records.

### Frontend Functionality Served

- **Buyer: Orders page** (`/buyer/orders`) — item image thumbnails, product title, artist name for each order
- **Artist: Orders page** (`/artist/orders`) — item name, quantity, and line price in each Kanban card
- **Admin: Orders page** — item count per order (derived)
- **Buyer: Checkout** — order summary items list

### Columns

| Column                   | Type          | Constraints                | Description                                                  |
| ------------------------ | ------------- | -------------------------- | ------------------------------------------------------------ |
| `id`                     | UUID          | PK                         | Order item identifier.                                       |
| `order_id`               | UUID          | FK → ORDERS.id             | The order this item belongs to.                              |
| `product_id`             | UUID          | FK → PRODUCTS.id, NULLABLE | Reference to the live product record. Nullable so records survive if a product is later deleted. |
| `product_title_snapshot` | VARCHAR(200)  | NOT NULL                   | Product title at time of purchase. Displayed in order history even if product is renamed or deleted. |
| `product_image_snapshot` | VARCHAR(500)  | NULLABLE                   | Primary image URL at time of purchase.                       |
| `artist_name_snapshot`   | VARCHAR(150)  | NOT NULL                   | Artist's brand name at time of purchase.                     |
| `price_at_purchase`      | DECIMAL(10,2) | NOT NULL                   | Unit price charged. May differ from current product price.   |
| `quantity`               | INT           | NOT NULL, DEFAULT 1        | Number of units purchased.                                   |

### Relationships

- **Belongs to** `ORDERS` (many-to-one via `order_id`)
- **References** `PRODUCTS` (many-to-one via `product_id`, nullable)

------

## 18. ORDER_TRACKING_EVENTS

### Purpose

An append-only log of status change events for an order. Each time an order moves from one status to another (e.g., artist marks it as "shipped"), a new row is inserted here. This provides the full timeline displayed in the buyer's order tracking view. The current status of the order is always in `ORDERS.status`; this table provides the historical event log.

### Frontend Functionality Served

- **Buyer: Orders page** (`/buyer/orders`) — "Delivery Status" tracking timeline with event names and timestamps, revealed when "Track Order" is clicked

### Columns

| Column       | Type      | Constraints    | Description                                                  |
| ------------ | --------- | -------------- | ------------------------------------------------------------ |
| `id`         | UUID      | PK             | Tracking event identifier.                                   |
| `order_id`   | UUID      | FK → ORDERS.id | The order this event belongs to.                             |
| `event`      | ENUM      | NOT NULL       | The event type: `confirmed`, `dispatched`, `out_for_delivery`, `delivered`, `cancelled`. |
| `note`       | TEXT      | NULLABLE       | Optional artist or system note about this status change (e.g., "Dispatched via BlueDart, tracking: XYZ"). |
| `created_at` | TIMESTAMP | NOT NULL       | When this event occurred. Displayed as the step timestamp in the timeline. |

### Relationships

- **Belongs to** `ORDERS` (many-to-one via `order_id`)

------

## 19. CART_ITEMS

### Purpose

Persists the buyer's shopping cart server-side. This allows carts to survive browser refreshes, session expiration, and cross-device access. Each row represents one product in the cart with a quantity. Cart items are cleared (deleted) after a successful order is placed.

### Frontend Functionality Served

- **Buyer: Cart page** (`/buyer/cart`) — item list with images, titles, artist names, quantity controls, remove button, order summary totals
- **Buyer: Navbar** (`BuyerNavbar.vue`) — cart item count badge
- **Buyer: Checkout** (`/buyer/checkout`) — cart contents displayed in order summary sidebar

### Columns

| Column       | Type      | Constraints            | Description                                     |
| ------------ | --------- | ---------------------- | ----------------------------------------------- |
| `id`         | UUID      | PK                     | Cart item identifier.                           |
| `buyer_id`   | UUID      | FK → BUYER_PROFILES.id | The buyer who owns this cart item.              |
| `product_id` | UUID      | FK → PRODUCTS.id       | The product added to the cart.                  |
| `quantity`   | INT       | NOT NULL, DEFAULT 1    | How many units of this product are in the cart. |
| `added_at`   | TIMESTAMP | NOT NULL               | When this item was first added.                 |
| `updated_at` | TIMESTAMP | NOT NULL               | When the quantity was last changed.             |

### Constraints

- Composite UNIQUE on `(buyer_id, product_id)` — a product appears once per cart; incrementing quantity updates the `quantity` column rather than adding a new row.

### Relationships

- **Belongs to** `BUYER_PROFILES` (many-to-one via `buyer_id`)
- **References** `PRODUCTS` (many-to-one via `product_id`)

------

## 20. BROADCASTS

### Purpose

Records broadcast messages sent by artists to their subscribers. A broadcast is a direct communication from the artist to all their followers — it can include a message, be associated with a catalogue (e.g., announcing a new launch), declare a commercial intent, and be synced to external social media platforms. The `platforms` JSON column stores which platforms (email, Instagram, Facebook, Telegram) the message was posted to.

### Frontend Functionality Served

- **Artist: Subscribers & Broadcasts page** (`/artist/sendouts`) — compose form (catalogue selection, message, intent, platform toggles, live preview), send action
- **Artist: Catalogues page** — ending a catalogue or launching a new one may trigger a broadcast
- **Follower notifications** — the broadcast record drives what notifications/emails followers receive

### Columns

| Column         | Type      | Constraints                  | Description                                                  |
| -------------- | --------- | ---------------------------- | ------------------------------------------------------------ |
| `id`           | UUID      | PK                           | Broadcast identifier.                                        |
| `artist_id`    | UUID      | FK → ARTIST_PROFILES.id      | The artist who created and sent this broadcast.              |
| `catalogue_id` | UUID      | FK → CATALOGUES.id, NULLABLE | Optional link to a catalogue being promoted. If present, the broadcast includes a catalogue attachment in the preview. |
| `message`      | TEXT      | NOT NULL                     | The body of the broadcast message.                           |
| `intent`       | ENUM      | NOT NULL                     | `launch`, `preorder`, `flash_sale`, or `exclusive_reveal`. Used to label the message and may affect display formatting. |
| `platforms`    | JSON      | NOT NULL                     | Array of platform identifiers the message was posted to, e.g., `["email", "telegram"]`. |
| `status`       | ENUM      | DEFAULT 'draft'              | `draft`, `sent`, or `failed`.                                |
| `scheduled_at` | TIMESTAMP | NULLABLE                     | If set, the broadcast is queued for future delivery.         |
| `sent_at`      | TIMESTAMP | NULLABLE                     | When the broadcast was actually delivered.                   |
| `created_at`   | TIMESTAMP | NOT NULL                     | When the broadcast was first saved.                          |

### Relationships

- **Belongs to** `ARTIST_PROFILES` (many-to-one via `artist_id`)
- **References** `CATALOGUES` (many-to-one, nullable, via `catalogue_id`)

------

## 21. ANALYTICS_SNAPSHOTS

### Purpose

Stores AI-generated analytical summaries for both artists and the platform admin. When an analytics summary is requested (or generated on schedule), the current metrics are collected, sent to an LLM, and the resulting summaries are stored here for fast retrieval. This avoids regenerating expensive AI summaries on every page load. Includes both a general performance summary and, for artists, a sentiment summary derived from buyer reviews.

### Frontend Functionality Served

- **Artist: Analytics / Dashboard** — AI-generated performance summary and sentiment analysis of buyer reviews
- **Admin: Analytics page** (`/admin/analytics`) — "AI Insights" section (currently a placeholder in the frontend, backed by this table)

### Columns

| Column              | Type        | Constraints | Description                                                  |
| ------------------- | ----------- | ----------- | ------------------------------------------------------------ |
| `id`                | UUID        | PK          | Snapshot identifier.                                         |
| `entity_type`       | ENUM        | NOT NULL    | `artist` or `platform`. Determines whether this snapshot is for an individual artist or the admin-level platform view. |
| `entity_id`         | UUID        | NULLABLE    | For `artist` type: the `ARTIST_PROFILES.id`. For `platform` type: null. |
| `period`            | VARCHAR(20) | NOT NULL    | The time period this snapshot covers (e.g., "2026-03", "2026-Q1", "all-time"). |
| `metrics`           | JSON        | NOT NULL    | The raw metrics data that was fed to the AI (revenue, orders, views, review count, average rating, etc.). |
| `ai_summary`        | TEXT        | NULLABLE    | The AI-generated natural language summary of performance metrics. |
| `sentiment_summary` | TEXT        | NULLABLE    | For artist snapshots: AI-generated analysis of buyer sentiment from review texts. |
| `generated_at`      | TIMESTAMP   | NOT NULL    | When this snapshot was generated. Used to determine if a fresh snapshot is needed. |

### Relationships

- **Associated with** `ARTIST_PROFILES` (many-to-one via `entity_id` when `entity_type = 'artist'`)

------

## 22. ARTIST_REVENUE_TREND

### Purpose

A time-series table storing monthly aggregated performance metrics for each artist. Populated by a scheduled background job (e.g., nightly or monthly) that aggregates data from `ORDERS`, `CATALOGUE_VIEWS`, and `POSTS`. Used to generate the line/dual-axis chart on the artist's dashboard.

### Frontend Functionality Served

- **Artist: Dashboard** (`/artist/dashboard`) — "Performance Over Time" dual-axis line chart (Revenue on left axis, Catalogue Views on right axis), across months (Jan–Jul etc.)
- **Artist: Analytics** — trend charts and KPI comparisons

### Columns

| Column                  | Type          | Constraints             | Description                                                |
| ----------------------- | ------------- | ----------------------- | ---------------------------------------------------------- |
| `id`                    | UUID          | PK                      | Trend record identifier.                                   |
| `artist_id`             | UUID          | FK → ARTIST_PROFILES.id | The artist this data point belongs to.                     |
| `month`                 | VARCHAR(7)    | NOT NULL                | Period identifier in YYYY-MM format (e.g., "2026-03").     |
| `revenue`               | DECIMAL(12,2) | DEFAULT 0               | Total revenue from completed orders in this month.         |
| `orders`                | INT           | DEFAULT 0               | Number of orders received in this month.                   |
| `catalogue_views`       | INT           | DEFAULT 0               | Total views across all catalogues in this month.           |
| `story_engagement_rate` | FLOAT         | NULLABLE                | Percentage of followers who engaged with posts this month. |
| `recorded_at`           | TIMESTAMP     | NOT NULL                | When this data point was written/updated.                  |

### Constraints

- Composite UNIQUE on `(artist_id, month)` — one row per artist per month.

### Relationships

- **Belongs to** `ARTIST_PROFILES` (many-to-one via `artist_id`)

------

## 23. PLATFORM_REVENUE_TREND

### Purpose

A time-series table storing monthly aggregated platform-wide metrics. Analogous to `ARTIST_REVENUE_TREND` but scoped to the entire marketplace. Populated by the same scheduled aggregation jobs. Used by the admin analytics page.

### Frontend Functionality Served

- **Admin: Dashboard** (`/admin/dashboard`) — "Revenue Trend" line chart
- **Admin: Analytics** (`/admin/analytics`) — Revenue Trend and Orders Trend charts; KPIs for revenue, signups, orders, average order value

### Columns

| Column            | Type          | Constraints | Description                                                  |
| ----------------- | ------------- | ----------- | ------------------------------------------------------------ |
| `id`              | UUID          | PK          | Trend record identifier.                                     |
| `month`           | VARCHAR(7)    | UNIQUE      | Period in YYYY-MM format. One row per month for the whole platform. |
| `revenue`         | DECIMAL(12,2) | DEFAULT 0   | Total platform revenue from all completed orders this month. |
| `new_signups`     | INT           | DEFAULT 0   | Number of new user registrations this month.                 |
| `total_orders`    | INT           | DEFAULT 0   | Total orders placed across the platform this month.          |
| `avg_order_value` | DECIMAL(10,2) | DEFAULT 0   | Mean order total for this month.                             |
| `recorded_at`     | TIMESTAMP     | NOT NULL    | When this record was last written/updated.                   |

------

## 24. Entity Relationship Summary

The following summarises the key foreign-key relationships across the schema:

```
USERS
  ├── ARTIST_PROFILES (1:1)
  │     ├── PRODUCTS (1:N)
  │     │     ├── PRODUCT_IMAGES (1:N)
  │     │     └── CATALOGUE_PRODUCTS (N:M via join)
  │     ├── CATALOGUES (1:N)
  │     │     ├── CATALOGUE_PRODUCTS (1:N)
  │     │     ├── CATALOGUE_STATS (1:1)
  │     │     ├── CATALOGUE_VIEWS (1:N)
  │     │     └── CATALOGUE_LIKES (1:N)
  │     ├── POSTS (1:N)
  │     ├── BROADCASTS (1:N)
  │     ├── ORDERS (1:N, as seller)
  │     ├── FOLLOWS (1:N, as followee)
  │     ├── ARTIST_REVENUE_TREND (1:N)
  │     └── ANALYTICS_SNAPSHOTS (1:N)
  │
  ├── BUYER_PROFILES (1:1)
  │     ├── FOLLOWS (1:N, as follower)
  │     ├── CART_ITEMS (1:N)
  │     ├── ORDERS (1:N, as buyer)
  │     │     ├── ORDER_ITEMS (1:N)
  │     │     └── ORDER_TRACKING_EVENTS (1:N)
  │     ├── REVIEWS (1:N)
  │     ├── CATALOGUE_VIEWS (1:N)
  │     └── CATALOGUE_LIKES (1:N)
  │
  ├── ADDRESSES (1:N)
  └── PAYMENT_METHODS (1:N)

PLATFORM_REVENUE_TREND (standalone, platform-level)
ANALYTICS_SNAPSHOTS (platform-level rows have null entity_id)
```

### Cross-Domain Interactions

| Interaction                | Tables Involved                                              | Trigger               |
| -------------------------- | ------------------------------------------------------------ | --------------------- |
| Buyer places order         | CART_ITEMS → ORDERS + ORDER_ITEMS + ORDER_TRACKING_EVENTS    | Checkout completion   |
| Artist ships order         | ORDERS.status update + ORDER_TRACKING_EVENTS insert          | Artist Kanban action  |
| Buyer views catalogue      | CATALOGUE_VIEWS insert + CATALOGUE_STATS.total_views increment | Catalogue page load   |
| Buyer likes catalogue      | CATALOGUE_LIKES insert + CATALOGUE_STATS.total_likes increment | Like button click     |
| Artist publishes catalogue | CATALOGUES.status = 'live', CATALOGUES.published_at set      | Publish action        |
| Buyer follows artist       | FOLLOWS insert                                               | Follow button         |
| Buyer unfollows artist     | FOLLOWS delete                                               | Unfollow button       |
| Artist sends broadcast     | BROADCASTS insert, delivery jobs triggered                   | Send Broadcast action |
| Analytics refresh          | ORDERS + CATALOGUE_VIEWS + REVIEWS aggregated → ARTIST_REVENUE_TREND + ANALYTICS_SNAPSHOTS | Scheduled job         |
| Admin approves artist      | ARTIST_PROFILES.verification_status = 'approved', verified_at + verified_by set | Admin action          |
| Admin suspends user        | USERS.is_suspended = true                                    | Admin action          |