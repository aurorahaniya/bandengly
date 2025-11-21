from flask import Flask, render_template_string, request, redirect, url_for, session
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import time


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL:", SUPABASE_URL)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

INDEX_WEB = """ 
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bandengly</title>

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
        body {
            margin: 0;
            font-family: "Poppins", sans-serif;
            background: #FFFDF7;
            color: #4a3b25;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        /* NAVBAR */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px 60px;
            background: linear-gradient(to right, #ffe28a, #ffd65a);
            position: sticky;
            top: 0;
            z-index: 10;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }

        .navbar .logo {
            font-size: 27px;
            font-weight: 700;
            letter-spacing: 0.5px;
            background: linear-gradient(90deg, #c59f00, #7ca300);
            -webkit-background-clip: text;
            color: transparent;
        }

        .navbar a {
            margin-left: 35px;
            text-decoration: none;
            font-weight: 600; /* lebih tegas */
            color: #4a3b25;
            letter-spacing: 0.3px;
            transition: 0.2s;
        }

        .navbar a:hover {
            color: #7ca300;
        }

        /* HERO */
        .hero {
            flex: 1;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 70px 70px;
            background: linear-gradient(to bottom right, #fff6d1, #ffefb5, #ffeaa1);
        }

        .hero-left {
            max-width: 550px;
            margin-top: -40px; 
            padding-top: 10px;
        }

        .hero-left h1 {
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 18px;
            color: #6a4d2f;
        }

        .hero-left p {
            line-height: 1.7;
            font-size: 18px;
            color: #6d5c44;
            max-width: 490px;
        }

        .btn-primary {
            margin-top: 22px;
            padding: 14px 32px;
            font-size: 17px;
            font-weight: 600;
            background: #7bb547;
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: 0.2s;
        }

        .btn-primary {
          display: inline-block;
          text-decoration: none;
          }


        .btn-primary:hover {
            background: #6aa13b;
        }

        .hero-right img {
            width: 430px;
            margin-top: -20px;
            border-radius: 20px;
            box-shadow: 0 8px 22px rgba(0,0,0,0.10);
        }

        /* FOOTER */
        .footer {
            text-align: center;
            padding: 22px;
            font-size: 14px;
            font-weight: 500;
            color: #6a5b44;
            background: #fff2c6;
            border-top: 1px solid rgba(0,0,0,0.05);
        }
    </style>
</head>

<body>

<header class="navbar">
    <div class="logo">Bandengly</div>
    <nav>
        <a href="#">Tentang</a>
        <a href="#">Fitur</a>
        <a href="#">Kontak</a>
    </nav>
</header>

<section class="hero">
    <div class="hero-left">
        <h1>Sistem Akuntansi <br> Bandengly</h1>
        <p>
            Bandengly membantu bisnis mencatat transaksi dan mengelola keuangan dengan lebih cepat dan rapi.
        </p>
        <a href="/login" class="btn-primary">Mulai dengan Email</a>
    </div>

    <div class="hero-right">
        <img src="{{ url_for('static', filename='laman.png') }}" alt="Ilustrasi">
    </div>
</section>

<footer class="footer">
    © 2025 Bandengly 
</footer>

</body>
</html>
"""

# Inisialisasi Flask
app = Flask(__name__)
app.secret_key = "BANDENGLY_123"

# Halaman utama
@app.route("/")
def index():
    return render_template_string(INDEX_WEB)

