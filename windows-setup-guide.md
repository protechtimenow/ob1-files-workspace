# 🪟 OB-1 Windows Setup Guide

## 🚨 You're on Windows - Different Setup Required!

The path `/workspaces/` is for **GitHub Codespaces/Linux**, not Windows!

---

## ✅ CORRECT WINDOWS PATHS:

### 📂 Your Current Location:
```powershell
PS C:\Users\Moham\OneDrive\Documents\GitHub\ob1-files-workspace>
```

### 🎯 Correct Commands for Windows:
```powershell
# You're already in the right place!
cd C:\Users\Moham\OneDrive\Documents\GitHub\ob1-files-workspace

# OR if you want to navigate properly:
cd "C:\Users\Moham\OneDrive\Documents\GitHub\ob1-files-workspace"
```

---

## 🛠️ INSTALL OB-1 MCP TOOLKIT ON WINDOWS:

### 1. **Prerequisites:**
```powershell
# Install Node.js if not already installed
# Download from: https://nodejs.org/

# Check if installed:
node --version
npm --version
```

### 2. **Setup MCP Server:**
```powershell
# Navigate to your project
cd "C:\Users\Moham\OneDrive\Documents\GitHub\ob1-files-workspace"

# Create MCP directory
mkdir ob1-copilot-mcp
cd ob1-copilot-mcp

# Initialize project
npm init -y

# Install dependencies
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node ts-node

# Create TypeScript config
echo '{"compilerOptions":{"target":"ES2020","module":"commonjs","outDir":"./dist","rootDir":"./src","strict":true,"esModuleInterop":true}}' > tsconfig.json
```

### 3. **Create Directory Structure:**
```powershell
# Create source directory
mkdir src

# Copy MCP files (already created in the repo)
# Files will be available after git pull
```

---

## ⚡ QUICK WINDOWS DEPLOYMENT:

### Option A: **Use This Repo Directly**
```powershell
# Pull latest changes
git pull origin main

# Navigate to MCP directory
cd ob1-copilot-mcp

# Install and build
npm install
npm run build

# Start MCP server
npm start
```

### Option B: **Manual Windows Installation**
```powershell
# 1. Install dependencies
npm install -g typescript ts-node

# 2. Clone/setup in Windows format
just use the files I'm pushing to your repo!
```

---

## 🎯 WINDOWS-SPECIFIC MCP CONFIG:

### Claude Desktop Config (`%APPDATA%/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "ob1-copilot-toolkit": {
      "command": "node",
      "args": ["C:\\\\Users\\\\Moham\\\\OneDrive\\\\Documents\\\\GitHub\\\\ob1-files-workspace\\\\ob1-copilot-mcp\\\\dist\\\\index.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

---

## 🚀 TESTING ON WINDOWS:

```powershell
# Test MCP server
cd "C:\Users\Moham\OneDrive\Documents\GitHub\ob1-files-workspace\ob1-copilot-mcp"
node dist/index.js

# Should see: "OB-1 + Copilot MCP Server Started"
```

---

## 🎯 COMMON WINDOWS ISSUES & FIXES:

| Issue | Fix |
|-------|-----|
| **Path not found** | Use double quotes around paths with spaces |
| **Permission denied** | Run PowerShell as Administrator |
| **Node not found** | Install Node.js from nodejs.org |
| **History file error** | Normal Windows issue, can ignore |

---

## ✅ YOUR NEXT COMMANDS:

```powershell
# 1. Stay in your current directory (it's correct!)
pwd # Should show: C:\Users\Moham\OneDrive\Documents\GitHub\ob1-files-workspace

# 2. Pull the MCP toolkit I just pushed
git pull origin main

# 3. Setup MCP
cd ob1-copilot-mcp
npm install
npm run build
npm start
```

**You're in the RIGHT place - just use Windows paths, not Linux ones!** 🪟✅