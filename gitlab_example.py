#!/usr/bin/env python3
"""Contoh pemakaian konektor GitLab 1 (custom.gitlab) — READ-ONLY.

STATUS VERIFIKASI — JUJUR, 2026-11-07: GAGAL / BELUM TERBUKTI.
Perintah `whoami` (GET /api/v4/user ke gitlab.com) mengembalikan HTTP 403
`insufficient_granular_scope`: token yang tersimpan adalah fine-grained
personal access token TANPA permission User: Read. Identitas pemilik token
belum terbukti. JANGAN klaim konektor ini bekerja sebelum whoami berhasil.
Perbaikan: buat token baru dengan User: Read (atau scope `api`), lalu
reconnect konektor custom.gitlab.

File ini TIDAK berisi API key/token/rahasia apa pun. Semua otentikasi
dilakukan oleh helper resmi di
~/workspace/custom-connectors/custom.gitlab/bin/gitlab.py yang memakai
surrogate dari secure storage. Jalankan hanya perintah read-only di bawah.

Cara pakai:
    python3 gitlab_example.py              # whoami
    python3 gitlab_example.py projects     # daftar project yang bisa dilihat token
    python3 gitlab_example.py project <id-atau-path>   # baca satu project
    python3 gitlab_example.py search_projects perkara  # cari project
"""

import subprocess
import sys

import os

HELPER = os.environ.get("GITLAB_HELPER", "/home/hatch/workspace/custom-connectors/custom.gitlab/bin/gitlab.py")


def run(*args: str) -> int:
    """Jalankan helper gitlab.py dengan argumen read-only dan teruskan outputnya."""
    cmd = ["python3", HELPER, *args]
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, text=True)
    return result.returncode


def main() -> int:
    args = sys.argv[1:] or ["whoami"]
    allowed = {"whoami", "projects", "project", "search_projects"}
    if args[0] not in allowed:
        print(f"Perintah tidak diizinkan (hanya read-only): {args[0]}", file=sys.stderr)
        print(f"Yang diizinkan: {sorted(allowed)}", file=sys.stderr)
        return 2
    if args[0] in {"project", "search_projects"} and len(args) < 2:
        print(f"Pemakaian: {args[0]} <id/path atau kata kunci>", file=sys.stderr)
        return 2
    return run(*args)


if __name__ == "__main__":
    raise SystemExit(main())
