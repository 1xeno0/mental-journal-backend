# Backend PRD: Serene -- Flask API (SQLite Edition)

## Role of the Backend

The backend is responsible for:

-   Secure authentication
-   Private journal data storage
-   AI-powered "Vibe Check" generation
-   Weekly mood analytics
-   Strict data isolation between users
-   Single-container deployment compatibility

The backend must prioritize:

-   Security
-   Simplicity
-   Maintainability
-   Clear API contracts

------------------------------------------------------------------------

# 1. Architecture Overview

## Stack

-   Flask
-   SQLAlchemy
-   SQLite
-   OpenAI API
-   JWT Authentication (httpOnly cookies)
-   Docker (single container)

## API Namespace

All backend routes must exist under:

/api/\*

The frontend must never access the database directly.

------------------------------------------------------------------------

# 2. Database Design

## Database Type

SQLite

Default connection:

sqlite:///./data/serene.db

Database file must be stored in:

/data

to allow Docker volume persistence.

------------------------------------------------------------------------

## A. User Table

  Field           Type            Description
  --------------- --------------- ----------------
  id              UUID (string)   Primary key
  email           string          Unique
  password_hash   string          Bcrypt hashed
  created_at      datetime        Auto-generated

------------------------------------------------------------------------

## B. Entry Table

  Field         Type            Description
  ------------- --------------- ----------------
  id            UUID            Primary key
  user_id       UUID            Foreign key
  mood          string          Required
  tags          string (JSON)   Optional
  note          text            Required
  ai_response   text            Optional
  created_at    datetime        Auto-generated
  updated_at    datetime        Auto-updated

------------------------------------------------------------------------

# 3. Authentication System

## Authentication Method

JWT stored in httpOnly cookie

## Security Requirements

-   Passwords hashed using bcrypt
-   JWT verified on every protected route
-   All queries filtered by user_id
-   No user data leaks

------------------------------------------------------------------------

## Endpoints

### POST /api/auth/register

Creates user.

Request: { "email": "user@email.com", "password": "securepassword" }

Response: { "success": true }

Sets authentication cookie.

------------------------------------------------------------------------

### POST /api/auth/login

Authenticates user. Sets JWT cookie.

------------------------------------------------------------------------

### POST /api/auth/logout

Clears JWT cookie.

------------------------------------------------------------------------

### GET /api/auth/me

Returns: { "id": "...", "email": "..." }

------------------------------------------------------------------------

# 4. Journal Entry API

All routes require authentication.

------------------------------------------------------------------------

## POST /api/entries

Creates entry.

Validation Rules: - note must be ≥ 50 characters - mood required - tags
optional

Behavior: - Automatically triggers AI Vibe Check - Stores AI response

------------------------------------------------------------------------

## GET /api/entries

Query parameters: - from - to

Returns entries sorted newest first.

------------------------------------------------------------------------

## GET /api/entries/{id}

Ownership enforced.

------------------------------------------------------------------------

## PUT /api/entries/{id}

Updates: - mood - tags - note

If note changes: - Re-run AI

------------------------------------------------------------------------

## DELETE /api/entries/{id}

Deletes entry.

------------------------------------------------------------------------

# 5. AI "Vibe Check" System

## Primary Endpoint

POST /api/ai/vibe-check

Used internally by entry creation and optionally directly by frontend.

------------------------------------------------------------------------

## Trigger Conditions

AI executes only if:

-   note ≥ 50 characters
-   note not empty
-   note not gibberish

------------------------------------------------------------------------

## AI Behavior Requirements

The AI must:

-   Respond in 1--2 sentences
-   Be supportive
-   Avoid diagnosis
-   Avoid clinical language
-   Avoid crisis instructions
-   Maintain calm tone

------------------------------------------------------------------------

## Safety Guardrails

If note contains trigger phrases such as:

-   suicide
-   kill myself
-   self harm
-   want to die

Return standard disclaimer:

"If you're feeling unsafe or overwhelmed, please consider reaching out
to someone you trust or a local support service."

No extended AI analysis should follow.

------------------------------------------------------------------------

## Optional Streaming Endpoint (Advanced)

POST /api/ai/vibe-check/stream

Returns Server-Sent Events (SSE). Not required for MVP.

------------------------------------------------------------------------

# 6. Weekly Analytics Endpoint

## GET /api/analytics/weekly

Returns mood distribution for current week.

Example response: { "happy": 4, "anxious": 2, "calm": 3 }

------------------------------------------------------------------------

# 7. Error Response Standard

All errors must return: { "error": "Human readable message", "code":
"ERROR_CODE" }

HTTP status codes must be accurate.

------------------------------------------------------------------------

# 8. Non-Functional Requirements

-   Cold start \< 3 seconds
-   API latency \< 500ms (excluding AI call)
-   All secrets via environment variables
-   Works via single docker run
-   SQLite file persisted via Docker volume

------------------------------------------------------------------------

# 9. Environment Variables

DATABASE_URL=sqlite:///./data/serene.db JWT_SECRET=supersecret
OPENAI_API_KEY=...

------------------------------------------------------------------------

# 10. Out of Scope (MVP)

-   Social login
-   Email verification
-   Role system
-   Multi-user sharing
-   Admin interface
-   Background job queue

------------------------------------------------------------------------

# 11. Implementation Order

Recommended backend build order:

1.  Database models
2.  Authentication system
3.  Entry CRUD
4.  AI integration
5.  Analytics endpoint
6.  Docker production hardening
