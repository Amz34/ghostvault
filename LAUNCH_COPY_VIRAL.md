# Public Launch Announcement Deck

Direct distribution copy for GhostVault release across technical and founder channels.

---

## 1. LinkedIn Announcement

Google wanted $24/year for an "80% full" storage alert. 
I spent Sunday afternoon auditing their IMAP & Drive APIs instead.

Here is the truth Big Tech does not advertise:
My 622 emails were not filling up my account. They only consumed 768 MB (4.9% of the 15 GB quota).

Google's UI bundles Gmail + Drive + Photos into one red warning banner to drive subscriptions to Google One.

Instead of paying recurring storage fees or deleting irreplaceable business records, I engineered GhostVault: an open-source, zero-loss cloud archiver.

What happens in 30 seconds:
1. Pulls raw byte-for-byte RFC822 email archives & Drive objects.
2. Runs cryptographic checksum verification (MD5/SHA256) across all 266 files — 0 differences found.
3. Purges the originals from server quota.
4. Quota drops from 80% to 5%.
5. Dispatches an auto-flagged starred email with single-click restore commands.

Total cost: $0.00.
Data lost: 0 bytes.

Two tracks included:
- Track A: 3 clicks, zero terminal, immediate fix.
- Track B: Python CLI, IMAP protocol internals, and rclone parity.

Full open-source code & repo: https://github.com/Amz34/ghostvault

---

## 2. X (Twitter) Technical Thread

Google’s $1.99/mo storage upgrade is one of the most effective subscription funnels on the internet.

Your inbox is rarely full. Google's storage calculation simply bundles everything together.

I analyzed Google’s storage APIs and built an open-source tool that drops your quota to 5% without deleting a single file.

Technical breakdown 🧵👇

1/ The Storage Split:
Google bundles Gmail + Drive + Photos into a single 15 GB pool.
When you see "80% full", the intuitive reaction is: "I need to delete emails."

Our audit showed:
All 600+ emails with attachments = 768 MB total (only 4.9% of the pool).
The real culprits: obsolete video recordings and un-emptied Trash sitting in Drive.

2/ The Protocol Catch:
You cannot simply EXPUNGE Gmail emails via IMAP.
[Gmail]/All Mail silently clears the deleted flag to prevent accidental loss.

The RFC-compliant path:
1. UID MOVE to [Gmail]/Trash
2. Select [Gmail]/Trash
3. Set \Deleted flags
4. Call EXPUNGE

3/ The Solution: GhostVault
- Mirrors Google Drive to Cloudflare R2 ($0 egress) or Local SSD.
- Cryptographically verifies all files with MD5/SHA256 checksums (266 files, 0 differences).
- Safely clears server quota.
- Quota: 80% down to 5%.

4/ Full Open Source Release:
100% Free. Zero Data Loss.
Repository: https://github.com/Amz34/ghostvault

---

## 3. Hacker News (Show HN)

**Title:** Show HN: GhostVault – Zero-loss Google quota reclaimer using IMAP & rclone parity

**Body:**
Hey HN,

Recently hit Google’s warning banner indicating that account storage was at 80% and incoming emails would be blocked unless upgraded to Google One.

Before subscribing, I ran a forensic script using IMAP getquotaroot and the Google Drive v3 API to inspect the storage distribution.

Key observations:
1. IMAP RFC 8438 SIZE revealed that 622 emails with attachments only occupied 768 MB (<5% of the 15 GB quota).
2. The remaining 11+ GB was tied up in old video assets and un-emptied Google Drive Trash (which retains files for 30 days against quota).
3. Gmail’s IMAP implementation clears \Deleted flags on [Gmail]/All Mail. Permanent removal requires an explicit UID MOVE to [Gmail]/Trash followed by a mailbox-scoped expunge.

I packaged this into GhostVault: a lightweight CLI that streams Drive and RFC822 raw emails into a local SSD or Cloudflare R2 bucket, validates parity via rclone check (0 byte divergence), and then safely clears the server quota.

The repo includes a 3-click guide for non-technical users and full CLI instructions for engineers.

GitHub: https://github.com/Amz34/ghostvault
Feedback and PRs welcome.
