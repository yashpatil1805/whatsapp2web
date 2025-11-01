# Clone Instructions for WhatsApp2Web Repository

Quick reference guide for cloning this repository via SSH.

## Quick Clone Command

```bash
git clone git@github.com:YOUR_USERNAME/whatsapp2web.git
```

**Replace `YOUR_USERNAME` with the actual GitHub username.**

## Full Setup Instructions

### Step 1: Verify SSH Setup

Check if you have SSH keys configured:

```bash
# Check for existing SSH keys
ls -al ~/.ssh
```

### Step 2: Generate SSH Key (If Needed)

If you don't have an SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press Enter for default location, then optionally set a passphrase.

### Step 3: Add SSH Key to GitHub

1. Copy your public key:
   ```bash
   # macOS/Linux/Git Bash
   cat ~/.ssh/id_ed25519.pub
   
   # Windows PowerShell
   Get-Content ~/.ssh/id_ed25519.pub
   ```

2. Go to GitHub → Settings → SSH and GPG keys → New SSH key
3. Paste your key and save

### Step 4: Test SSH Connection

```bash
ssh -T git@github.com
```

You should see: `Hi username! You've successfully authenticated...`

### Step 5: Clone the Repository

```bash
git clone git@github.com:YOUR_USERNAME/whatsapp2web.git
cd whatsapp2web
```

### Step 6: Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 7: Configure and Run

1. Update database credentials in `config.py`
2. Run the application: `python app.py`

## HTTPS Alternative (If SSH Not Available)

```bash
git clone https://github.com/YOUR_USERNAME/whatsapp2web.git
```

## Common Issues

| Error | Solution |
|-------|----------|
| Permission denied (publickey) | Add your SSH key to GitHub |
| Repository not found | Verify username and repository name |
| Host key verification failed | Run: `ssh-keyscan github.com >> ~/.ssh/known_hosts` |

---

**Note:** Replace `YOUR_USERNAME` with the actual GitHub username throughout this document.

