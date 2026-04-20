## Getting Started

### Prerequisites

Make sure you have the following installed:
- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL 14+
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/IAmNotNotYash/SoftwareEngineering.git
cd SoftwareEngineering
```

---

### 2. Frontend Setup

```bash
cd ../frontend
```

**Install dependencies:**
```bash
npm install
```

**Run the Vue development server:**
```bash
npm run dev
```
The frontend will be available at `http://localhost:5173`.

> During development the frontend and backend run on separate ports. Vue's dev server proxies API requests to Flask — this is configured in `vite.config.js`.