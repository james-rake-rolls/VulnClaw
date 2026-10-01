---
name: ctf-misc
description: CTF misc knowledge base — Python jail escape, Bash jail escape, encoding-chain identification and decoding, QR/audio/image steganography, game-VM reversing, CTFd API navigation, Linux privilege escalation
---

# CTF Misc Knowledge Base

A practical knowledge base for CTF Misc challenges, covering **sandbox escape, encoding-chain identification, steganography, game reversing**, and other miscellaneous challenge types.

## Scenario routing

| Scenario | Reference | Core content |
|------|---------|---------|
| Python sandbox escape | `python-jail-escape.md` | `__import__` / func\_globals / eval chains |
| Bash sandbox escape | `bash-jail-escape.md` | HISTFILE / ctypes.sh / vi-editor escape |
| Encoding-chain identification and decoding | `encoding-chain-reference.md` | Base64→Hex→ROT13 multi-layer nesting |
| Game / custom-VM reversing | `game-and-vm-reverse.md` | WASM / Brainfuck / Z3 constraint solving |
| CTFd platform operations | `ctfd-platform-guide.md` | API attachment download / flag submission |
| Linux privilege escalation | `linux-privesc-quick.md` | SUID / sudo / cron / kernel exploits |

## Quick triage

| Challenge characteristic | Likely topic | Recommended reference |
|---------|---------|---------|
| Python exec/eval input box | PyJail escape | python-jail-escape.md |
| Command-line restricted bash | BashJail escape | bash-jail-escape.md |
| Odd encoded string | Encoding-chain decode | encoding-chain-reference.md |
| QR code / audio file | Steganography | encoding-chain-reference.md |
| Game binary / WASM | Custom-VM reversing | game-and-vm-reverse.md |
| CTFtime / CTFd platform | Platform API | ctfd-platform-guide.md |
| You were given a shell | Linux privilege escalation | linux-privesc-quick.md |
