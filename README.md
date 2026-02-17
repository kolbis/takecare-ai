# TakeCare — AI-Powered Medication Assistant (WhatsApp)

> ⚠️ **Work in Progress**
> This repository is under active development. Architecture, APIs, and features may change frequently.

TakeCare is an AI-powered medication assistant built on WhatsApp.
It helps older adults manage complex medication schedules safely and reliably, while keeping caregivers informed when needed.

---

## 🌿 Motivation

This project was born from a personal need.

My mom was recently diagnosed with **Acute Myeloid Leukemia (AML)**. She now takes more than **20 different pills every day**, often while feeling overwhelmed or confused, and she lives far away.

TakeCare is being built to support her — and families like ours — by providing:

* Clear, simple medication guidance
* Timely reminders
* Safety checks
* Caregiver notifications when something seems wrong

This is not just a technical experiment.
It’s a real-world tool solving a real-world problem.

---

## 🏗 Architecture Overview

The project follows a **DDD-inspired modular structure**.

```
.
├── api/
├── app/
├── agentic/
└── shared/
```

### **api/**

FastAPI layer:

* WhatsApp webhooks
* REST endpoints
* Scheduler
* Caregiver notifications
* Infrastructure adapters

### **app/**

Core application layer (DDD):

* Use cases
* Domain entities & value objects
* Repository interfaces (currently mocked)
* RAG orchestration

### **agentic/**

AI orchestration layer:

* LangGraph flows
* Tools
* Skills
* Prompts
* Agent graph definitions

### **shared/**

Cross-cutting components:

* Shared types
* i18n (EN / HE)
* Utilities

---

## 🚧 Current Status

* Core domain modeling in progress
* Agent workflows under active experimentation
* Infrastructure adapters evolving
* Database integration not finalized
* APIs may change without notice

This repository should be considered **unstable and experimental** at this stage.

---

## ⚙️ Setup

Install dependencies:

```bash
uv sync
```

Run the API:

```bash
uv run --project api uvicorn api.main:app --reload
```

Run a specific package:

```bash
uv run --project agentic python -c "from agentic.graph.graph import graph; print(graph)"
```

---

## 🎯 Vision

TakeCare aims to become:

* A reliable AI medication companion
* A safety layer for complex treatments
* A bridge between patients and caregivers
* A multilingual (EN/HE) assistant accessible through familiar messaging platforms