LOGIN_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login - Bandengly</title>

  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <style>
    * {
    box-sizing: border-box;}

    body {
      margin: 0;
      font-family: "Poppins", sans-serif;
      background: linear-gradient(to bottom right, #fff6d1, #ffefb5, #ffeaa1);
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      color: #4a3b25;
    }

    .login-card {
      width: 380px;
      padding: 40px 35px;
      border-radius: 20px;
      background: rgba(255, 253, 247, 0.95);
      box-shadow: 0 8px 26px rgba(0, 0, 0, 0.12);
      border: 1px solid rgba(0,0,0,0.05);
      backdrop-filter: blur(8px);
      animation: fadeIn 0.35s ease-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    h2 {
      margin: 0;
      margin-bottom: 25px;
      text-align: center;
      font-weight: 700;
      font-size: 27px;
      letter-spacing: 0.3px;
      color: #6a4d2f;
    }

    .form-label {
      display: block;
      font-weight: 600;
      margin-bottom: 6px;
      color: #6d5c44;
      font-size: 15px;
    }

    .form-control {
      width: 100%;
      padding: 12px;
      border-radius: 12px;
      border: 1.8px solid #ffd65a;
      background: #fffdf7;
      font-size: 15px;
      margin-bottom: 18px;
      transition: 0.25s;
    }

    .form-control:focus {
      border-color: #ffcc4d;
      box-shadow: 0 0 9px rgba(255, 214, 90, 0.5);
      outline: none;
    }

    .btn-login {
      width: 100%;
      padding: 13px;
      margin-top: 10px;
      font-size: 16px;
      font-weight: 600;
      background: #7bb547;
      color: white;
      border: none;
      border-radius: 12px;
      cursor: pointer;
      box-shadow: 0 5px 14px rgba(0,0,0,0.15);
      transition: 0.25s;
      letter-spacing: 0.3px;
    }

    .btn-login:hover {
      background: #6aa13b;
      transform: translateY(-1px);
    }

    .link {
      display: block;
      margin-top: 18px;
      text-align: center;
      font-size: 14px;
      color: #6a4d2f;
      text-decoration: none;
      font-weight: 500;
      transition: 0.2s;
    }

    .link:hover {
      text-decoration: underline;
      color: #7ca300;
    }
  </style>
</head>

<body>

  <div class="login-card">
    <h2>Masuk ke Bandengly</h2>

    <form method="POST" action="/login">
      <label class="form-label" for="email">Email</label>
      <input type="email" id="email" name="email" class="form-control" required>

      <label class="form-label" for="password">Password</label>
      <input type="password" id="password" name="password" class="form-control" required>

      <button type="submit" class="btn-login">Masuk</button>
    </form>

    <a href="/register" class="link">Belum punya akun? Daftar</a>
  </div>

</body>
</html>


"""

# ✅ Halaman login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            user = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            # simpan session (jangan ambil user.session!)
            session["user_email"] = email

            return redirect("/dashboard")

        except Exception as e:
            print("Login error:", e)
            return render_template_string(LOGIN_WEB, error="Login gagal! Periksa email & password.")

    return render_template_string(LOGIN_WEB)


REGISTRASI_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Daftar Akun - Bandengly</title>

  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <style>
    * {
    box-sizing: border-box;}

    body {
      margin: 0;
      font-family: "Poppins", sans-serif;
      background: linear-gradient(to bottom right, #fff6d1, #ffefb5, #ffeaa1);
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      color: #4a3b25;
    }

    .register-card {
      width: 380px;
      padding: 40px 35px;
      border-radius: 20px;
      background: rgba(255, 253, 247, 0.95);
      box-shadow: 0 8px 26px rgba(0, 0, 0, 0.12);
      border: 1px solid rgba(0,0,0,0.05);
      backdrop-filter: blur(8px);
      animation: fadeIn 0.35s ease-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    h2 {
      margin: 0;
      margin-bottom: 25px;
      text-align: center;
      font-weight: 700;
      font-size: 27px;
      letter-spacing: 0.3px;
      color: #6a4d2f;
    }

    .form-label {
      display: block;
      font-weight: 600;
      margin-bottom: 6px;
      color: #6d5c44;
      font-size: 15px;
    }

    .form-control {
      width: 100%;
      padding: 12px;
      border-radius: 12px;
      border: 1.8px solid #ffd65a;
      background: #fffdf7;
      font-size: 15px;
      margin-bottom: 18px;
      transition: 0.25s;
    }

    .form-control:focus {
      border-color: #ffcc4d;
      box-shadow: 0 0 9px rgba(255, 214, 90, 0.5);
      outline: none;
    }

    .btn-register {
      width: 100%;
      padding: 13px;
      margin-top: 10px;
      font-size: 16px;
      font-weight: 600;
      background: #7bb547;
      color: white;
      border: none;
      border-radius: 12px;
      cursor: pointer;
      box-shadow: 0 5px 14px rgba(0,0,0,0.15);
      transition: 0.25s;
      letter-spacing: 0.3px;
    }

    .btn-register:hover {
      background: #6aa13b;
      transform: translateY(-1px);
    }

    .link {
      display: block;
      margin-top: 18px;
      text-align: center;
      font-size: 14px;
      color: #6a4d2f;
      text-decoration: none;
      font-weight: 500;
      transition: 0.2s;
    }

    .link:hover {
      text-decoration: underline;
      color: #7ca300;
    }
  </style>
</head>

<body>

  <div class="register-card">
    <h2>Buat Akun Baru</h2>

    <form method="POST" action="/register">
      <label class="form-label" for="email">Email</label>
      <input type="email" class="form-control" id="email" name="email" required>

      <label class="form-label" for="password">Kata Sandi</label>
      <input type="password" class="form-control" id="password" name="password" required>

      <button type="submit" class="btn-register">Daftar</button>
    </form>

    <a href="/login" class="link">Sudah punya akun? Masuk</a>
  </div>

</body>
</html>
"""


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            # Register user ke Supabase
            user = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            return redirect("/login")  # setelah daftar, kembali ke login

        except Exception as e:
            print("🔴 ERROR:", e)  # <--- ini tampil di terminal
            return render_template_string(REGISTRASI_WEB, error="Gagal daftar! " + str(e))

    return render_template_string(REGISTRASI_WEB)


@app.route("/auth/callback")
def auth_callback():
    from flask import request

    token = request.args.get("access_token")

    if not token:
        return "Token tidak ditemukan di URL verifikasi."

    # Simpan session login
    session["access_token"] = token

    return redirect("/dashboard")
DASHBOARD_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Dashboard Bandengly</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
  :root {
    --bg1: #fff7df;
    --bg2: #ffefc2;
    --bg3: #ffe59b;

    --card-bg: rgba(255, 253, 247, 0.92);
    --border: rgba(255, 214, 90, 0.55);
    --text: #6a4d2f;

    --green: #7bb547;
    --green-hover: #6aa13b;
    --gold: #d09b3d;
  }

  body {
    margin: 0;
    font-family: "Poppins", sans-serif;
    background: linear-gradient(135deg, var(--bg1), var(--bg2), var(--bg3));
    height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .wrapper {
    width: 95%;
    max-width: 1200px;
    height: 90vh;
    background: var(--card-bg);
    border-radius: 30px;
    padding: 40px;
    border: 2px solid var(--border);
    box-shadow: 0 18px 45px rgba(0,0,0,0.12);
    backdrop-filter: blur(10px);

    display: flex;
    flex-direction: column;
  }

  h2 {
    text-align: center;
    font-weight: 700;
    color: var(--text);
    font-size: 28px;
    margin-bottom: 4px;
    letter-spacing: 0.3px;
  }

  .subtitle {
    text-align: center;
    color: #8a7a63;
    margin-bottom: 30px;
    font-size: 14px;
  }

  .grid-menu {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }

  .menu-item {
    background: #ffffff;
    border: 2px solid var(--border);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: 0.25s;

    display: flex;
    flex-direction: column;
    justify-content: center;

    font-size: 15px;
    font-weight: 600;
    color: var(--text);
  }

  .menu-item:hover {
    transform: translateY(-6px);
    background: #fffaf0;
    box-shadow: 0 12px 28px rgba(255,214,90,0.55);
  }

  .menu-icon {
    font-size: 22px;
    margin-bottom: 6px;
    color: var(--gold);
  }

  .logout-area {
    text-align: center;
    margin-top: 18px;
  }

  .logout-btn {
    background: var(--green);
    color: white;
    padding: 10px 26px;
    border-radius: 14px;
    text-decoration: none;
    font-weight: 600;
    transition: 0.25s;
    font-size: 14px;
  }

  .logout-btn:hover {
    background: var(--green-hover);
  }
</style>
</head>

<body>

<div class="wrapper">
  <h2>Selamat datang, {{ user }} 👋</h2>
  <div class="subtitle">Pilih menu untuk mulai bekerja.</div>

  <div class="grid-menu">

    <div class="menu-item" onclick="window.location.href='/neraca-saldo-awal'">
        <span class="menu-icon">📘</span>Neraca Saldo Awal
    </div>

    <div class="menu-item" onclick="window.location.href='/informasi-perusahaan'">
        <span class="menu-icon">📘</span>Informasi Perusahaan
    </div>

    <div class="menu-item" onclick="window.location.href='/transaksi'">
        <span class="menu-icon">💸</span>Input Transaksi
    </div>

    <div class="menu-item" onclick="window.location.href='/jurnal-umum'">
        <span class="menu-icon">🧾</span>Jurnal Umum
    </div>

    <div class="menu-item" onclick="window.location.href='/buku-besar'">
        <span class="menu-icon">📚</span>Buku Besar
    </div>

    <div class="menu-item" onclick="window.location.href='/neraca-saldo-sebelum-penyesuaian'">
        <span class="menu-icon">⚖️</span>Neraca Saldo Sebelum Penyesuaian
    </div>

    <div class="menu-item" onclick="window.location.href='/penyesuaian'">
        <span class="menu-icon">⚙️</span>Penyesuaian
    </div>

    <div class="menu-item" onclick="window.location.href='/neraca-lajur'">
        <span class="menu-icon">🧮</span>Neraca Lajur
    </div>

    <div class="menu-item" onclick="window.location.href='/laba-rugi'">
        <span class="menu-icon">💰</span>Laba Rugi
    </div>

    <div class="menu-item" onclick="window.location.href='/laporan-akhir'">
        <span class="menu-icon">📄</span>Laporan Akhir
    </div>

    <div class="logout-area">
        <a href="/logout" class="logout-btn">Logout</a>
    </div>
  </div>
</div>

</body>
</html>
"""






@app.route("/dashboard")
def dashboard():
    if "user_email" not in session:
        return redirect("/login")

    user_email = session.get("user_email")
    return render_template_string(DASHBOARD_WEB, user=user_email)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

daftarAkun = []
AKUN_WEB = """ 
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Neraca Saldo Awal</title>

<style>
    body {
        font-family: "Segoe UI", Arial;
        background: #FFF7D6;
        margin: 0;
        padding: 30px;
        color: #3a3a3a;
    }
    h1 { 
        font-size: 32px; 
        margin-bottom: 10px; 
        color: #D18B00;
    }
    h2 { 
        margin-top: 35px; 
        color: #B17700; 
        border-left: 6px solid #F7C948; 
        padding-left: 10px; 
    }

    .card {
        background: white;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        margin-bottom: 30px;
        border-left: 4px solid #F2B233;
    }

    input, button {
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #d9b979;
        margin-right: 8px;
        font-size: 14px;
    }

    button {
        background: #F7C948;
        border: none;
        cursor: pointer;
        color: white;
        font-weight: bold;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        background: white;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #F2B233;
    }

    th, td {
        padding: 12px;
        border: 1px solid #FCE7A6;
    }

    th {
        background: #FCEFC7;
        text-align: left;
        color: #825900;
    }

    tr:hover td {
        background: #FFF4C2;
    }

    .total-row {
        background: #FCE7A6;
        font-weight: bold;
        color: #7A5200;
    }

    .hapus-btn {
        background:#E09A00; 
        color:white; 
        padding:12px 20px; 
        border-radius:8px; 
        border:none; 
        cursor:pointer; 
        font-weight:bold;
    }
</style>
</head>

<body>

<h1>📘 Neraca Saldo Awal</h1>

<!-- Tambah Akun -->
<div class="card">
    <h2>Tambah Akun</h2>
    <form method="POST" action="{{ url_for('tambah_akun') }}">
        <input type="text" name="kode" placeholder="Kode Akun" required>
        <input type="text" name="nama" placeholder="Nama Akun" required>
        <input type="number" name="debit" placeholder="Debit" value="0">
        <input type="number" name="kredit" placeholder="Kredit" value="0">
        <button type="submit">Tambah</button>
    </form>
</div>

<!-- Tabel Akun -->
<div class="card">
    <h2>Daftar Akun</h2>
    
    <table>
        <thead>
            <tr>
                <th>No</th>
                <th>Kode Akun</th>
                <th>Nama Akun</th>
                <th>Debit</th>
                <th>Kredit</th>
            </tr>
        </thead>

        <tbody>
        {% for akun in daftarAkun %}
        <tr>
          <td>{{ akun.No }}</td>
          <td>{{ akun.Kode_Akun }}</td>
          <td>{{ akun.Nama_Akun }}</td>
          <td>Rp {{ "{:,.0f}".format(akun.Debit).replace(",", ".") }}</td>
          <td>Rp {{ "{:,.0f}".format(akun.Kredit).replace(",", ".") }}</td>
        </tr>
        {% endfor %}

        <tr class="total-row">
            <td colspan="3">TOTAL</td>
            <td>Rp {{ "{:,.0f}".format(total_debit).replace(",", ".") }}</td>
            <td>Rp {{ "{:,.0f}".format(total_kredit).replace(",", ".") }}</td>
        </tr>

        </tbody>
    </table>

<div style="display: flex; gap: 15px; align-items: center; margin-top: 20px;">

    <!-- Tombol Hapus Semua Akun (warna atas) -->
    <form action="{{ url_for('hapus_semua') }}" method="POST">
        <button type="submit">Hapus Semua</button>
    </form>



    <!-- Tombol Kembali ke Dashboard -->
    <a href="/dashboard" 
       style="background-color: #f1c232; color: white; padding: 12px 25px; border-radius: 10px; font-weight: bold; text-decoration: none; display: inline-block;">
        Kembali ke Dashboard
    </a>

</div>


</body>
</html>
"""



# ============================
#           ROUTES
# ============================

@app.route("/neraca-saldo-awal")
def daftar_akun():
    response = supabase.table("neraca_saldo_awal").select("*").execute()
    data = response.data

    # Hitung total debit & kredit
    total_debit = sum(int(row["Debit"]) for row in data)
    total_kredit = sum(int(row["Kredit"]) for row in data)

    return render_template_string(
        AKUN_WEB,
        daftarAkun=data,
        total_debit=total_debit,
        total_kredit=total_kredit
    )

@app.route("/tambah", methods=["POST"])
def tambah_akun():
    debit_raw = request.form.get("debit", "").strip()
    kredit_raw = request.form.get("kredit", "").strip()

    data = {
        "Kode_Akun": request.form["kode"],
        "Nama_Akun": request.form["nama"],
        "Debit": int(debit_raw) if debit_raw.isdigit() else 0,
        "Kredit": int(kredit_raw) if kredit_raw.isdigit() else 0
    }

    supabase.table("neraca_saldo_awal").insert(data).execute()
    return redirect(url_for("daftar_akun"))

@app.route("/hapus_semua", methods=["POST"])
def hapus_semua():
    supabase.table("neraca_saldo_awal").delete().gt("No", -1).execute()
    return redirect(url_for("daftar_akun"))




TRANSAKSI_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Input Transaksi 💸</title>

<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600&display=swap" rel="stylesheet">

<style>
    * { box-sizing: border-box; }

    body { 
        font-family: 'Fredoka', sans-serif;
        font-size: 20px;
        background: linear-gradient(to bottom, #fff9e6, #fff3c4);
        padding: 40px;
    }

    h2 { 
        text-align: center; 
        color: #6a4d2f; 
        font-weight: 700;
        margin-bottom: 25px;
    }

    .form-container {
        max-width: 700px; 
        margin: auto; 
        background: #fffdf7; 
        padding: 25px;
        border-radius: 18px; 
        border: 3px solid #f7d84b;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }

    label { 
        font-weight: 600; 
        margin-top: 15px; 
        color: #6a4d2f; 
        display: block; 
        font-size: 15px;
    }

    input {
        width: 100%; 
        padding: 11px; 
        border-radius: 12px; 
        border: 2px solid #f2d37a; 
        margin-top: 5px;
        background: #fffdf5;
    }

    input:focus {
        border-color: #f7d84b;
        outline: none;
        box-shadow: 0 0 8px rgba(247,216,75,0.5);
    }

    button {
        margin-top: 20px; 
        padding: 13px; 
        width: 100%;
        background: #f7d84b; 
        border-radius: 14px; 
        border: none;
        color: #6a4d2f; 
        font-weight: 700; 
        font-size: 15px;
        cursor: pointer;
        transition: 0.2s;
    }

    button:hover {
        background: #f4cc2b;
        transform: translateY(-1px);
    }

    .row-box {
        padding: 18px;
        margin-top: 22px;
        border: 2px solid #f1c232;
        border-radius: 14px;
        background: #fff8dc;
    }

    .del-btn {
        background: #d9534f;
        color: white;
        padding: 10px;
        border-radius: 10px; 
        cursor: pointer; 
        text-align: center; 
        width: 100%;
        margin-top: 15px;
        transition: 0.2s;
    }

    .del-btn:hover {
        background: #c64542;
    }

    .back-btn {
        background: #6a4d2f;
        color: white;
    }

    .back-btn:hover {
        background: #5c4328;
    }
</style>
</head>

<body>

<h2>Input Transaksi 💸</h2>

<div class="form-container">
<form method="POST" onsubmit="return showSuccess()">

    <label>Tanggal</label>
    <input type="date" name="tanggal" required>

    <div id="akun-container">

        <div class="row-box akun-row">
            <label>Nama Akun</label>
            <input type="text" name="nama_akun[]" required>

            <label>Ref</label>
            <input type="text" name="ref[]" required>

            <label>Debit</label>
            <input type="number" name="debit[]" value="0">

            <label>Kredit</label>
            <input type="number" name="kredit[]" value="0">

            <div class="del-btn" onclick="hapus(this)">Hapus</div>
        </div>

    </div>

    <button type="button" onclick="tambah()">+ Tambah Akun</button>
    <button type="submit">Simpan Transaksi</button>

    <button type="button" class="back-btn" onclick="window.location.href='/dashboard'">
        Kembali ke Dashboard
    </button>

</form>
</div>

<script>
function tambah() {
    let box = document.querySelector(".akun-row");
    let clone = box.cloneNode(true);
    clone.querySelectorAll("input").forEach(i => i.value = "");
    document.getElementById("akun-container").appendChild(clone);
}

function hapus(el) {
    let rows = document.querySelectorAll(".akun-row");
    if (rows.length > 1) {
        el.parentNode.remove();
    }
}

function showSuccess() {
    alert("Transaksi berhasil disimpan!");
    return true;
}
</script>

</body>
</html>
"""



@app.route("/transaksi", methods=["GET", "POST"])
def transaksi():
    if request.method == "POST":
        tanggal = request.form["tanggal"]

        # Ambil semua input
        nama_akun = request.form.getlist("nama_akun[]")
        ref = request.form.getlist("ref[]")
        debit = request.form.getlist("debit[]")
        kredit = request.form.getlist("kredit[]")

        # Buat nomor transaksi unik
        no_transaksi = f"{tanggal.replace('-', '')}-{int(time.time())}"

        # Simpan semua akun dalam satu nomor transaksi
        for i in range(len(nama_akun)):
            supabase.table("input_transaksi").insert({
                "no_transaksi": no_transaksi,
                "tanggal": tanggal,
                "nama_akun": nama_akun[i],
                "ref": ref[i],
                "debit": float(debit[i]) if debit[i] else 0,
                "kredit": float(kredit[i]) if kredit[i] else 0
            }).execute()

    # Tampilkan transaksi
    result = (
        supabase.table("input_transaksi")
        .select("*")
        .order("tanggal")
        .execute()
    )

    transaksi_list = result.data

    return render_template_string(TRANSAKSI_WEB, transaksi=transaksi_list)


JU_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Jurnal Umum</title>

<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&display=swap" rel="stylesheet">

<style>
    body { 
        font-family: 'Fredoka', sans-serif;
        background: #fff7df;
        padding: 40px;
        font-size: 18px;
    }

    h2 { 
        text-align: center; 
        color: #6a4d2f;
        font-weight: 700;
        margin-bottom: 20px;
        font-size: 32px;
    }

    table {
        margin-top: 30px; 
        width: 100%;
        border-collapse: collapse; 
        background: #fffdf7;
        border-radius: 16px;
        overflow: hidden;
        border: 3px solid #f7d84b;
        box-shadow: 0 10px 25px rgba(0,0,0,0.07);
    }

    th {
        background: #f7e4b2;
        font-family: 'Poppins', sans-serif;
        border: 2px solid #e6c985;
        padding: 12px;
        text-align: center;
        font-weight: 700;
        color: #6a4d2f;
        font-size: 17px;
    }

    td {
        border: 2px solid #e6c985;
        font-family: 'Poppins', sans-serif;
        padding: 12px;
        font-size: 16px;
        color: #4a3723;
        background: #fff9e6;;
    }

    .tanggal-cell {
        vertical-align: top;
        text-align: center;
        font-weight: 600;
    }

    .akun-debit {
        padding-left: 35px !important;
        text-align: left;
        font-weight: 600;
    }

    .akun-kredit {
        text-align: center;
        font-weight: 600;
    }

    .detail-row td {
        border-top: none !important;
    }

    .detail-last td {
        border-bottom: 2px solid #e6c985 !important;
    }

    .center { text-align: center; font-weight: 600; }

</style>
</head>

<body>

<h2>Jurnal Umum 📘</h2>


<table>
    <tr>
        <th>Tanggal</th>
        <th>Nama Akun</th>
        <th>Ref</th>
        <th>Debit</th>
        <th>Kredit</th>
    </tr>

    {% for trx_id, rows in jurnal_grouped.items() %}
    {% for idx in range(rows|length) %}
    {% set row = rows[idx] %}
    
    <tr class="
        {% if idx > 0 %} detail-row {% endif %}
        {% if idx == rows|length - 1 %} detail-last {% endif %}
    ">

        {% if idx == 0 %}
        <td class="tanggal-cell" rowspan="{{ rows|length }}">
            {{ row.tanggal }}
        </td>
        {% endif %}

        <td class="{% if row.debit > 0 %}akun-debit{% else %}akun-kredit{% endif %}">
            {{ row.nama_akun }}
        </td>

        <td class="center">{{ row.ref }}</td>

        <td class="center">
            {% if row.debit > 0 %}
                Rp {{ row.debit|rp }}
            {% endif %}
        </td>

        <td class="center">
            {% if row.kredit > 0 %}
                Rp {{ row.kredit|rp }}
            {% endif %}
        </td>

    </tr>
    {% endfor %}
{% endfor %}

<tr style="background:#fff3c4; font-weight:700;">
    <td colspan="3" style="text-align:left; padding:15px;">TOTAL</td>
    <td class="center">Rp {{ total_debit|rp }}</td>
    <td class="center">Rp {{ total_kredit|rp }}</td>
</tr>
</table>

<style>
table {
    margin-bottom: 25px; /* Biar nggak mepet tombol */
}
</style>

<!-- Tombol Kembali ke Dashboard -->
    <a href="/dashboard" 
       style="background-color: #f1c232; color: white; padding: 12px 25px; border-radius: 10px; font-weight: bold; text-decoration: none; display: inline-block;">
        Kembali ke Dashboard
    </a>
</body>
</html>
"""

@app.route("/jurnal-umum")
def jurnal_umum():
    # Ambil data dari Supabase
    result = (
        supabase.table("input_transaksi")
        .select("*")
        .order("no_transaksi, id")  
        .execute()
    )

    data = result.data

    # Grouping per transaksi
    jurnal_grouped = {}
    for r in data:
        trx = r["no_transaksi"]
        if trx not in jurnal_grouped:
            jurnal_grouped[trx] = []
        jurnal_grouped[trx].append(r)

    # Hitung total debit & kredit
    total_debit = sum(
        float(row["debit"]) 
        for rows in jurnal_grouped.values() 
        for row in rows
    )

    total_kredit = sum(
        float(row["kredit"]) 
        for rows in jurnal_grouped.values() 
        for row in rows
    )

    # Render ke HTML
    return render_template_string(
        JU_WEB,
        jurnal_grouped=jurnal_grouped,
        total_debit=total_debit,
        total_kredit=total_kredit,
    )
@app.template_filter("rp")
def format_rupiah(value):
    if not value:
        return ""
    return f"{value:,.0f}".replace(",", ".")


# =============================
#     BUKU BESAR (HTML)
# =============================
BUKU_BESAR_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Buku Besar</title>

<style>
    body {
        font-family: Poppins, sans-serif;
        background: #fff7df;
        padding: 40px;
        color: #6a4d2f;
    }

    h1 {
        text-align: center;
        margin-bottom: 30px;
        font-weight: 700;
    }

    .card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #f1d28b;
        margin-bottom: 35px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.08);
    }

    .account-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #ffe9a9;
        padding: 10px 15px;
        border-radius: 10px;
        border: 2px solid #f1d28b;
        font-size: 22px;
        font-weight: 700;
    }

    table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 15px;
    }

    th, td {
        border: 2px solid #e6c985;
        padding: 10px;
        text-align: center;
    }

    th {
        background: #f5e4b3;
        font-weight: 700;
    }

    .text-left {
        text-align: left;
        padding-left: 15px;
    }
</style>
</head>

<body>

<h1>📘 Buku Besar</h1>

{% for key, data in buku_besar.items() %}
<div class="card">

    <div class="account-title">
        {{ key }} 
        <span>{{ data.kode }}</span>
    </div>

<table>
    <tr>
        <th>Tanggal</th>
        <th>Keterangan</th>
        <th>Ref</th>
        <th>Debit</th>
        <th>Kredit</th>
        <th>Saldo</th>
    </tr>

    {% for row in data.rows %}
    <tr>
        <td>{{ row.tanggal }}</td>
        <td class="text-left">{{ row.keterangan }}</td>
        <td>{{ row.ref }}</td>

        <td>
            {% if row.debit > 0 %}
                Rp {{ '{:,.0f}'.format(row.debit).replace(',', '.') }}
            {% else %}-{% endif %}
        </td>

        <td>
            {% if row.kredit > 0 %}
                Rp {{ '{:,.0f}'.format(row.kredit).replace(',', '.') }}
            {% else %}-{% endif %}
        </td>

        <td>
            {% if row.saldo_berjalan == 0 %}
                Rp -
            {% else %}
                Rp {{ row.saldo_berjalan|rp }}
            {% endif %}
        </td>
    </tr>
    {% endfor %}
</table>

</div>
{% endfor %}

<style>
table {
    margin-bottom: 25px;
}
</style>

<a href="/dashboard" 
   style="background-color: #f1c232; color: white; padding: 12px 25px; border-radius: 10px; font-weight: bold; text-decoration: none; display: inline-block;">
    Kembali ke Dashboard
</a>

</body>
</html>
"""

@app.route("/buku-besar")
def buku_besar_page():
    # --- Ambil data saldo awal & transaksi ---
    saldo_awal = supabase.table("neraca_saldo_awal").select("*").execute().data
    transaksi = supabase.table("input_transaksi").select("*").order("tanggal").execute().data

    buku_besar = {}

    # ============================
    # 1. PROSES SALDO AWAL
    # ============================
    for row in saldo_awal:

        nama = row["Nama_Akun"].strip().title()   # NORMALISASI NAMA
        kode = row["Kode_Akun"]

        buku_besar.setdefault(nama, {
            "akun": nama,
            "kode": kode,
            "rows": [],
            "saldo": 0
        })

        debit = float(row["Debit"])
        kredit = float(row["Kredit"])

        buku_besar[nama]["saldo"] += debit - kredit

        buku_besar[nama]["rows"].append({
            "tanggal": "2024-01-12",
            "keterangan": "Saldo Awal",
            "ref": kode,
            "debit": debit,
            "kredit": kredit,
            "saldo_berjalan": buku_besar[nama]["saldo"]
        })

    # ============================
    # 2. PROSES TRANSAKSI
    # ============================
    for t in transaksi:

        nama = t["nama_akun"].strip().title()   # NORMALISASI NAMA
        kode = t["ref"]

        buku_besar.setdefault(nama, {
            "akun": nama,
            "kode": kode,
            "rows": [],
            "saldo": 0
        })

        debit = float(t["debit"])
        kredit = float(t["kredit"])

        buku_besar[nama]["saldo"] += debit - kredit

        buku_besar[nama]["rows"].append({
            "tanggal": t["tanggal"],
            "keterangan": "Jurnal Umum",
            "ref": kode,
            "debit": debit,
            "kredit": kredit,
            "saldo_berjalan": buku_besar[nama]["saldo"]
        })

    buku_besar_sorted = dict(
        sorted(buku_besar.items(), key=lambda x: x[1]["kode"])
    )

    return render_template_string(BUKU_BESAR_WEB, buku_besar=buku_besar_sorted)

NS_SBLM_PENYESUAIAN_WEB= """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Neraca Saldo Sebelum Penyesuaian</title>

<style>
    body {
        font-family: Arial, sans-serif;
        padding: 30px;
        background: #fff7df;
        color: #6a4d2f;
    }

    h2 {
        text-align: center;
        margin-bottom: 25px;
        font-weight: bold;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background: white;
    }
    th, td {
        border: 2px solid #e6c985;
        padding: 10px;
        text-align: left;   /* RATA KIRI SEMUA */
    }

    th {
        background: #f5e4b3;
        font-weight: bold;
    }

    .text-left {
        text-align: left;
        padding-left: 10px;
    }
</style>
</head>

<body>

<h2>Neraca Saldo Sebelum Penyesuaian</h2>

<table>
    <tr>
        <th>Akun</th>
        <th>Nama Akun</th>
        <th>Debit</th>
        <th>Kredit</th>
    </tr>

    {% for row in data %}
    <tr>
        <td>{{ row.kode_akun }}</td>
        <td>{{ row.nama_akun }}</td>

        <td>
            {% if row.debit %}
                Rp {{ "{:,.0f}".format(row.debit).replace(",", ".") }}
            {% endif %}
        </td>

        <td>
            {% if row.kredit %}
                Rp {{ "{:,.0f}".format(row.kredit).replace(",", ".") }}
            {% endif %}
        </td>
    </tr>
    {% endfor %}

    <tr style="background:#ffe9a9; font-weight:bold;">
        <td colspan="2">Total</td>

        <td>
            {% if total_debit %}
                Rp {{ "{:,.0f}".format(total_debit).replace(",", ".") }}
            {% endif %}
        </td>

        <td>
            {% if total_kredit %}
                Rp {{ "{:,.0f}".format(total_kredit).replace(",", ".") }}
            {% endif %}
        </td>
    </tr>
</table>

"""


@app.route("/neraca-saldo-sebelum-penyesuaian")
def neraca_saldo_awal():

    rows = supabase.table("buku_besar").select("*").order("tanggal").execute().data

    saldo = {}

    for r in rows:
        kode = r["kode_akun"]        # pastikan kolom ini ada
        nama = r["nama_akun"]
        akhir = r.get("saldo", 0)

        if kode not in saldo:
            saldo[kode] = {"nama": nama, "saldo": akhir}
        else:
            saldo[kode]["saldo"] = akhir

    final_list = []

    for kode, info in saldo.items():
        akhir = info["saldo"]

        if akhir > 0:
            debit = akhir
            kredit = 0
        else:
            debit = 0
            kredit = abs(akhir)

        final_list.append({
            "kode_akun": kode,
            "nama_akun": info["nama"],
            "debit": debit,
            "kredit": kredit
        })

    # sort berdasarkan kode akun (string atau int)
    final_list = sorted(final_list, key=lambda x: x["kode_akun"])

    total_debit = sum(i["debit"] for i in final_list)
    total_kredit = sum(i["kredit"] for i in final_list)

    return render_template_string(
        NS_SBLM_PENYESUAIAN_WEB,
        data=final_list,
        total_debit=total_debit,
        total_kredit=total_kredit
    )





# ✅ Pindah ke paling bawah
if __name__ == "__main__":
    app.run(debug=True)
