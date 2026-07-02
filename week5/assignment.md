# Week 5 – Multi-Stack AI-Accelerated Web App Build

## Assignment Overview
Build the same functional web application in 2 distinct technology stacks. At least one version must use an AI app generation platform such as [`bolt.new`](https://bolt.new/) (others include Lovable & Figma Make). At least one version must use a non-JavaScript language for either the frontend or backend (e.g., Django, Ruby on Rails).

You may reuse the app from previous weeks (the "developer control center") or create a new app of your choosing, as long as it meets the [minimum functional scope](#minimum-functional-scope). The app should be end-to-end functional (frontend + backend + persistence where applicable).

## Minimum Functional Scope 
- User can create, read, update, and delete a primary resource (e.g., notes, tasks, posts).
- Persistent storage (database or file-based) where appropriate for the stack.
- Basic validation and error handling.
- Simple but functional UI that surfaces the main flows.
- Clear instructions to run each version locally (and deploy links if you deploy).

## Stack Requirements
Build 2 separate versions of the same app, each of which use a distinct stack. Examples:
- MERN (MongoDB, Express, React, Node.js)
- MEVN (MongoDB, Express, Vue.js, Node.js)
- Flask + Vanilla JS (or React)
- Next.js + Node (or NestJS)
- Django + React (or Vue)
- Ruby on Rails (full-stack)

Reminder that at least one version must include a non-JavaScript language for either frontend or backend (e.g., Python/Django, Ruby/Rails).

## More about Bolt
Bolt is an AI-assisted development platform that generates websites, web apps, and mobile apps from natural language prompts. Users can describe their idea in plain text, and Bolt produces a functional prototype—ranging from landing pages and e-commerce sites to CRMs and mobile tools—within minutes. Learn more [here](https://support.bolt.new/building/intro-bolt).

## Tips for Usage of AI App Generators
- App generators like Bolt are best-suited for modern full-stack technologies, which you will get by default when using them without specifying specific frameworks.
- Prefer starting from a clean prompt describing your app concept, entities, routes, and UI flows.
- Clearly describe data models and relationships in your prompts.
- Iteratively refine prompts for data models, CRUD endpoints, auth (if used), and frontend components.
- Keep each version isolated to avoid dependency conflicts.
 
## Deliverables
1) **TWO** project folders (one per version) within the `week5/` folder, each including:
   - Source code
   - `README.md` with prerequisites, installation/set-up instructions, run, and env configuration
   - Notes on deviations, known issues, and any manual fixes after generation
2) Completed `writeup.md` file:
   - App Concept
   - 2 App Descriptions (1 per version)
   - Completed Reflection