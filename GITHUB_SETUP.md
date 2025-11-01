# GitHub Repository Setup Instructions

Your local git repository has been initialized and all files have been committed. Follow these steps to create the GitHub repository and push your code:

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in to your account
2. Click the "+" icon in the top right corner and select "New repository"
3. Repository name: `whatsapp2web`
4. Choose visibility (Public or Private)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Connect and Push

After creating the repository, GitHub will show you instructions. Use these commands:

```bash
git remote add origin https://github.com/YOUR_USERNAME/whatsapp2web.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Alternative: If you already have a repository

If you've already created the repository, just run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/whatsapp2web.git
git branch -M main
git push -u origin main
```

## Current Status

✅ Git repository initialized
✅ All files committed (22 files, 1950+ lines)
✅ .gitignore created
✅ requirements.txt created
✅ README.md created

You're ready to push to GitHub!

---

# How to Clone This Repository (For Your Friends/Colleagues)

## Prerequisites

Before cloning via SSH, ensure you have:
1. **Git installed** on your system
2. **SSH key set up** with GitHub
3. **Access to the repository** (if it's private, you need to be added as a collaborator)

### Setting Up SSH Key (If Not Already Done)

1. **Check if you have an SSH key:**
   ```bash
   ls -al ~/.ssh
   ```
   Look for files named `id_rsa.pub`, `id_ed25519.pub`, or similar.

2. **If you don't have an SSH key, generate one:**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   Press Enter to accept default file location, then set a passphrase (optional but recommended).

3. **Copy your public key:**
   ```bash
   # On macOS/Linux
   cat ~/.ssh/id_ed25519.pub
   
   # On Windows (Git Bash)
   cat ~/.ssh/id_ed25519.pub
   
   # On Windows (PowerShell)
   Get-Content ~/.ssh/id_ed25519.pub
   ```

4. **Add SSH key to GitHub:**
   - Go to GitHub → Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste your public key and save

5. **Test your SSH connection:**
   ```bash
   ssh -T git@github.com
   ```
   You should see: "Hi username! You've successfully authenticated..."

## Clone the Repository via SSH

Once your SSH key is set up, clone the repository:

```bash
git clone git@github.com:YOUR_USERNAME/whatsapp2web.git
```

Replace `YOUR_USERNAME` with the actual GitHub username of the repository owner.

**Example:**
```bash
git clone git@github.com:johnsmith/whatsapp2web.git
```

## Alternative: Clone via HTTPS (If SSH is not set up)

If SSH is not configured, you can clone using HTTPS:

```bash
git clone https://github.com/YOUR_USERNAME/whatsapp2web.git
```

## After Cloning

1. **Navigate to the project directory:**
   ```bash
   cd whatsapp2web
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application:**
   - Update `config.py` with your database credentials
   - Change admin credentials in `app.py` if needed

5. **Run the application:**
   ```bash
   python app.py
   ```

## Troubleshooting

### Permission Denied Error
If you get "Permission denied (publickey)" error:
- Verify your SSH key is added to GitHub
- Test connection: `ssh -T git@github.com`
- Ensure you're using the correct GitHub username

### Repository Not Found
- Verify the repository name and username are correct
- If it's a private repository, ensure you have access
- Check if the repository exists and is spelled correctly

### SSL Certificate Error (HTTPS)
- Update your Git: `git update-git-for-windows` (Windows) or update via your package manager
- Or use SSH instead of HTTPS

