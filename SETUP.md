# Development Environment Setup Guide

This guide walks you through setting up your Mac to work on the GGI website using Claude Code and the helper scripts in the `tools/` directory.

## What You'll Install

- **Homebrew** - A package manager that makes it easy to install other tools
- **Git** - Version control system for tracking code changes
- **Node.js** - JavaScript runtime needed to run the website locally
- **Python 3** - Programming language used by helper scripts
- **Pillow** - Python library for image processing
- **Claude Code** - AI coding assistant

---

## Step 1: Open Terminal

1. Press `Cmd + Space` to open Spotlight Search
2. Type `Terminal` and press Enter
3. A window with a command prompt will appear

You'll type all commands in this window. After typing each command, press **Enter** to run it.

---

## Step 2: Install Homebrew

Homebrew is a package manager that simplifies installing developer tools on Mac.

Copy and paste this entire command into Terminal, then press Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- You'll be prompted to enter your Mac password (the one you use to log in)
- When you type your password, no characters will appear - this is normal
- Press Enter after typing your password
- Follow any on-screen prompts (press Enter when asked)

**Important**: After installation completes, Homebrew may display instructions to add it to your PATH. If you see lines like "Add Homebrew to your PATH...", copy and run those commands.

To verify Homebrew is installed, run:

```bash
brew --version
```

You should see a version number like `Homebrew 4.x.x`.

---

## Step 3: Install Git

Git tracks changes to code and lets you sync with GitHub.

```bash
brew install git
```

Verify it's installed:

```bash
git --version
```

You should see something like `git version 2.x.x`.

### Configure Git with Your Identity

Replace the placeholder text with your actual name and email, then run these commands:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 4: Install Node.js

Node.js runs the website's development server.

```bash
brew install node
```

Verify installation:

```bash
node --version
npm --version
```

You should see version numbers for both.

---

## Step 5: Install Python 3

Python runs the helper scripts in the `tools/` directory.

macOS includes Python, but let's ensure you have a recent version:

```bash
brew install python
```

Verify installation:

```bash
python3 --version
```

You should see something like `Python 3.x.x`.

### Install Pillow (Image Processing Library)

The `add-post.py` script requires Pillow for image processing:

```bash
pip3 install Pillow
```

---

## Step 6: Clone the Repository

Now you'll download the website code from GitHub.

First, decide where to store the project. A common location is a folder called `Projects` or `Code` in your home directory. Run these commands to create that folder and navigate into it:

```bash
mkdir -p ~/Projects
cd ~/Projects
```

Now clone (download) the repository:

```bash
git clone https://github.com/steve31415/ggi.git
```

Navigate into the project folder:

```bash
cd ggi
```

---

## Step 7: Install Project Dependencies

The website uses various JavaScript libraries that need to be downloaded:

```bash
npm install
```

This may take a minute. You'll see progress output as packages are downloaded.

---

## Step 8: Verify the Website Runs

Start the development server:

```bash
npm run dev
```

You should see output indicating the server is running, typically at `http://localhost:3000`.

Open your web browser and go to: **http://localhost:3000**

You should see the GGI website.

**To stop the server**: Go back to Terminal and press `Ctrl + C`.

---

## Step 9: Install Claude Code

Claude Code is an AI assistant that helps you write and modify code.

1. Visit https://docs.anthropic.com/en/docs/claude-code/installing
2. Follow the installation instructions for macOS
3. After installation, you can run Claude Code from Terminal:

```bash
claude
```

### Using Claude Code with This Project

1. Open Terminal
2. Navigate to the project folder:
   ```bash
   cd ~/Projects/ggi
   ```
3. Start Claude Code:
   ```bash
   claude
   ```

Claude Code will read the project's `CLAUDE.md` file to understand the codebase and can help you:
- Add new blog posts
- Modify the website
- Debug issues
- Understand the code

---

## Using the Helper Scripts

The `tools/` directory contains Python scripts to automate common tasks.

### add-post.py

Automates adding a blog post from secondthoughts.ai to the website.

**Usage:**

```bash
python3 tools/add-post.py <article-url> <header-image>
```

**Examples:**

With a local image file:
```bash
python3 tools/add-post.py https://secondthoughts.ai/p/some-article ./my-image.jpg
```

With an image URL:
```bash
python3 tools/add-post.py https://secondthoughts.ai/p/some-article https://example.com/image.jpg
```

**What it does:**
1. Pulls the latest code from GitHub
2. Extracts article metadata (title, author, date) from the URL
3. Creates an MDX file in the `posts/` folder
4. Processes the header image (crops to 4:3 ratio) and saves it
5. Updates the homepage to show the new post

**After running:**
1. Start the dev server (`npm run dev`) to preview
2. If everything looks good, commit and push the changes

---

## Common Terminal Commands

Here are commands you'll use frequently:

| Command | What it does |
|---------|--------------|
| `cd ~/Projects/ggi` | Navigate to the project folder |
| `npm run dev` | Start the development server |
| `Ctrl + C` | Stop the running server |
| `git pull` | Download latest changes from GitHub |
| `git status` | See what files have changed |
| `git add -A` | Stage all changes for commit |
| `git commit -m "message"` | Save changes with a description |
| `git push` | Upload changes to GitHub |
| `claude` | Start Claude Code |

---

## Troubleshooting

### "command not found" Errors

If you see `command not found` after installing something:
1. Close Terminal completely (`Cmd + Q`)
2. Open Terminal again
3. Try the command again

### Permission Errors

If you see "Permission denied" when running npm install:
```bash
sudo chown -R $(whoami) ~/.npm
npm install
```

### Port Already in Use

If you see an error about port 3000 being in use:
- Another application is using that port
- Either close that application, or run the dev server on a different port:
  ```bash
  npm run dev -- -p 3001
  ```
  Then visit http://localhost:3001

### Git Authentication Issues

If Git asks for credentials when pushing:
1. Create a Personal Access Token on GitHub:
   - Go to GitHub.com > Settings > Developer settings > Personal access tokens > Tokens (classic)
   - Generate a new token with "repo" permissions
2. Use that token as your password when prompted

---

## Getting Help

- **Claude Code**: Just ask Claude for help with any coding task
- **This README**: Check `README.md` and `CLAUDE.md` for project-specific info
- **Issues**: Report problems at https://github.com/steve31415/ggi/issues
