# 🖼️ PasswordNotepad.exe

[![Platform](https://img.shields.io/badge/Platform-Windows%20x64-blue)](https://github.com/)
[![Security](https://img.shields.io/badge/Encryption-AES--256--GCM-red)](https://cryptography.io/)
[![Format](https://img.shields.io/badge/Output-PNG%20(Lossless)-orange)](https://www.w3.org/PNG/)

---

## 📖 Overview

`PasswordNotepad.exe` is a standalone, zero-dependency Windows application for cryptographically securing structured data. It transforms JSON records, credentials, and configuration files into self-contained, password-protected PNG images featuring a unique geometric glyph pattern. 

Built on a deterministic, offline-first pipeline, the tool guarantees **100% lossless data recovery**. No cloud sync, no telemetry, no external dependencies. Your data stays on your machine, encrypted, and visually verifiable.

---

## ⚡ Key Features

| Feature | Description |
|---------|-------------|
| 🖥️ **Standalone Executable** | Runs natively on Windows x64. No Python, runtimes, or admin rights required. |
| 🔐 **Zero-Knowledge Architecture** | Passwords are never stored, logged, or transmitted. Decryption happens entirely in local RAM. |
| 📦 **Strict Schema Enforcement** | Data is serialized via `proto3` (`SerPaswd`), ensuring type safety and compact binary representation. |
| 🗜️ **High-Efficiency Compression** | Zstandard (Level 22) reduces payload size by 40–70% before encryption. |
| 🔣 **Visual Cryptographic Codec** | Binary payloads are mapped to a deterministic grid of `/` and `\` symbols (10×10px cells). |
| 🛡️ **Tamper-Evident Output** | AES-256-GCM authentication tags instantly detect corruption or unauthorized modification. |

---

## 🔄 How It Works

`PasswordNotepad.exe` processes your data through a verified, sequential pipeline:

---

Structured Data (JSON) 
   ↓
📦 Protobuf Serialization (SerPaswd schema validation)
   ↓
🗜️ Zstandard Compression (Level 22)
   ↓
🔒 AES-256-GCM Encryption (PBKDF2-HMAC-SHA256 + 16-byte salt)
   ↓
🔣 Binary-to-Glyph Mapping (Crypto padding → / & \ grid)
   ↓
🖼️ PNG Generation (Dark background + white geometric lines)

---

Each generated image contains:
- A randomly generated 16-byte salt embedded in the ciphertext
- A 12-byte AES nonce for stream uniqueness
- A 16-byte GCM authentication tag for integrity verification
- A mathematically precise glyph grid representing the encrypted payload

---

## 🚀 Getting Started

### 1️⃣ Launch the Application
Run `PasswordNotepad.exe`. No installation or unpacking required.

### 2️⃣ Encode Data → PNG
1. Paste your JSON or structured text into the input field.
2. Set a strong password (minimum 8 characters recommended).
3. Click **Generate Image**.
4. Save the resulting `.png` file.

### 3️⃣ Decode PNG → Data
1. Open `PasswordNotepad.exe` and select **Decode**.
2. Load your previously saved `.png` file.
3. Enter the exact password used during encoding.
4. Click **Extract**. Your original data is instantly restored.

---

## 🔐 Security Architecture

| Component | Implementation |
|-----------|----------------|
| **Key Derivation** | `PBKDF2-HMAC-SHA256` (600,000 iterations, OWASP 2023 compliant) |
| **Cipher Mode** | `AES-256-GCM` (authenticated encryption with associated data) |
| **Salt & Nonce** | Cryptographically random (`os.urandom`), unique per encoding |
| **Integrity Check** | 16-byte GCM tag fails immediately on wrong password or file corruption |
| **Memory Safety** | All sensitive data held in volatile RAM, wiped on exit |

> 🔒 **Design Principle:** The application follows a strict zero-trust model. If the password is lost, recovery is cryptographically impossible. This is intentional and ensures absolute data sovereignty.

---

## ⚠️ Important Guidelines

- 🖼️ **Format Requirement:** Always save/load as **PNG**. Lossy compression (JPEG, WebP, HEIC) alters pixel values and permanently breaks the glyph grid.
- 💾 **Data Limits:** Recommended payload size ≤ 10 MB per image. Larger datasets require proportionally more RAM during visualization.
- 🌐 **Offline-Only:** The application never connects to the internet. No updates, no telemetry, no background services.
- 📝 **Schema Compliance:** Input must align with the `SerPaswd` structure (`record_id`, `title`, `description`, `login`, `password`). Malformed JSON will be rejected before encryption.

---

## 🤝 Transparency & Auditing

`PasswordNotepad.exe` is built on the open-source **Visual Glyphs** cryptographic core. The complete Python pipeline, `proto3` schema definitions, and build instructions are publicly available for independent security audits, reproducibility testing, and community verification.
