# XSS Attacks Prevention System

## Project Overview
This project illustrates a comprehensive approach to preventing Cross-Site Scripting (XSS) attacks in a web application. It features a multi-layered defense strategy including context-aware sanitization, advisory detection, security headers, and a monitoring dashboard.

## System Architecture

### 1. Core Application Layer
- **`app.py`**: Initializes the Flask application, registers blueprints (main, admin, dashboard), and attaches middleware.
- **`config.py`**: Centralized configuration for secret keys, database URI, and CSP policy.
- **`extensions.py`**: Manages Flask extensions (SQLAlchemy, Migrate, Talisman) to prevent circular imports.

### 2. Data Layer
- **`models/comment.py`**: orm model for storing user comments. Keeps `raw_text` for analysis and `sanitized_text` for display.
- **`models/attack_log.py`**: Records metadata about suspected XSS attempts (payload, risk score, matched rules).

### 3. Service Layer (The Brain)
- **`services/sanitization_service.py`**: Uses `bleach` to clean HTML and provides methods for context-specific encoding (HTML, JS, URL).
- **`services/detection_service.py`**: Regex-based heuristic engine to detect and score suspicious patterns (e.g., `<script>`, `onmouseover`).
- **`services/security_service.py`**: The orchestration layer. It calls detection, logs threats, and *always* sanitizes input before return.

### 4. Middleware Layer
- **`middleware/headers.py`**: Enforces strict security headers:
    - `Content-Security-Policy` (CSP)
    - `X-Content-Type-Options`
    - `X-Frame-Options`
- **`middleware/request_logger.py`**: Logs request metadata (IP, Method, Duration) for forensic analysis.

### 5. Dashboard & Analytics
- **`dashboard/analytics.py`**: Aggregates data for the dashboard (attack distribution, recent threats).
- **`dashboard/routes.py`**: Endpoints for the admin interface.

## Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd xss-io
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize the database** (if not already done):
    ```bash
    python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
    ```

4.  **Run the application**:
    ```bash
    flask run
    ```
    or
    ```bash
    python app.py
    ```

5.  **Access the application**:
    - Home: `http://127.0.0.1:5000/`
    - Dashboard: `http://127.0.0.1:5000/dashboard/`

## Typical System Workflow

1.  **User Input**: User submits a comment via the web form.
2.  **Client-Side Validation**: Basic JS checks (can be bypassed).
3.  **Server Reception**: valid request reaches `app.py`.
4.  **Security Orchestration**:
    - **Detection**: `DetectionService` scans for patterns. If suspicious, it's logged to `AttackLog`.
    - **Sanitization**: `SanitizationService` strips dangerous tags using `bleach`.
5.  **Storage**: The **sanitized** version is stored in the `Comment` table.
6.  **Response**: The page renders. `sanitized_text` is safe to display. Additional protection is provided by CSP headers.

## Security Features Demonstrated
- **Context-Aware Encoding**: Different strategies for HTML body vs. attributes vs. JS.
- **Content Security Policy**: Restricts sources of scripts and styles.
- **Audit Logging**: Keeps a record of potential attacks for review.
- **Defense in Depth**: Even if one layer fails (e.g., regex detection), sanitization and CSP provide backup.
