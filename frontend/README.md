# RepoClarity AI frontend
Web interface for RepoClarity AI, enabling repository indexing and AI-powered code exploration.
## Overview

This frontend allows users to:
* Index code repositories
* Chat with AI models about the codebase
* Switch between different AI providers

> Requires the RepoClarity backend API to be running.

## Features

* Repository indexing via backend API
* AI-powered Q&A over indexed code
* * Support for multiple AI models (local)

## Requirements

* NodeJS **22+**

## Tech-Stack

* Vue 3
* Nuxt 4
* TailwindCSS
* Pinia
* Nuxt UI

## Setup

Make sure to install dependencies:

```bash
# npm
npm install
```

**Note:** Nuxt UI is currently not compatible with vue-router 5.x.  
If installation fails, use:
```bash
# npm
npm install --legacy-peer-deps
```

## Backend dependency

Requires the RepoClarity backend API running at:
http://localhost:8000

Make sure the backend is running and accessible before using the UI.

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev
```

Once running, open http://localhost:3000 to access the UI.

## Production

Build the application for production:

```bash
# npm
npm run build
```

Locally preview production build:

```bash
# npm
npm run preview
```

Check out the official [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

## Project Structure

- `/pages` – application routes
- `/components` – reusable UI components
- `/stores` – Pinia state management
- `/composables` – reusable logic (e.g. API calls)
- `/types` – TypeScript types and interfaces
- `/layouts` – layout components

## Configuration

Currently no environment variables are required.