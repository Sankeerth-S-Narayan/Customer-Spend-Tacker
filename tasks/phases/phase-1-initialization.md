# ✅ Phase 1: Project Initialization - Detailed Tasks

This document outlines the specific steps and commands needed to complete the project setup.

---

### Task 1.1: Initialize Local Git Repository

- [x] **Initialize Git:** Run the following command in the project root to create the repository.
  ```bash
  git init
  ```
  > **Summary:** The `git init` command was executed, creating a new `.git` directory in the project root. This initializes the project as a local Git repository, enabling version control.

- [ ] **Create Core Branches:** Run these commands to create our main branches.
  ```bash
  git branch main
  git branch dev
  git branch test
  ```
- [ ] **Switch to Development Branch:** We will start our work on the `dev` branch.
  ```bash
  git checkout dev
  ```

---

### Task 1.2: Create Project Directory Structure

- [x] **Create Service Directories:** Run this command to create the folders for our services.
  ```bash
  mkdir frontend backend db
  ```
  > **Summary:** The core directories `frontend`, `backend`, and `db` have been created at the project root. This establishes the necessary structure for our different application services.

---

### Task 1.3: Create Core Project Files

- [x] **Create `.gitignore`:** Create a file named `.gitignore` in the project root and add the following content to it. This will prevent common temporary files and secret files from being committed.
  ```gitignore
  # Byte-compiled / optimized / DLL files
  __pycache__/
  *.py[cod]
  *$py.class

  # C extensions
  *.so

  # Distribution / packaging
  .Python
  build/
  develop-eggs/
  dist/
  downloads/
  eggs/
  .eggs/
  lib/
  lib64/
  parts/
  sdist/
  var/
  wheels/
  pip-wheel-metadata/
  share/python-wheels/
  *.egg-info/
  .installed.cfg
  *.egg
  MANIFEST

  # PyInstaller
  #  Usually these files are written by a python script from a template
  #  before PyInstaller builds the exe, so as to inject date/other infos into it.
  *.manifest
  *.spec

  # Installer logs
  pip-log.txt
  pip-delete-this-directory.txt

  # Unit test / coverage reports
  htmlcov/
  .tox/
  .nox/
  .coverage
  .coverage.*
  .cache
  nosetests.xml
  coverage.xml
  *.cover
  .hypothesis/
  .pytest_cache/

  # Environments
  .env
  .venv
  env/
  venv/
  ENV/
  env.bak/
  venv.bak/

  # VSCode
  .vscode/
  ```
  > **Summary:** A comprehensive `.gitignore` file has been created at the project root. It is configured to ignore Python artifacts, virtual environments, IDE-specific folders, and environment files, ensuring our repository remains clean.

- [x] **Create `.env` file:** Create an empty file named `.env` in the project root. This file will hold our environment variables later.
  > **Summary:** An empty `.env` file was created at the project root. This file is ignored by Git and will be used to store application secrets and environment-specific configuration, such as database credentials.

- [x] **Create `README.md`:** Create a file named `README.md` in the project root and add the following content.
  ```markdown
  # Customer Spending Analytics Dashboard

  This project is a full-stack analytics platform designed to provide insights into personal spending data. It is built for local development to demonstrate a modern software engineering workflow.
  ```
  > **Summary:** A `README.md` file was created with a title and a brief project overview. This file will serve as the main entry point for understanding the project's purpose.

---

### Task 1.4: Make Initial Commit

- [ ] **Stage and Commit:** After creating all the files and folders above, run the following commands to make your first commit, following the conventional commit standard.
  ```bash
  git add .
  git commit -m "feat: initial project structure and configuration"
  ``` 