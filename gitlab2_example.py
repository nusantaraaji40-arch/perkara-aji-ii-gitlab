#!/usr/bin/env python3
"""Contoh pemakaian konektor GitLab 2 (custom.gitlab-2) — READ-ONLY.

STATUS VERIFIKASI — JUJUR, 2026-11-07: GAGAL / BELUM TERBUKTI.
Perintah `whoami` (GET /api/v4/user ke gitlab.com) mengembalikan HTTP 401
Unauthorized dengan body {"message": "401 Unauthorized"}. Kredensial sudah
dibawa di header PRIVATE-TOKEN, jadi token yang tersimpan DITOLAK GitLab
(hilang / salah format / dicabut / kedaluwarsa). Identitas pemilik token
belum terbukti. JANGAN klaim konektor ini bekerja sebelum whoami berhasil.
Perbaikan: buat token GitLab baru, lalu reconnect konektor custom.gitlab-2.

File ini TIDAK berisi API key/token/rahasia apa pun. Semua otentikasi
dilakukan oleh helper resmi di
~/workspace/custom-connectors/custom.gitlab-2/bin/gitlab2.py yang memakai
surrogate dari secure storage. Jalankan hanya perintah read-only di bawah.

Cara pakai:
    python3 gitlab2_example.py              # whoami
    python3 gitlab2_example.py projects     # daftar project yang bisa dilihat token
    python3 gitlab2_example.py project <id-atau-path>   # baca satu project
    python3 gitlab2_example.py search_projects perkara  # cari project
"""

import subprocess
import sys

import os

HELPER = os.environ.get("GITLAB2_HELPER", "/home/hatch/workspace/custom-connectors/custom.gitlab-2/bin/gitlab2.py")


def run(*args: str) -> int:
    """Jalankan helper gitlab2.py dengan argumen read-only dan teruskan outputnya."""
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
