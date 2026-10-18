# 👻 GhostVault: The Zero-Loss Cloud Archiver

> **"Your storage is 80% full. Upgrade to Google One for $1.99/mo."**  
> We have all seen the red banner. Most people blindly pay the monthly ransom.  
> Smart engineers don't.

**GhostVault** is a lightweight, zero-dependency forensic auditor & cloud archiver that pulls your heavy Google Drive files and raw RFC822 emails into a cold vault (Cloudflare R2 or Local SSD) with **100% cryptographic checksum parity**, then safely reclaims your quota down to **<10%** — without deleting a single byte of critical data.

---

## ⚡ The Dual Playbook

Choose your lane:
1. **[Lane A: The Beginner Playbook](#-lane-a-the-beginner-playbook-no-code-3-clicks)** (No Terminal, 3 Clicks, Free Forever)
2. **[Lane B: The Hacker / Engineer Playbook](#-lane-b-the-hacker--engineer-playbook-cli--rclone)** (CLI, IMAP Internals & Cryptographic Parity)

---

## 🟢 Lane A: The Beginner Playbook (No Code, 3 Clicks)

If you don't care about code and just want that annoying red "80% full" banner gone without losing files:

### Step 1: The Secret Google Sorter Link
Don't browse folders manually. Click this direct Google link that sorts all your files by size:
👉 **[Open Drive Storage Quota Sorter](https://drive.google.com/drive/u/0/quota)**

### Step 2: Grab the 1-Click Free Snapshot (Zero Loss)
Before touching anything, get Google to package your entire Drive into a safe `.zip` for free:
👉 **[Google Takeout (100% Free Export)](https://takeout.google.com/)**
1. Deselect all, check **Drive**.
2. Click **Create Export**. Google will email you a direct download link.
3. Save it to your computer or external hard drive.

### Step 3: The 30-Day Trash Purge Trap
Deleting a file in Google Drive **DOES NOT** free up storage! It moves to Trash and sits there eating your quota for 30 days.
👉 **[Click Here to Empty Drive Trash](https://drive.google.com/drive/trash)**  
Click **"Empty trash"**. Your storage immediately drops by gigabytes.

---

## 💻 Lane B: The Hacker / Engineer Playbook (CLI & Rclone)

For developers, sysadmins, and automation engineers who want programmatic, verifiable zero-loss archiving.

```
       [Google Unified Pool (15 GB)]
      ┌──────────────┴──────────────┐
      ▼                             ▼
[Gmail IMAP]               [Google Drive API]
 (RFC822 Raw Mime)          (rclone stream)
      │                             │
      ▼                             ▼
 ┌──────────────────────────────────────┐
 │    GHOSTVAULT FORENSIC PIPELINE      │
 └──────────────────────────────────────┘
      │                             │
      ▼                             ▼
[Local SSD Vault / R2]    [Cryptographic Checksum]
(266 files, 0 diffs)      (MD5 / SHA256 parity)
```

### The Technical Trap We Discovered
1. **The `[Gmail]/All Mail` Expunge Illusion:**  
   Calling `STORE +FLAGS \Deleted` followed by `EXPUNGE` on `[Gmail]/All Mail` is a **no-op**. Gmail silently clears deleted flags to protect users. The only RFC-compliant deletion path is:
   `UID MOVE <id> "[Gmail]/Trash"` $\rightarrow$ Select `[Gmail]/Trash` $\rightarrow$ `STORE +FLAGS \Deleted` $\rightarrow$ `EXPUNGE`.
2. **The Unified Pool Deception:**  
   Google's UI screams "Storage Full!", making users think their inbox is flooded. In our live audit:
   - 622 emails = **768 MB** total (only **4.9%** of the 15 GB pool).
   - The remaining ~11.2 GB was hidden in Google Drive video assets and un-emptied Trash.

---

### Quickstart (CLI)

```bash
# 1. Clone & Setup
git clone https://github.com/Amz34/ghostvault.git
cd ghostvault
chmod +x ghostvault.py

# 2. Run Forensic Quota Audit
./ghostvault.py audit -u your-email@gmail.com

# 3. Mirror Entire Drive with Cryptographic Verification
./ghostvault.py backup -r gdrive -o ./my_vault
```

### Verification Proof
```text
$ rclone check gdrive: ./my_vault --one-way
NOTICE: Local file system at ./my_vault: 0 differences found
NOTICE: Local file system at ./my_vault: 266 matching files
```

---

## 📊 Neuromarketing FAQ

**Q: Is Google Takeout really free?**  
Yes. 100% free forever. Google only charges if you expand your active online cloud storage via Google One ($1.99/mo).

**Q: What if I need a file back?**  
One terminal command restores it back to Google Drive instantly:
```bash
rclone copy ./my_vault/specific-folder/ "gdrive:Restored/"
```

---

## 📜 License
MIT License. Build, fork, and never pay the cloud storage tax again.
