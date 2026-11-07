# Contoh Konektor GitLab — PERKARA AJI II

Contoh pemakaian konektor GitLab (custom.gitlab, custom.gitlab-2, custom.gitlab-3) dari workspace Muse, khusus operasi **read-only** yang aman. Repo ini bagian dari proyek PERKARA AJI II — agen AI yang membuat video YouTube 8 menit dari foto presenter.

## Isi repo

| File | Konektor | Perintah |
|---|---|---|
| `gitlab_example.py` | custom.gitlab (GitLab 1) | `whoami`, `projects`, `project`, `search_projects` |
| `gitlab2_example.py` | custom.gitlab-2 (GitLab 2) | sama seperti di atas |
| `gitlab3_example.py` | custom.gitlab-3 (GitLab 3) | sama seperti di atas |

Ketiga konektor itu adalah **satu layanan GitLab** (tiga akun/token berbeda); code contohnya masing-masing memanggil helper-nya sendiri.

## Cara pakai

```bash
python3 gitlab_example.py                    # whoami — siapa pemilik token
python3 gitlab_example.py projects           # daftar project yang bisa dilihat token
python3 gitlab_example.py project <id/path>  # baca satu project
python3 gitlab_example.py search_projects perkara  # cari project
```

Syarat: helper konektor harus ada di mesinmu, yaitu `~/workspace/custom-connectors/custom.gitlab/bin/gitlab.py` (dan `gitlab2.py` / `gitlab3.py` untuk file ke-2/ke-3). Kalau helper-mu ada di tempat lain, atur lewat environment variable:

```bash
GITLAB_HELPER=/path/ke/gitlab.py python3 gitlab_example.py
GITLAB2_HELPER=/path/ke/gitlab2.py python3 gitlab2_example.py
GITLAB3_HELPER=/path/ke/gitlab3.py python3 gitlab3_example.py
```

## Tanpa secret

File-file di repo ini **tidak berisi API key, token, atau rahasia apa pun**. Semua otentikasi dilakukan helper konektor, yang memakai surrogate dari secure storage Muse. Jangan pernah menaruh token di file, di `.env`, atau di commit.

## Status verifikasi — jujur (2026-11-07)

Semua konektor GitLab **belum terbukti bekerja** pada 2026-11-07:

- **GitLab 1:** `whoami` dijawab HTTP 403 `insufficient_granular_scope` — token fine-grained yang tersimpan tidak punya permission User: Read.
- **GitLab 2 dan 3:** `whoami` dijawab HTTP 401 — token ditolak GitLab.

Perbaikan: buat token baru dengan User: Read (atau scope `api`) untuk GitLab 1, dan token baru yang valid untuk GitLab 2/3, lalu reconnect. **Update 2026-11-07 ~03:01:** link reconnect sudah dikirim untuk semua konektor yang gagal — status di atas bisa berubah begitu reconnect diisi. Jangan klaim konektor ini bekerja sebelum `whoami` berhasil.

## Repo terkait (hasil screening)

Repo open source terbaik untuk memakai GitLab API dari code sendiri (bukan bagian repo ini, lisensinya masing-masing):

- **python-gitlab** — https://github.com/python-gitlab/python-gitlab — wrapper Python resmi-komunitas untuk GitLab API v4 + CLI, lisensi LGPL-3.0. Paling cocok untuk agen ini karena agen ditulis Python.
- **glab** — https://gitlab.com/gitlab-org/cli — CLI resmi GitLab, lisensi MIT. Berguna untuk otomasi shell/CI di VPS.
- **gitbeaker** — https://github.com/jdalrymple/gitbeaker — SDK GitLab typed untuk Node.js, lisensi MIT. Relevan bila Workflow Web (JavaScript) mau bicara ke GitLab.

## Lisensi

Code contoh di repo ini berlisensi **MIT** (lihat `LICENSE`). Dependensi/repo terkait di atas punya lisensinya sendiri-sendiri — periksa sebelum memakai.
