# FileStore

A self-hosted, Drive-style file storage app. Users register, log in, and upload, browse, download and delete their own files from a clean icon-grid dashboard.

Built solo, entirely on an Android phone (Termux + proot Debian).

## Features (V1)

- Register and log in with session-based auth (cookie sessions)
- Upload files with a size cap and server-side file type detection
- Dashboard with an icon grid, with icons chosen by file type
- Download and delete files
- Per-user isolation: every query is scoped to the logged-in user, so nobody can read or delete another user's files
- Rate limiting on uploads, per user
- Files stored on local disk under random UUID keys, and original filenames are sanitized and used only as display labels

## Tech stack

| Layer | Tech |
| --- | --- |
| Backend | FastAPI (Python) |
| Database | PostgreSQL, queried through [pgcraft](https://github.com/Blaqcoder005/pgcraft), a Supabase-style query builder with built-in caching and rate limiting |
| Frontend | React, Vite, Tailwind CSS, lucide-react, axios |
| Storage | Local disk (`storage/`) |

## Project structure

```
FileStore/
├── backend/
│   ├── main.py            # app, middleware, routers
│   ├── dependencies.py    # auth and rate-limit dependencies
│   └── routes/            # auth.py, files.py
└── frontend/
    └── src/
        ├── components/    # FileTile, Layout, Topbar
        ├── context/       # AuthContext
        ├── pages/         # Login, Dashboard
        └── services/      # axios client
```

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL

### 1. Database

Create a database and run:

```sql
create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  username text unique not null,
  email text unique not null,
  password_hash text not null,
  created_at timestamptz not null default now()
);

create table if not exists folders (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  parent_id uuid references folders(id) on delete cascade,
  owner_id uuid not null references users(id) on delete cascade,
  created_at timestamptz not null default now()
);

create table if not exists files (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  folder_id uuid references folders(id) on delete cascade,
  owner_id uuid not null references users(id) on delete cascade,
  storage_key text not null,
  mime_type text,
  size bigint not null,
  created_at timestamptz not null default now()
);
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env     # then fill in your values
uvicorn main:app --reload --port 8000
```

Environment variables (see `.env.example`):

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Signs session cookies, so use a long random value |

API docs are served at `http://127.0.0.1:8000/docs`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite dev server proxies `/api` to the backend, so the session cookie stays same-origin. Use the same hostname (`localhost` or `127.0.0.1`) consistently while developing.

## API overview

| Method | Path | Description |
| --- | --- | --- |
| POST | `/auth/register` | Create an account |
| POST | `/auth/login` | Log in and start a session |
| GET | `/auth/me` | Current session user |
| GET | `/files` | List the current user's files |
| POST | `/files/upload` | Upload a file (multipart, field name `file`) |
| GET | `/files/download/{id}` | Download a file the user owns |
| DELETE | `/files/{id}` | Delete a file the user owns |

## Security notes

- Session cookies are signed with `SECRET_KEY`.
- File ownership is enforced in every query, and other users' file IDs return 404.
- Uploads are size-capped, type-sniffed from file bytes, and rate limited.
- Files are stored under UUID keys, and user-supplied names never build disk paths.
- Downloads are served with `Content-Disposition: attachment`.

## Roadmap

- [x] **V1:** auth, upload, list, download, delete
- [ ] **V1b:** folders, rename, move
- [ ] **V2:** trash, search, file preview, drag and drop
- [ ] **V3:** sharing links, permissions, storage quotas
- [ ] **V4:** large and resumable uploads, thumbnails, background processing

## License

MIT, see [LICENSE](LICENSE).

## Author

**Peter Airekholo**, full-stack developer based in Nigeria.
GitHub: [@Blaqcoder005](https://github.com/Blaqcoder005)
