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
            min-height: 100vh;}

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px 60px;
            background: linear-gradient(to right, #ffe28a, #ffd65a);
            position: sticky;
            top: 0;
            z-index: 10;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);}

        .navbar .logo {
            font-size: 27px;
            font-weight: 700;
            letter-spacing: 0.5px;
            background: linear-gradient(90deg, #c59f00, #7ca300);
            -webkit-background-clip: text;
            color: transparent;}

        .navbar a {
            margin-left: 35px;
            text-decoration: none;
            font-weight: 600; /* lebih tegas */
            color: #4a3b25;
            letter-spacing: 0.3px;
            transition: 0.2s;}

        .navbar a:hover {
            color: #7ca300;}

        .hero {
            flex: 1;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 70px 70px;
            background: linear-gradient(to bottom right, #fff6d1, #ffefb5, #ffeaa1);}

        .hero-left {
            max-width: 550px;
            margin-top: -40px; 
            padding-top: 10px;}

        .hero-left h1 {
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 18px;
            color: #6a4d2f;}

        .hero-left p {
            line-height: 1.7;
            font-size: 18px;
            color: #6d5c44;
            max-width: 490px;}

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
            transition: 0.2s;}

        .btn-primary {
          display: inline-block;
          text-decoration: none;}


        .btn-primary:hover {
            background: #6aa13b;}

        .hero-right img {
            width: 430px;
            margin-top: -20px;
            border-radius: 20px;
            box-shadow: 0 8px 22px rgba(0,0,0,0.10);}

        .footer {
            text-align: center;
            padding: 22px;
            font-size: 14px;
            font-weight: 500;
            color: #6a5b44;
            background: #fff2c6;
            border-top: 1px solid rgba(0,0,0,0.05);}
    </style>
</head>
<body>
<header class="navbar">
    <div class="logo">Bandengly</div>
    
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
    *{box-sizing: border-box;}

    body {
      margin: 0;
      font-family: "Poppins", sans-serif;
      background: linear-gradient(to bottom right, #fff6d1, #ffefb5, #ffeaa1);
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      color: #4a3b25;}

    .login-card {
      width: 380px;
      padding: 40px 35px;
      border-radius: 20px;
      background: rgba(255, 253, 247, 0.95);
      box-shadow: 0 8px 26px rgba(0, 0, 0, 0.12);
      border: 1px solid rgba(0,0,0,0.05);
      backdrop-filter: blur(8px);
      animation: fadeIn 0.35s ease-out;}

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }}

    h2 {
      margin: 0;
      margin-bottom: 25px;
      text-align: center;
      font-weight: 700;
      font-size: 27px;
      letter-spacing: 0.3px;
      color: #6a4d2f;}

    .form-label {
      display: block;
      font-weight: 600;
      margin-bottom: 6px;
      color: #6d5c44;
      font-size: 15px;}

    .form-control {
      width: 100%;
      padding: 12px;
      border-radius: 12px;
      border: 1.8px solid #ffd65a;
      background: #fffdf7;
      font-size: 15px;
      margin-bottom: 18px;
      transition: 0.25s;}

    .form-control:focus {
      border-color: #ffcc4d;
      box-shadow: 0 0 9px rgba(255, 214, 90, 0.5);
      outline: none;}

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
      letter-spacing: 0.3px;}

    .btn-login:hover {
      background: #6aa13b;
      transform: translateY(-1px);}

    .link {
      display: block;
      margin-top: 18px;
      text-align: center;
      font-size: 14px;
      color: #6a4d2f;
      text-decoration: none;
      font-weight: 500;
      transition: 0.2s;}

    .link:hover {
      text-decoration: underline;
      color: #7ca300;}
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

# Halaman login
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
    * {box-sizing: border-box;}

    body {
      margin: 0;
      font-family: "Poppins", sans-serif;
      background: linear-gradient(to bottom right, #fff6d1, #ffefb5, #ffeaa1);
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      color: #4a3b25;}

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
    /* SUNFLOWER COLORS */
    --sun1: #FFF9E8;   /* light sunflower cream */
    --sun2: #FFE9A8;   /* soft yellow */
    --sun3: #FFD45A;   /* sunflower highlight */
    --sun4: #FFC300;   /* core sunflower */

    --card: rgba(255, 251, 238, 0.7);
    --border: rgba(255, 195, 0, 0.45);
    --text: #5A3E2B;   /* sunflower seed brown */

    --accent: #8BBE4D;  /* leaf green */
    --accent-hover: #7CAF42;
  }

  body {
    margin: 0;
    font-family: "Poppins", sans-serif;
    background: linear-gradient(125deg, var(--sun1), var(--sun2), var(--sun3));
    min-height: 100vh;

    display: flex;
    justify-content: center;
    padding: 30px;
  }

  .wrapper {
    width: 100%;
    max-width: 1250px;
    background: var(--card);
    backdrop-filter: blur(15px);
    border-radius: 35px;
    padding: 45px 50px;
    border: 2px solid var(--border);
    box-shadow: 0 25px 60px rgba(0,0,0,0.12);
    animation: fade 0.45s ease-out;
  }

  @keyframes fade {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .header-area {
    text-align: center;
    margin-bottom: 35px;
  }

  h2 {
    font-size: 30px;
    font-weight: 700;
    color: var(--text);
    margin: 0;
  }

  .subtitle {
    color: #7b6b53;
    font-size: 14px;
    margin-top: 6px;
  }

  .grid-menu {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 22px;
  }

  .menu-item {
    background: #fffdf6;
    border: 2px solid var(--border);
    border-radius: 22px;
    padding: 24px;
    text-align: center;
    cursor: pointer;
    transition: 0.3s;

    color: var(--text);
    font-weight: 600;

    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .menu-item:hover {
    transform: translateY(-7px) scale(1.03);
    background: #fff6da;
    box-shadow: 0 12px 26px rgba(255, 195, 0, 0.35);
  }

  .menu-icon {
    font-size: 30px;
    margin-bottom: 8px;
    color: var(--sun4);
  }

  .logout-container {
    text-align: center;
    margin-top: 35px;
  }

  .logout-btn {
    background: var(--accent);
    color: white;
    padding: 12px 32px;
    border-radius: 16px;
    font-weight: 600;
    font-size: 15px;
    text-decoration: none;
    transition: 0.25s;
  }

  .logout-btn:hover {
    background: var(--accent-hover);
  }
</style>
</head>

<body>

<div class="wrapper">

  <div class="header-area">
      <h2>Selamat datang, {{ user }} 🌻</h2>
      <div class="subtitle">Pilih menu untuk mulai bekerja</div>
  </div>

  <div class="grid-menu">

    <div class="menu-item" onclick="location.href='/neraca-saldo-awal'">
      <span class="menu-icon">📘</span>Neraca Saldo Awal
    </div>

    <div class="menu-item" onclick="location.href='/informasi-perusahaan'">
      <span class="menu-icon">🏢</span>Informasi Perusahaan
    </div>

    <div class="menu-item" onclick="location.href='/transaksi'">
      <span class="menu-icon">💸</span>Input Transaksi
    </div>

    <div class="menu-item" onclick="location.href='/jurnal-umum'">
      <span class="menu-icon">🧾</span>Jurnal Umum
    </div>

    <div class="menu-item" onclick="location.href='/buku-besar'">
      <span class="menu-icon">📚</span>Buku Besar
    </div>

    <div class="menu-item" onclick="location.href='/neraca-saldo-sebelum-penyesuaian'">
      <span class="menu-icon">⚖️</span>Neraca Saldo Sebelum Penyesuaian
    </div>

    <div class="menu-item" onclick="location.href='/penyesuaian'">
      <span class="menu-icon">⚙️</span>Penyesuaian
    </div>

    <div class="menu-item" onclick="location.href='/neraca-saldo-setelah-penyesuaian'">
      <span class="menu-icon">🧮</span>Neraca Saldo Setelah Penyesuaian
    </div>

    <div class="menu-item" onclick="location.href='/neraca-lajur'">
      <span class="menu-icon">🗂️</span>Neraca Lajur
    </div>

    <div class="menu-item" onclick="location.href='/laporan-keuangan'">
      <span class="menu-icon">💰</span>Laporan Keuangan
    </div>

    <div class="menu-item" onclick="location.href='/jurnal-penutup'">
      <span class="menu-icon">📄</span>Jurnal Penutup
    </div>

    <div class="menu-item" onclick="location.href='/neraca-saldo-setelah-penutupan'">
      <span class="menu-icon">📑</span>Neraca Saldo Setelah Penutup
    </div>

  </div>

  <div class="logout-container">
    <a href="/logout" class="logout-btn">Logout</a>
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

<div class="card">
    <h2>Daftar Akun</h2>
    
    <table>
        <tr>
            <th>No</th>
            <th>Kode Akun</th>
            <th>Nama Akun</th>
            <th>Debit</th>
            <th>Kredit</th>
        </tr>

        {% for akun in daftarAkun %}
        <tr>
            <td>{{ akun.No }}</td>

            <td>{{ akun.Kode_Akun }}</td>

            <td>{{ akun.Nama_Akun }}</td>


            <td>
                {% if akun.Debit %}
                    Rp {{ "{:,.0f}".format(akun.Debit).replace(",", ".") }}
                {% endif %}
            </td>

            <td>
                {% if akun.Kredit %}
                    Rp {{ "{:,.0f}".format(akun.Kredit).replace(",", ".") }}
                {% endif %}
            </td>
        </tr>
        {% endfor %}

       
        <tr class="total-row">
            <td colspan="3" style="text-align:left;">TOTAL</td>

            <td style="border:1px solid #FCE7A6;">
                {% if total_debit %}
                    Rp {{ "{:,.0f}".format(total_debit).replace(",", ".") }}
                {% endif %}
            </td>

            <td style="border:1px solid #FCE7A6;">
                {% if total_kredit %}
                    Rp {{ "{:,.0f}".format(total_kredit).replace(",", ".") }}
                {% endif %}
            </td>
        </tr>
</table>
<div class="card" style="margin-top: 40px; padding: 18px;">
    <h2>Edit Akun</h2>

    <form method="POST" action="/update-akun" style="display:flex; gap:10px; flex-wrap:wrap;">

        <input type="number" name="no" placeholder="No Akun (ID)" required>
        <input type="text" name="kode_akun" placeholder="Kode Akun Baru" required>
        <input type="text" name="nama_akun" placeholder="Nama Akun Baru" required>
        <input type="number" name="debit" placeholder="Debit Baru">
        <input type="number" name="kredit" placeholder="Kredit Baru">

        <button type="submit" 
            style="background:#f1c232; color:white; font-weight:bold;">
            Simpan
        </button>

    </form>
</div>

<div style="display: flex; gap: 15px; align-items: center; margin-top: 20px;">
    <form action="{{ url_for('hapus_semua') }}" method="POST">
        <button type="submit">Hapus Semua</button>
    </form>

    <a href="/dashboard" 
       style="background-color: #f1c232; color: white; padding: 12px 25px; 
              border-radius: 10px; font-weight: bold; text-decoration: none;">
        Kembali ke Dashboard
    </a>
</div>
</body>
</html>
"""

@app.route("/neraca-saldo-awal")
def daftar_akun():
    response = supabase.table("neraca_saldo_awal").select("*").order("Kode_Akun").execute()
    data = response.data

    total_debit = sum(int(row["Debit"] or 0) for row in data)
    total_kredit = sum(int(row["Kredit"] or 0) for row in data)

    return render_template_string(
        AKUN_WEB,
        daftarAkun=data,
        total_debit=total_debit,
        total_kredit=total_kredit,
        akun_edit=None
    )


@app.route("/tambah", methods=["POST"])
def tambah_akun():
    debit_raw = request.form.get("debit", "").strip()
    kredit_raw = request.form.get("kredit", "").strip()

    data = {
        "Kode_Akun": request.form["kode"],
        "Nama_Akun": request.form["nama"],
        "Debit": int(debit_raw or 0),
        "Kredit": int(kredit_raw or 0)
    }

    supabase.table("neraca_saldo_awal").insert(data).execute()
    return redirect("/neraca-saldo-awal")


@app.route("/update-akun", methods=["POST"])
def update_akun():
    no = request.form["no"]

    data = {
        "Kode_Akun": request.form["kode_akun"],
        "Nama_Akun": request.form["nama_akun"],
        "Debit": request.form["debit"] or None,
        "Kredit": request.form["kredit"] or None
    }

    supabase.table("neraca_saldo_awal").update(data).eq("No", no).execute()
    
    return redirect("/neraca-saldo-awal")


@app.route("/hapus_semua", methods=["POST"])
def hapus_semua():
    supabase.table("neraca_saldo_awal").delete().gt("No", -1).execute()
    return redirect("/neraca-saldo-awal")

def rupiah(x):
    if x is None:
        return "-"
    try:
        x = float(x)
        x = int(x)
        return "Rp {:,}".format(x).replace(",", ".")
    except:
        return x
INFORMASI_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Informasi Perusahaan</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #FFFCE7;
            padding: 20px;
        }

        h1, h2 {
            color: #DAA520;
            border-left: 6px solid #DAA520;
            padding-left: 10px;
        }

        select, input, button {
            padding: 7px 10px;
            margin: 5px 0;
            border-radius: 6px;
            border: 1px solid #DAA520;
        }

        button {
            background: #DAA520;
            color: white;
            font-weight: bold;
            cursor: pointer;
            width: 120px;
        }

        table {
            width: 95%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 16px;
            color:#614924;
            margin: 0 auto;
        }

        th {
            background: #FAE7A5;
            padding: 12px;
            text-align: center;
            font-weight: bold;
            border-left: 2px solid #f7ee6a;
            border-right: 2px solid #f7ee6a;
            border-bottom: 2px solid #f7ee6a;
            color: #614924;
        }

        td {
            padding: 10px;
            border-left: 2px solid #f7ee6a;
            border-right: 2px solid #f7ee6a;
            border-bottom: 2px solid #f7ee6a;
            background: #fcfbe1;
            color: #614924,
        }

        tr:hover {
            background: #FFF6D0;
        }

        .form-box {
            background: #FFF7D1;
            padding: 20px;
            border-radius: 12px;
            border: 2px solid #F3D47A;
            width: 95%;
        }

        .form-row {
            display: flex;
            flex-direction: row;
            align-items: center;
            margin-bottom: 12px;
            width: 100%;
        }

        .form-row label {
            width: 200px;
            font-weight: bold;
            color: #C29018;
            font-size: 15px;
        }

        .form-row input {
            flex: 1;
        }
    </style>

</head>
<body>

<h1>Informasi Perusahaan</h1>

<form method="POST">
    <input type="hidden" name="aksi" value="pilih-kategori">
    <select name="kategori" onchange="this.form.submit()">
        <option value="">-- Pilih Kategori --</option>
        <option value="aset" {% if kategori=='aset' %}selected{% endif %}>Aset Tetap</option>
        <option value="ikan" {% if kategori=='ikan' %}selected{% endif %}>Persediaan Ikan</option>
    </select>
</form>

{% if kategori == 'aset' %}
<h3>Input Aset Tetap</h3>
<div class="form-box">
<form method="POST">
    <input type="hidden" name="aksi" value="simpan-aset">
    <input type="hidden" name="kategori" value="aset">

    <div class="form-row">
        <label>Jenis Aset:</label>
        <input name="jenis">
    </div>

    <div class="form-row">
        <label>Tanggal:</label>
        <input type="date" name="tanggal">
    </div>

    <div class="form-row">
        <label>Harga:</label>
        <input name="harga">
    </div>

    <div class="form-row">
        <label>Nilai Sisa:</label>
        <input name="nilai_sisa">
    </div>

    <div class="form-row">
        <label>Umur (tahun):</label>
        <input name="umur">
    </div>

    <button>Simpan</button>
</form>
</div>
{% endif %}

{% if kategori == 'ikan' %}
<h3>Input Persediaan Ikan</h3>
<div class="form-box">
<form method="POST">
    <input type="hidden" name="aksi" value="simpan-ikan">
    <input type="hidden" name="kategori" value="ikan">

    <div class="form-row">
        <label>Nama:</label>
        <input name="nama">
    </div>

    <div class="form-row">
        <label>Qty (kg):</label>
        <input name="qty">
    </div>

    <div class="form-row">
        <label>Harga per kg:</label>
        <input name="harga">
    </div>

    <div class="form-row">
        <label>Harga jual per kg:</label>
        <input name="jual">
    </div>

    <button>Simpan</button>
</form>
</div>
{% endif %}


<h2>Aset Tetap</h2>
<table>
    <tr>
        <th>Jenis Aset</th><th>Tanggal Perolehan</th><th>Harga Perolehan</th><th>Nilai Sisa</th><th>Umur</th>
    </tr>
    {% for a in aset %}
    <tr>
        <td>{{a.jenis}}</td>
        <td>{{a.tanggal}}</td>
        <td>{{a.harga}}</td>
        <td>{{a.nilai_sisa}}</td>
        <td>{{a.umur}}</td>
    </tr>
    {% endfor %}
</table>

<h2>Persediaan Ikan</h2>
<table>
    <tr><th>Nama Ikan</th><th>Qty</th><th>Harga Per Kg</th><th>Harga Jual</th><th>Total</th></tr>
    {% for i in ikan %}
    <tr>
        <td>{{i.nama}}</td>
        <td>{{i.qty}}</td>
        <td>{{i.harga}}</td>
        <td>{{i.jual}}</td>
        <td>{{i.total}}</td>
    </tr>
    {% endfor %}
</table>

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

@app.route("/informasi-perusahaan", methods=["GET", "POST"])
def informasi():

    def to_float(x):
        return float(x.replace(".", "").replace(",", "."))

    aksi = request.form.get("aksi", "")
    kategori = request.form.get("kategori") if aksi == "pilih-kategori" else request.form.get("kategori", "")

    # ---------------------- SIMPAN ASET
    if aksi == "simpan-aset":
        supabase.table("aset_tetap").insert({
            "jenis": request.form["jenis"],
            "tanggal": request.form["tanggal"],
            "harga": to_float(request.form["harga"]),
            "nilai_sisa": float(request.form["nilai_sisa"]),   # TANPA RP
            "umur": float(request.form["umur"])
        }).execute()
        kategori = "aset"

    # ---------------------- SIMPAN IKAN
    if aksi == "simpan-ikan":
        qty = to_float(request.form["qty"])
        harga = to_float(request.form["harga"])  # harga per kg
        jual = to_float(request.form["jual"])    # harga jual per kg

        supabase.table("persediaan_ikan").insert({
            "nama": request.form["nama"],
            "qty": qty,
            "harga_perkg": harga,      # ✅ sesuai tabel
            "harga_jual": jual,        # ✅ sesuai tabel
            "total": qty * harga       # total = qty × harga per kg
        }).execute()

        kategori = "ikan"



    # ---------------------- GET DATA
    aset_raw = supabase.table("aset_tetap").select("*").execute().data
    ikan_raw = supabase.table("persediaan_ikan").select("*").execute().data
    

    def rp(x):
        return f"Rp {x:,.0f}".replace(",", ".")

    aset = []
    for a in aset_raw:
        a["harga"] = rp(a["harga"])
        a["nilai_sisa"] = f"{a['nilai_sisa']:,.0f}".replace(",", ".") 
        a["umur"] = int(a["umur"])   # TANPA RP
        aset.append(a)

    ikan = []
    for i in ikan_raw:
        i["qty"] = int(i["qty"])
        i["harga"] = rp(i["harga_perkg"])     # Harga kolom kiri
        i["jual"] = rp(i["harga_jual"])       # Harga Jual kolom kanan
        i["total"] = rp(i["total"])
        ikan.append(i)


    return render_template_string(
        INFORMASI_WEB,
        kategori=kategori,
        aset=aset,
        ikan=ikan,
    )





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
    .total-row td {
        background: #f7e4b2;
        font-weight: bold;
        border-top: 2px solid #edf553;
        border-bottom: 2px solid #edf553;
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

<<tr class="total-row">
    <td colspan="3" style="text-align:left; padding:15px;">TOTAL</td>
    <td class="center">Rp {{ total_debit|rp }}</td>
    <td class="center">Rp {{ total_kredit|rp }}</td>
</tr>
</table>


</div>

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

{% for akun, data in buku_besar.items() %}
<div class="card">

    <!-- Judul Akun -->
    <div class="account-title">
        {{ akun }}
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
            {% if row.saldo == 0 %}
                Rp -
            {% else %}
                Rp {{ '{:,.0f}'.format(row.saldo).replace(',', '.') }}
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
    saldo_awal = supabase.table("neraca_saldo_awal").select("*").execute().data
    transaksi = supabase.table("input_transaksi").select("*").order("tanggal").execute().data
    penyesuaian = supabase.table("jurnal_penyesuaian").select("*").order("tanggal").execute().data
    penutup = supabase.table("jurnal_penutup").select("*").order("tanggal").execute().data



    buku_besar = {}

    # --- Normalisasi nama akun ---
    def fix(n):
        return n.strip().lower() if n else ""

    def get_nama(row):
        return (row.get("nama_akun") or row.get("Nama_Akun") or row.get("akun") or "").strip()

    # ===============================
    # SALDO AWAL
    # ===============================
    for row in saldo_awal:
        nama_asli = get_nama(row)
        nama_key = fix(nama_asli)
        kode = row.get("ref") or row.get("Kode_Akun")

        if nama_key not in buku_besar:
            buku_besar[nama_key] = {"nama": nama_asli, "kode": kode, "rows": []}

        buku_besar[nama_key]["rows"].append({
            "tanggal": "2024-12-01",
            "keterangan": "Saldo Awal",
            "ref": kode,
            "debit": float(row.get("debit") or row.get("Debit") or 0),
            "kredit": float(row.get("kredit") or row.get("Kredit") or 0)
        })

    # ===============================
    # TRANSAKSI / JURNAL UMUM
    # ===============================
    for t in transaksi:
        nama_asli = get_nama(t)
        nama_key = fix(nama_asli)
        kode = t["ref"]

        if nama_key not in buku_besar:
            buku_besar[nama_key] = {"nama": nama_asli, "kode": kode, "rows": []}

        buku_besar[nama_key]["rows"].append({
            "tanggal": t["tanggal"],
            "keterangan": t.get("keterangan", "Jurnal Umum"),
            "ref": kode,
            "debit": float(t["debit"] or 0),
            "kredit": float(t["kredit"] or 0)
        })

    # ===============================
    # JURNAL PENYESUAIAN
    # ===============================
    for p in penyesuaian:
        nama_asli = get_nama(p)
        nama_key = fix(nama_asli)
        kode = p["kode_akun"]

        if nama_key not in buku_besar:
            buku_besar[nama_key] = {"nama": nama_asli, "kode_akun": kode, "rows": []}

        buku_besar[nama_key]["rows"].append({
            "tanggal": p["tanggal"],
            "keterangan": "Penyesuaian",
            "kode_akun": kode,
            "debit": float(p["debit"] or 0),
            "kredit": float(p["kredit"] or 0)
        })
    
    for jp in penutup:
        nama_asli = get_nama(jp)
        nama_key = fix(nama_asli)
        kode = jp["ref"]

        if nama_key not in buku_besar:
            buku_besar[nama_key] = {"nama": nama_asli, "kode": kode, "rows": []}

        buku_besar[nama_key]["rows"].append({
            "tanggal": jp["tanggal"],
            "keterangan": "Penutup",
            "ref": kode,
            "debit": float(jp["debit"] or 0),
            "kredit": float(jp["kredit"] or 0)
        })

    
    for key, akun in buku_besar.items():
        saldo = 0
        for row in akun["rows"]:
            saldo += row["debit"] - row["kredit"]
            row["saldo"] = saldo

   
    buku_besar_sorted = dict(
        sorted(buku_besar.items(), key=lambda x: x[1]["kode"])
    )

    final_data = {
        akun_data["nama"]: {
            "kode": akun_data["kode"],
            "rows": akun_data["rows"]
        }
        for akun_data in buku_besar_sorted.values()
    }

    return render_template_string(BUKU_BESAR_WEB, buku_besar=final_data)






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
        text-align: left;
    }

    th {
        background: #f5e4b3;
        font-weight: bold;
    }

    .text-left {
        text-align: left;
        padding-left: 10px;
    }

    .button-bottom {
    margin-top: 30px;
    display: flex;
    gap: 12px;        /* jarak antar tombol */
    align-items: center;
    }

    .btn-kembali, .btn-simpan {
        background: #d4a842;
        padding: 12px 28px;
        border-radius: 10px;
        font-weight: bold;
        color: white;
        border: none;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: 0.2s;
    }

    .btn-kembali:hover, .btn-simpan:hover {
        background: #bf922d;
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

<div class="button-bottom">
    <a href="/dashboard" class="btn-kembali">Kembali ke Dashboard</a>

    <form action="/neraca-saldo-sebelum-penyesuaian" method="post">
        <button type="submit" class="btn-simpan">Simpan Neraca Saldo</button>
    </form>
</div>


</body>
</html>
"""

@app.route("/neraca-saldo-sebelum-penyesuaian", methods=["GET", "POST"])
def neraca_saldo_sebelum_penyesuaian():

    
    if request.method == "POST":

        
        saldo_awal = supabase.table("neraca_saldo_awal").select("*").execute().data
        transaksi = supabase.table("input_transaksi").select("*").execute().data

        saldo = {}

        
        for r in saldo_awal:
            kode = r["Kode_Akun"]
            nama = r["Nama_Akun"]
            debit = float(r["Debit"] or 0)
            kredit = float(r["Kredit"] or 0)

            saldo[kode] = {
                "nama": nama,
                "saldo": debit - kredit
            }

    
        for t in transaksi:
            kode = t["ref"]
            debit = float(t["debit"] or 0)
            kredit = float(t["kredit"] or 0)

            saldo.setdefault(kode, {
                "nama": t["nama_akun"],
                "saldo": 0
            })

            saldo[kode]["saldo"] += debit - kredit

        
        final_list = [{
            "kode_akun": k,
            "nama_akun": v["nama"],
            "debit": v["saldo"] if v["saldo"] > 0 else 0,
            "kredit": abs(v["saldo"]) if v["saldo"] < 0 else 0
        } for k, v in saldo.items()]

        
        supabase.table("neraca_saldo_sebelum_penyesuaian").delete().neq("kode_akun", "").execute()
        supabase.table("neraca_saldo_sebelum_penyesuaian").insert(final_list).execute()

        return redirect("/neraca-saldo-sebelum-penyesuaian")



   
    #  TAMPILKAN HALAMAN
    saldo_awal = supabase.table("neraca_saldo_awal").select("*").execute().data
    transaksi = supabase.table("input_transaksi").select("*").execute().data

    saldo = {}

   
    for r in saldo_awal:
        kode = r["Kode_Akun"]
        nama = r["Nama_Akun"]
        debit = float(r["Debit"] or 0)
        kredit = float(r["Kredit"] or 0)

        saldo[kode] = {
            "nama": nama,
            "saldo": debit - kredit
        }

    
    for t in transaksi:
        kode = t["ref"]
        debit = float(t["debit"] or 0)
        kredit = float(t["kredit"] or 0)

        saldo.setdefault(kode, {
            "nama": t["nama_akun"],
            "saldo": 0
        })

        saldo[kode]["saldo"] += debit - kredit

    
    final_list = [{
        "kode_akun": k,
        "nama_akun": v["nama"],
        "debit": v["saldo"] if v["saldo"] > 0 else 0,
        "kredit": abs(v["saldo"]) if v["saldo"] < 0 else 0
    } for k, v in saldo.items()]

    
    final_list = sorted(final_list, key=lambda x: x["kode_akun"])

    
    total_debit = sum(i["debit"] for i in final_list)
    total_kredit = sum(i["kredit"] for i in final_list)

    return render_template_string(
        NS_SBLM_PENYESUAIAN_WEB,
        data=final_list,
        total_debit=total_debit,
        total_kredit=total_kredit
    )
PENYESUAIAN_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Jurnal Penyesuaian</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #FFFCE7;
            padding: 25px;
        }

        h1 {
            color: #DAA520;
            border-left: 6px solid #DAA520;
            padding-left: 12px;
            margin-bottom: 20px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }

        .row {
            display: flex;
            gap: 12px;
            margin-bottom: 10px;
        }

        input {
            padding: 10px;
            border: 1px solid #C9A86A;
            border-radius: 10px;
            font-size: 14px;
        }

        .mid   { width: 220px; }
        .small { width: 90px; }

        button {
            padding: 10px 16px;
            background: #F4C430;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            color: white;
        }

        .add-btn {
            background: #4CAF50;
            margin-top: 10px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 16px;
        }

        th {
            background: #FAE7A5;
            padding: 12px;
            text-align: center;
            font-weight: bold;
        }

        td {
            padding: 10px;
            border-bottom: 1px solid #eee;
        }

        .tanggal-cell {
            vertical-align: top;
            text-align: center;
            font-weight: 600;
            width: 110px;
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

        .center {
            text-align: center;
            font-weight: 600;
        }
    </style>
</head>

<body>

<h1>📘 Jurnal Penyesuaian</h1>
<div class="card">
    <h2 style="color:#DAA520;">Tambah Jurnal Penyesuaian</h2>

    <form method="POST" action="/penyesuaian">

        <div class="row">
            <input type="date" name="tanggal" required>
        </div>

        <div id="input-area">
            <div class="row">
                <input type="text"   name="nama_akun[]" class="mid" placeholder="Nama Akun" required>
                <input type="text"   name="kode_akun[]" class="small" placeholder="Ref">
                <input type="number" name="debit[]" class="small" placeholder="Debit">
                <input type="number" name="kredit[]" class="small" placeholder="Kredit">
            </div>
        </div>

        <button type="button" class="add-btn" onclick="addRow()">+ Tambah Baris</button>
        <button type="submit">Simpan</button>
    </form>
</div>

<div class="card">
    <h2 style="color:#DAA520;">Daftar Jurnal Penyesuaian</h2>

<table>
    <tr>
        <th>Tanggal</th>
        <th>Nama Akun</th>
        <th>Ref</th>
        <th>Debit</th>
        <th>Kredit</th>
    </tr>

    {# GROUPING PER TANGGAL #}
    {% set grouped = {} %}

    {% for r in penyesuaian_entries %}
        {% if r.tanggal not in grouped %}
            {% set _ = grouped.update({ r.tanggal: [] }) %}
        {% endif %}
        {% set _ = grouped[r.tanggal].append(r) %}
    {% endfor %}

    {# TAMPILKAN PER TANGGAL #}
    {% for tanggal, rows in grouped.items() %}
        {% for i in range(rows|length) %}
            {% set row = rows[i] %}
            <tr>

                {# TANGGAL muncul sekali saja #}
                {% if i == 0 %}
                <td class="tanggal-cell" rowspan="{{ rows|length }}">
                    {{ tanggal }}
                </td>
                {% endif %}

                {# NAMA AKUN: debit kiri, kredit kanan #}
                <td class="{% if row.debit > 0 %}akun-debit{% else %}akun-kredit{% endif %}">
                    {{ row.nama_akun }}
                </td>

                <td class="center">{{ row.kode_akun or "" }}</td>

                <td class="center">
                    {% if row.debit > 0 %}
                        Rp {{ "{:,.0f}".format(row.debit) }}
                    {% endif %}
                </td>

                <td class="center">
                    {% if row.kredit > 0 %}
                        Rp {{ "{:,.0f}".format(row.kredit) }}
                    {% endif %}
                </td>
            </tr>
        {% endfor %}
    {% endfor %}

    <tr style="background:#fff3c4; font-weight:700;">
        <td colspan="3" style="text-align:left; padding:15px;">TOTAL</td>
        <td class="center">Rp {{ "{:,.0f}".format(total_debit) }}</td>
        <td class="center">Rp {{ "{:,.0f}".format(total_kredit) }}</td>
    </tr>
</table>
<style>
table {
    margin-bottom: 25px;
}
</style>

<a href="/dashboard" 
   style="background-color: #f1c232; color: white; padding: 12px 25px; border-radius: 10px; font-weight: bold; text-decoration: none; display: inline-block;">
    Kembali ke Dashboard
</a>

</div>

<script>
function addRow() {
    let div = document.createElement("div");
    div.className = "row";

    div.innerHTML = `
        <input type="text"   name="nama_akun[]" class="mid" placeholder="Nama Akun" required>
        <input type="text"   name="kode_akun[]" class="small" placeholder="Ref">
        <input type="number" name="debit[]" class="small" placeholder="Debit">
        <input type="number" name="kredit[]" class="small" placeholder="Kredit">
    `;

    document.getElementById("input-area").appendChild(div);
}
</script>

</body>
</html>
"""

@app.route("/penyesuaian", methods=["GET", "POST"])
def jurnal_penyesuaian():
    if request.method == "POST":
        tanggal = request.form.get("tanggal")
        nama_akun = request.form.getlist("nama_akun[]")
        kode_akun = request.form.getlist("kode_akun[]")
        debit = request.form.getlist("debit[]")
        kredit = request.form.getlist("kredit[]")

        for i in range(len(nama_akun)):
            if not nama_akun[i].strip():
                continue

            d = float(debit[i]) if debit[i] else 0
            k = float(kredit[i]) if kredit[i] else 0

            supabase.table("jurnal_penyesuaian").insert({
                "tanggal": tanggal,
                "nama_akun": nama_akun[i],
                "kode_akun": kode_akun[i] if i < len(kode_akun) else None,
                "debit": d,
                "kredit": k,
            }).execute()

    # Load data
    data = (
        supabase.table("jurnal_penyesuaian")
        .select("*")
        .order("tanggal")
        .execute()
        .data
    )

    total_debit = sum(x["debit"] for x in data)
    total_kredit = sum(x["kredit"] for x in data)

    return render_template_string(
        PENYESUAIAN_WEB,
        penyesuaian_entries=data,
        total_debit=total_debit,
        total_kredit=total_kredit,
    )



NERACA_SESUDAH_PENYESUAIAN_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Neraca Saldo Setelah Penyesuaian</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #FFFBE9;
            margin: 0;
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: #B6862E;
            margin-bottom: 30px;
        }

        
        table {
            width: 80%;
            border-collapse: collapse;
            margin: 0 auto 40px auto;
            margin-bottom: 40px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        th, td {
            border: 1px solid #E0D5B5;   /* 🔥 garis tabel */
        }

        th {
            background: #F3E2B3;
            padding: 12px;
            text-align: center;
            color: #5A4500;
            font-size: 16px;
        }

        td {
            padding: 10px 12px;
            font-size: 15px;
            text-align: left;             /* 🔥 saldo rata kiri */
            white-space: nowrap;
        }

        .total-row {
            background: #FFF4D0;
            font-weight: bold;
        }
        .button-row {
            margin-top: 20px;
            display: flex;
            gap: 20px;       /* jarak antar tombol */
            align-items: center;
        }
        
        .btn-kembali,
        .btn-simpan {
            background-color: #f1c232;
            color: white;
            padding: 12px 25px;
            border-radius: 10px;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
            border: none;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 3px 5px rgba(0,0,0,0.2);
        }

        .btn-simpan:hover,
        .btn-kembali:hover {
            background-color: #d4a62a;
        }

        

    </style>

</head>

<body>

<h1>Neraca Saldo Setelah Penyesuaian</h1>

<table>
    <thead>
        <tr>
            <th>Kode Akun</th>
            <th>Nama Akun</th>
            <th>Debit</th>
            <th>Kredit</th>
        </tr>
    </thead>

    <tbody>

        {% for kode, a in akun.items() %}
        <tr>
            <td>{{ kode }}</td>
            <td>{{ a.nama }}</td>

            <td class="num">
                {% if a.debit > 0 %}
                    Rp {{ "{:,.0f}".format(a.debit).replace(",", ".") }}
                {% endif %}
            </td>

            <td class="num">
                {% if a.kredit > 0 %}
                    Rp {{ "{:,.0f}".format(a.kredit).replace(",", ".") }}
                {% endif %}
            </td>
        </tr>
        {% endfor %}

        <tr class="total-row">
            <td colspan="2">TOTAL</td>

            <td class="num">
                {% if total_debit > 0 %}
                    Rp {{ "{:,.0f}".format(total_debit).replace(",", ".") }}
                {% endif %}
            </td>

            <td class="num">
                {% if total_kredit > 0 %}
                    Rp {{ "{:,.0f}".format(total_kredit).replace(",", ".") }}
                {% endif %}
            </td>
        </tr>

    </tbody>
</table>
<div class="button-row">
    <a href="/dashboard" class="btn-kembali">Kembali ke Dashboard</a>
    <form method="POST" action="/neraca-saldo-setelah-penyesuaian" style="display:inline;">
        <button type="submit" class="btn-simpan">Simpan Neraca Setelah Penyesuaian</button>
    </form>
</div>
</body>
</html>
"""

@app.route("/neraca-saldo-setelah-penyesuaian", methods=["GET", "POST"])
def neraca_saldo_setelah_penyesuaian():

    saldo_awal = supabase.table("neraca_saldo_awal").select("*").execute().data
    transaksi = supabase.table("input_transaksi").select("*").order("tanggal").execute().data
    penyesuaian = supabase.table("jurnal_penyesuaian").select("*").order("tanggal").execute().data

    akun_dict = {}

    def get_nama(row):
        return (
            row.get("nama_akun")
            or row.get("Nama_Akun")
            or row.get("akun")
            or "Tidak diketahui"
        )

    def add(kode, nama, d, k):
        kode = str(kode)
        if kode not in akun_dict:
            akun_dict[kode] = {"nama": nama, "debit": 0, "kredit": 0}
        akun_dict[kode]["debit"] += d
        akun_dict[kode]["kredit"] += k

    for s in saldo_awal:
        add(
            s.get("ref") or s.get("Kode_Akun"),
            get_nama(s),
            float(s.get("debit") or s.get("Debit") or 0),
            float(s.get("kredit") or s.get("Kredit") or 0)
        )

  
    for t in transaksi:
        add(
            t["ref"],
            get_nama(t),
            float(t.get("debit") or 0),
            float(t.get("kredit") or 0)
        )

   
    for p in penyesuaian:
        add(
            p["kode_akun"],
            get_nama(p),
            float(p.get("debit") or 0),
            float(p.get("kredit") or 0)
        )


    akun_final = {}

    for kode, val in akun_dict.items():
        nama = val["nama"]
        debit = val["debit"]
        kredit = val["kredit"]

        selisih = debit - kredit

        if selisih > 0:
            d = selisih
            k = 0
        elif selisih < 0:
            d = 0
            k = abs(selisih)
        else:
            d = 0
            k = 0

        akun_final[kode] = {
            "nama": nama,
            "debit": d,
            "kredit": k
        }

    akun_sorted = dict(sorted(akun_final.items(), key=lambda x: x[0]))

    total_debit = sum(v["debit"] for v in akun_sorted.values())
    total_kredit = sum(v["kredit"] for v in akun_sorted.values())
    if request.method == "POST":

        rows = []
        for kode, a in akun_sorted.items():
            rows.append({
                "kode_akun": kode,
                "nama_akun": a["nama"],
                "debit": a["debit"],
                "kredit": a["kredit"],
            })

        supabase.table("neraca_setelah_penyesuaian").delete().neq("kode_akun", "").execute()

       
        supabase.table("neraca_setelah_penyesuaian").insert(rows).execute()

        return redirect("/neraca-saldo-setelah-penyesuaian")

    # ================================


    return render_template_string(
        NERACA_SESUDAH_PENYESUAIAN_WEB,
        akun=akun_sorted,
        total_debit=total_debit,
        total_kredit=total_kredit
   )
def format_rupiah(value):
    try:
        value = float(value)
        return "Rp{:,.0f}".format(value).replace(",", ".")
    except:
        return value

app.jinja_env.filters["rupiah"] = format_rupiah
@app.route("/neraca-lajur", methods=["GET", "POST"])
def neraca_lajur():
    if request.method == "POST":
        sebelum = supabase.table("neraca_saldo_sebelum_penyesuaian").select("*").execute().data
        penyesuaian = supabase.table("jurnal_penyesuaian").select("*").execute().data
        setelah = supabase.table("neraca_setelah_penyesuaian").select("*").execute().data

        dict_awal = {row["kode_akun"]: row for row in sebelum}
        
        dict_adj = {}
        for row in penyesuaian:
            kode = str(row["kode_akun"])  # atau row["kode_akun"] kalau itu kolomnya
            if kode not in dict_adj:
                dict_adj[kode] = []
            dict_adj[kode].append(row)

        dict_after = {row["kode_akun"]: row for row in setelah}

        semua_kode = sorted(
            set(dict_awal.keys()) |
            set(dict_adj.keys()) |
            set(dict_after.keys()))
        rows_to_save = []

        for kode in semua_kode:

            lr_d = lr_k = 0
            nr_d = nr_k = 0

            awal = dict_awal.get(kode, {})
            adj_rows = dict_adj.get(kode, [])
            aft = dict_after.get(kode, {})

            if awal:
                nama = awal.get("nama_akun", "")
            elif adj_rows:
                nama = adj_rows[0].get("nama", "")
            else:
                nama = ""

            awal_d = awal.get("debit", 0)
            awal_k = awal.get("kredit", 0)

            adj_d = sum(r.get("debit", 0) for r in adj_rows)
            adj_k = sum(r.get("kredit", 0) for r in adj_rows)

            aft_d = aft.get("debit", 0)
            aft_k = aft.get("kredit", 0)

            kode_akun = str(kode)
            if kode_akun.startswith("4"):
                lr_k = aft_k - aft_d
            elif kode_akun.startswith(("5", "6")):
                lr_d = aft_d - aft_k

            if kode_akun.startswith("1"):   # Aset (normal debit)
                selisih = aft_d - aft_k
                if selisih >= 0:
                    nr_d = selisih
                else:
                    nr_k = abs(selisih)   # kalau minus, pindah ke kredit
            elif kode_akun.startswith(("2", "3")):   # Utang & Ekuitas (normal kredit)
                selisih = aft_k - aft_d
                if selisih >= 0:
                    nr_k = selisih
                else:
                    nr_d = abs(selisih) 
            rows_to_save.append({
                "kode_akun": kode_akun,
                "nama_akun": nama,
                "awal_d": awal_d,
                "awal_k": awal_k,
                "adj_d": adj_d,
                "adj_k": adj_k,
                "aft_d": aft_d,
                "aft_k": aft_k,
                "lr_d": lr_d,
                "lr_k": lr_k,
                "nr_d": nr_d,
                "nr_k": nr_k
            })

        
        supabase.table("neraca_lajur").delete().neq("id", 0).execute()

      
        supabase.table("neraca_lajur").insert(rows_to_save).execute()




        return redirect("/neraca-lajur")



    # ==========================================================
    # =========== GET: TAMPILKAN KE HALAMAN ====================
    # ==========================================================

    sebelum = supabase.table("neraca_saldo_sebelum_penyesuaian").select("*").execute().data
    penyesuaian = supabase.table("jurnal_penyesuaian").select("*").execute().data
    setelah = supabase.table("neraca_setelah_penyesuaian").select("*").execute().data

    dict_awal = {row["kode_akun"]: row for row in sebelum}
    dict_adj = {}
    for row in penyesuaian:
        kode = str(row["kode_akun"])  # atau row["kode_akun"] kalau itu kolomnya
        if kode not in dict_adj:
            dict_adj[kode] = []
        dict_adj[kode].append(row)
    dict_after = {row["kode_akun"]: row for row in setelah}

    semua_kode = sorted(
        set(dict_awal.keys()) |
        set(dict_adj.keys()) |
        set(dict_after.keys())
    )

    rows = []

    tot_awal_d = tot_awal_k = 0
    tot_adj_d = tot_adj_k = 0
    tot_aft_d = tot_aft_k = 0
    tot_lr_d = tot_lr_k = 0
    tot_nr_d = tot_nr_k = 0

    for kode in semua_kode:

        lr_d = lr_k = 0
        nr_d = nr_k = 0

        awal = dict_awal.get(kode, {})
        adj_rows = dict_adj.get(kode, [])
        aft = dict_after.get(kode, {})

        if awal:
            nama = awal.get("nama_akun", "")
        elif adj_rows:
            nama = adj_rows[0].get("nama", "")
        else:
            nama = ""

        awal_d = awal.get("debit", 0)
        awal_k = awal.get("kredit", 0)

        adj_d = sum(r.get("debit", 0) for r in adj_rows)
        adj_k = sum(r.get("kredit", 0) for r in adj_rows)

        aft_d = aft.get("debit", 0)
        aft_k = aft.get("kredit", 0)

        kode_akun = str(kode)

        if kode_akun.startswith("4"):
            lr_k = aft_k - aft_d
        elif kode_akun.startswith(("5", "6")):
            lr_d = aft_d - aft_k

        if kode_akun.startswith("1"):   # Aset (normal debit)
            selisih = aft_d - aft_k
            if selisih >= 0:
                nr_d = selisih
            else:
                nr_k = abs(selisih)   # kalau minus, pindah ke kredit
        elif kode_akun.startswith(("2", "3")):   # Utang & Ekuitas (normal kredit)
            selisih = aft_k - aft_d
            if selisih >= 0:
                nr_k = selisih
            else:
                nr_d = abs(selisih) 
       
        tot_awal_d += awal_d
        tot_awal_k += awal_k
        tot_adj_d += adj_d
        tot_adj_k += adj_k
        tot_aft_d += aft_d
        tot_aft_k += aft_k
        tot_lr_d += lr_d
        tot_lr_k += lr_k
        tot_nr_d += nr_d
        tot_nr_k += nr_k

        rows.append({
            "kode": kode,
            "nama": nama,
            "awal_d": awal_d,
            "awal_k": awal_k,
            "adj_d": adj_d,
            "adj_k": adj_k,
            "aft_d": aft_d,
            "aft_k": aft_k,
            "lr_d": lr_d,
            "lr_k": lr_k,
            "nr_d": nr_d,
            "nr_k": nr_k,
        })

  
    laba_rugi = tot_lr_k - tot_lr_d
    red_lr_d = tot_lr_d
    red_lr_k = tot_lr_k
    red_nr_d = tot_nr_d
    red_nr_k = tot_nr_k

    if laba_rugi > 0:
        red_lr_d += laba_rugi
        red_nr_k += laba_rugi
    elif laba_rugi < 0:
        red_lr_k += abs(laba_rugi)
        red_nr_d += abs(laba_rugi)


    html = """
    <html>
    <head>
        <title>Neraca Lajur</title>
        <style>
            body {
                background: #f5e9bf;
                font-family: Arial, sans-serif;
                padding: 20px;
            }
            h1 { text-align: center; color: #5e4803; font-weight: bold; }
            table {
                width: max-content;
                margin: auto;
                border-collapse: collapse;
                background: #eddda1;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                margin-top: 25px;
                color: #5e4803
                
            }
            th, td {
                border: 1px solid #ccc;
                padding: 6px 10px;
                text-align: left;
                border-color: #bd9919
            }
            th {
                background:  #f0d04f;
                color: #5e4803;
                text-align: center;
            }


        </style>
    </head>
    <body>

    <h1>Neraca Lajur</h1>

    <table>
        <tr>
            <th rowspan="2">Kode Akun</th>
            <th rowspan="2">Nama Akun</th>
            <th colspan="2">Neraca Saldo</th>
            <th colspan="2">Penyesuaian</th>
            <th colspan="2">Neraca Saldo Setelah Penyesuaian</th>
            <th colspan="2">Laba Rugi</th>
            <th colspan="2">Neraca</th>
        </tr>

        <tr>
            <th>Debit</th><th>Kredit</th>
            <th>Debit</th><th>Kredit</th>
            <th>Debit</th><th>Kredit</th>
            <th>Debit</th><th>Kredit</th>
            <th>Debit</th><th>Kredit</th>
        </tr>

        {% for r in rows %}
        <tr>
            <td>{{ r.kode }}</td>
            <td>{{ r.nama }}</td>

            <td>{% if r.awal_d %}Rp {{ "{:,.0f}".format(r.awal_d).replace(",", ".") }}{% endif %}</td>
            <td>{% if r.awal_k %}Rp {{ "{:,.0f}".format(r.awal_k).replace(",", ".") }}{% endif %}</td>

            <td>{% if r.adj_d %}Rp {{ "{:,.0f}".format(r.adj_d).replace(",", ".") }}{% endif %}</td>
            <td>{% if r.adj_k %}Rp {{ "{:,.0f}".format(r.adj_k).replace(",", ".") }}{% endif %}</td>

            <td>{% if r.aft_d %}Rp {{ "{:,.0f}".format(r.aft_d).replace(",", ".") }}{% endif %}</td>
            <td>{% if r.aft_k %}Rp {{ "{:,.0f}".format(r.aft_k).replace(",", ".") }}{% endif %}</td>

            <td>{% if r.lr_d %}Rp {{ "{:,.0f}".format(r.lr_d).replace(",", ".") }}{% endif %}</td>
            <td>{% if r.lr_k %}Rp {{ "{:,.0f}".format(r.lr_k).replace(",", ".") }}{% endif %}</td>

            <td>{% if r.nr_d %}Rp {{ "{:,.0f}".format(r.nr_d).replace(",", ".") }}{% endif %}</td>
            <td>{% if r.nr_k %}Rp {{ "{:,.0f}".format(r.nr_k).replace(",", ".") }}{% endif %}</td>
        </tr>
        {% endfor %}


        <tr class="total-row" style="background: #f0d04f;color:#5e4803; font-weight:bold;">
            <td colspan="2" style="text-align:center;">Jumlah</td>

            <td>{{ total_awal_d|rupiah }}</td>
            <td>{{ total_awal_k|rupiah }}</td>

            <td>{{ total_adj_d|rupiah }}</td>
            <td>{{ total_adj_k|rupiah }}</td>

            <td>{{ total_aft_d|rupiah }}</td>
            <td>{{ total_aft_k|rupiah }}</td>

            <td>{{ total_lr_d|rupiah }}</td>
            <td>{{ total_lr_k|rupiah }}</td>

            <td>{{ total_nr_d|rupiah }}</td>
            <td>{{ total_nr_k|rupiah }}</td>
        </tr>

       <tr class="laba-row"style="background: #f0d04f; color:#5e4803; font-weight:800;">
            <td colspan="2" style="text-align:center;">Laba (Rugi) Bersih</td>
            <td colspan="6"></td>

            
            {% if laba_rugi_bersih >= 0 %}
                <!-- LABA → LR DEBIT -->
                <td>{{ laba_rugi_bersih|rupiah }}</td> 
                <td></td>
            {% else %}
                <td></td>
                <td>{{ (laba_rugi_bersih|abs)|rupiah }}</td> 
            {% endif %}

            {% if laba_rugi_bersih >= 0 %}
                <!-- LABA → NERACA KREDIT -->
                <td></td>
                <td>{{ laba_rugi_bersih|rupiah }}</td>
            {% else %}
                <!-- RUGI → NERACA DEBIT -->
                <td>{{ (laba_rugi_bersih|abs)|rupiah }}</td>
                <td></td>
            {% endif %}
        </tr>

        <tr class="row-total-red" style="background: #f0d04f; color:#5e4803; font-weight:bold;">
            <td colspan="2"style="text-align:center;">Jumlah</td>
            <td colspan="6"></td>

           
            <td>{{ red_lr_d and red_lr_d|rupiah or "" }}</td>
            <td>{{ red_lr_k and red_lr_k|rupiah or "" }}</td>

            <!-- Kolom Neraca (Debit, Kredit) -->
            <td>{{ red_nr_d and red_nr_d|rupiah or "" }}</td>
            <td>{{ red_nr_k and red_nr_k|rupiah or "" }}</td>
        </tr>
    </table>
    <style>
    table {
        margin-bottom: 25px;
    }

    .button-aksi {
        background-color: #f1c232; 
        color: white; 
        padding: 12px 25px; 
        border-radius: 10px; 
        font-weight: bold; 
        text-decoration: none; 
        display: inline-block;
        margin-right: 10px;
    }
    </style>

    <!-- TOMBOL KEMBALI -->
    <a href="/dashboard" class="button-aksi">
        Kembali ke Dashboard
    </a>

    <!-- TOMBOL SIMPAN -->
    <form action="/neraca-lajur" method="POST" style="display:inline-block;">
        <button type="submit" 
            style="background-color:#6aa84f; color:white; padding:12px 25px; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">
            Simpan Neraca Lajur
        </button>
    </form>



    </body>
    </html>
    """

    return render_template_string(
        html,
        rows=rows,
        total_awal_d=tot_awal_d,
        total_awal_k=tot_awal_k,
        total_adj_d=tot_adj_d,
        total_adj_k=tot_adj_k,
        total_aft_d=tot_aft_d,
        total_aft_k=tot_aft_k,
        total_lr_d=tot_lr_d,
        total_lr_k=tot_lr_k,
        total_nr_d=tot_nr_d,
        total_nr_k=tot_nr_k,
        laba_rugi_bersih=laba_rugi,
        red_lr_d=red_lr_d,
        red_lr_k=red_lr_k,
        red_nr_d=red_nr_d,
        red_nr_k=red_nr_k,
    )

LAPORAN_WEB =  """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Laporan Keuangan</title>

    <style>
        body {
            font-family: Calibri, Arial, sans-serif;
            background: #FFFBEA;
            padding: 25px;
            color: #3a3a3a;
        }

        .box {
            margin: 30px auto;       
            border: 2px solid #D8B66A;
            padding: 18px;
            background: #FFF7DA;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            
            max-width: 750px;        /* BATASIN LEBAR BOX */
            width: 95%;              /* biar responsif di HP */
        }


        h2 {
            text-align: center;
            background: #E6C98E;
            padding: 12px;
            margin-top: 0;
            border-radius: 8px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 18px;
            font-size: 15px;
            table-layout: fixed; 
        }
        

        td {
            padding: 8px 6px;
            border-bottom: 1px solid #d9ba78;
        }
        .lpk-table, 
        .lpk-table th, 
        .lpk-table td {
            border: 1px solid #DAA520; /* warna garis */
            border-collapse: collapse;
        }

        .lpk-table th, 
        .lpk-table td {
            padding: 6px 10px;
        }
        .center {
            text-align: center;
        }
        .bold { font-weight: bold; }
        .right { text-align: right; }
        .mt20 { padding-top: 20px; }
        
        
    </style>

</head>
<body>

  <!-- ====================== -->
<!--   LAPORAN LABA RUGI    -->
<!-- ====================== -->
<div class="box">
    <h2>LAPORAN LABA RUGI</h2>

    <table>

    <!-- PENDAPATAN -->
    <tr>
        <td class="bold">Pendapatan :</td>
        <td></td>
        <td></td>
    </tr>

    {% for r in rows if r.kode_akun.startswith('4') %}
    <tr>
        <td>{{ r.nama_akun }}</td>
        <td></td>
        <td class="right">{{ r.lr_k | rupiah }}</td>
    </tr>
    {% endfor %}

    <!-- HPP -->
    <tr>
        <td class="bold mt20">Harga Pokok Penjualan :</td>
        <td></td>
        <td></td>
    </tr>

    {% for r in rows if r.kode_akun.startswith ('5') %}
    <tr>
        <td>{{ r.nama_akun }}</td>
        <td class="right">{{ r.lr_d | rupiah }}</td>   
        <td></td>                                      
    </tr>
    {% endfor %}
    <tr>
        <td class="bold mt20">Total Harga Pokok Penjualan</td>
        <td></td>
        <td class="right bold">({{ hpp | rupiah }})</td>
    </tr>


    <tr>
        <td class="bold mt20">Laba Kotor</td>
        <td></td>
        <td class="right bold">{{ laba_kotor | rupiah }}</td>
    </tr>

    <!-- BEBAN OPERASIONAL -->
    <tr>
        <td class="bold mt20">Beban Operasional :</td>
        <td></td>
        <td></td>
    </tr>

    {% for r in rows if r.kode_akun.startswith('6') %}
    <tr>
        <td>{{ r.nama_akun }}</td>
        <td class="right">{{ r.lr_d | rupiah }}</td>   <!-- KOLOM TENGAH -->
        <td></td>                                      <!-- KOLOM KANAN KOSONG -->
    </tr>
    {% endfor %}

    <!-- TOTAL BEBAN OPERASIONAL -->
    <tr>
        <td class="bold mt20">Total Beban Operasional</td>
        <td></td>
        <td class="right bold">({{ beban_operasional | rupiah }})</td>
    </tr>

    <!-- LABA BERSIH -->
    <tr>
        <td class="bold">Laba Bersih</td>
        <td></td>
        <td class="right bold">{{ laba_bersih | rupiah }}</td>
    </tr>

</table>



</div>
<!-- =========================== -->
<!--   LAPORAN PERUBAHAN EKUITAS -->
<!-- =========================== -->
<div class="box">
    <h2>LAPORAN PERUBAHAN EKUITAS</h2>

    <table>

        <tr>
            <td>Modal Awal</td>
            <td class="right">{{ modal_awal | rupiah }}</td>
        </tr>

        <tr><td class="bold mt20">Penambahan Modal :</td><td></td></tr>

        <tr>
            <td>Laba Bersih Periode</td>
            <td class="right">{{ laba_bersih | rupiah }}</td>
        </tr>

        <tr>
            <td class="bold">Total Kenaikan Modal</td>
            <td class="right bold">{{ total_kenaikan_modal | rupiah }}</td>
        </tr>

        <tr><td class="bold mt20">Pengurangan Modal :</td><td></td></tr>

        <tr>
            <td class="bold">Total Penurunan Modal</td>
            <td class="right bold">{{ prive | rupiah }}</td>
        </tr>

        <tr>
            <td class="bold mt20">Modal Akhir</td>
            <td class="right bold">{{ modal_akhir | rupiah }}</td>
        </tr>

    </table>
</div>

<!-- ============================= -->
<!--       LAPORAN POSISI KEUANGAN -->
<!-- ============================= -->
<div class="box">
    <h2>LAPORAN POSISI KEUANGAN</h2>

   <table class="lpk-table">


        <tr>
            <th>Aset</th>
            <th>Desember</th>
            <th>Utang & Modal</th>
            <th>Desember</th>
        </tr>

        <!-- ======================= -->
        <!--        ASET LANCAR       -->
        <!-- ======================= -->
        <tr>
            <td class="bold">Aset Lancar :</td>
            <td></td>
            <td class="bold">Utang :</td>
            <td></td>
        </tr>

                <!-- ASET LANCAR -->
       

        {% set max_len = [
            aset_lancar_list|length,
            utang_list|length
        ] | max %}

        {% for i in range(max_len) %}
        <tr>
            {# --- ASET LANCAR KIRI --- #}
            {% if i < aset_lancar_list|length %}
                <td>{{ aset_lancar_list[i].nama_akun }}</td>
                <td class="right">{{ aset_lancar_list[i].nr_d|rupiah }}</td>
            {% else %}
                <td></td><td></td>
            {% endif %}

            {# --- UTANG KANAN --- #}
            {% if i < utang_list|length %}
                <td>{{ utang_list[i].nama_akun }}</td>
                <td class="right">{{ utang_list[i].nr_k|rupiah }}</td>
            {% else %}
                <td></td><td></td>
            {% endif %}
        </tr>
        {% endfor %}


        <!-- SUBTOTAL ASET LANCAR -->
        <tr class="subtotal">
            <td class="bold">Total Aset Lancar</td>
            <td class="right bold">{{ aset_lancar|rupiah }}</td>
            <td class="bold">Total Utang</td>
            <td class="right bold">{{ utang|rupiah }}</td>
        </tr>

        <!-- ======================= -->
        <!--        ASET TETAP       -->
        <!-- ======================= -->
        <tr>
            <td class="bold">Aset Tetap :</td>
            <td></td>
            <td class="bold">Modal :</td>
            <td></td>
        </tr>

        {% set max_len = [
            aset_tetap_list|length,
            modal_list|length
        ] | max %}

        {% for i in range(max_len) %}
        <tr>

            {# =================== KIRI: ASET TETAP =================== #}
            {% if i < aset_tetap_list|length %}
                <td>{{ aset_tetap_list[i].nama_akun }}</td>

                <td class="right">
                    {% if aset_tetap_list[i].nr_d > aset_tetap_list[i].nr_k %}
                        {{ (aset_tetap_list[i].nr_d - aset_tetap_list[i].nr_k)|rupiah }}
                    {% elif aset_tetap_list[i].nr_k > aset_tetap_list[i].nr_d %}
                        ({{ (aset_tetap_list[i].nr_k - aset_tetap_list[i].nr_d)|rupiah }})
                    {% else %}
                        {{ 0|rupiah }}
                    {% endif %}
                </td>
            {% else %}
                <td></td><td></td>
            {% endif %}

            {# =================== KANAN: MODAL =================== #}
            {% if i < modal_list|length %}
                <td>{{ modal_list[i].nama_akun }}</td>

                <td class="right">
                    {% if modal_list[i].nr_k > modal_list[i].nr_d %}
                        {{ (modal_list[i].nr_k - modal_list[i].nr_d)|rupiah }}
                    {% elif modal_list[i].nr_d > modal_list[i].nr_k %}
                        ({{ (modal_list[i].nr_d - modal_list[i].nr_k)|rupiah }})
                    {% else %}
                        {{ 0|rupiah }}
                    {% endif %}
                </td>
            {% else %}
                <td></td><td></td>
            {% endif %}

        </tr>
        {% endfor %}



        <!-- SUBTOTAL ASET TETAP -->
        <tr class="subtotal">
            <td class="bold">Total Aset Tetap</td>
            <td class="right bold">{{ aset_tetap|rupiah }}</td>
            <td class="bold">Total Modal</td>
            <td class="right bold">{{ ekuitas|rupiah }}</td>
        </tr>

        <!-- TOTAL BESAR -->
        <tr class="subtotal">
            <td class="bold">Total Aset</td>
            <td class="right bold">{{ total_aset|rupiah }}</td>
            <td class="bold">Total Utang & Modal</td>
            <td class="right bold">{{ total_utang_modal|rupiah }}</td>
        </tr>

    </table>
    </div>
    <div class="box">
        <h2>LAPORAN ARUS KAS</h2>

    <table>

        <tr>
            <td class="bold">ARUS KAS DARI AKTIVITAS OPERASI</td>
            <td></td>
            <td></td>
        </tr>

        <!-- Penerimaan -->
        {% for akun, total in arus_kas.penerimaan.items() %}
        <tr>
            <td>{{ akun }}</td>
            <td></td>
            <td class="right">
                {% if total < 0 %}
                    ({{ (-total)|rupiah }})
                {% else %}
                    {{ total|rupiah }}
                {% endif %}
            </td>
        </tr>
        {% endfor %}

        <tr>
            <td class="bold">TOTAL PENERIMAAN KAS</td>
            <td></td>
            <td class="right bold">
                {% if arus_kas.total_penerimaan < 0 %}
                    ({{ (-arus_kas.total_penerimaan)|rupiah }})
                {% else %}
                    {{ arus_kas.total_penerimaan|rupiah }}
                {% endif %}
            </td>
        </tr>

        <!-- Pengeluaran -->
        <tr><td class="mt20 bold">PENGELUARAN KAS :</td><td></td><td></td></tr>

        {% for akun, total in arus_kas.pengeluaran.items() %}
        <tr>
            <td>{{ akun }}</td>

            <!-- KOLOM TENGAH -->
            <td class="center">
                {% if total < 0 %}
                    ({{ (-total)|rupiah }})
                {% else %}
                    {{ total|rupiah }}
                {% endif %}
            </td>

            <!-- KOLOM KANAN KOSONG -->
            <td></td>
        </tr>

        {% endfor %}

        <tr>
            <td class="bold">TOTAL PENGELUARAN KAS</td>
            <td></td>
            <td class="right bold">
                {% if arus_kas.total_pengeluaran < 0 %}
                    ({{ (-arus_kas.total_pengeluaran)|rupiah }})
                {% else %}
                    {{ arus_kas.total_pengeluaran|rupiah }}
                {% endif %}
            </td>
        </tr>

        <tr>
            <td class="bold mt20">ARUS KAS BERSIH DARI AKTIVITAS OPERASI</td><td></td>
            <td class="right bold">
                {% if arus_kas.kas_bersih_operasi < 0 %}
                    ({{ (-arus_kas.kas_bersih_operasi)|rupiah }})
                {% else %}
                    {{ arus_kas.kas_bersih_operasi|rupiah }}
                {% endif %}
            </td>
        </tr>
            <!-- Spacer -->
        <tr><td colspan="3" style="height: 20px;"></td></tr>

        <!-- KAS AWAL PERIODE -->
        <tr>
            <td class="bold">KAS AWAL PERIODE, 1 DES</td><td></td>
            <td class="right bold">
                {% if kas_awal < 0 %}
                    ({{ (-kas_awal)|rupiah }})
                {% else %}
                    {{ kas_awal|rupiah }}
                {% endif %}
            </td>
        </tr>

        <!-- KENAIKAN / PENURUNAN KAS BERSIH -->
        <tr>
            <td class="bold">
                {% if arus_kas.kas_bersih_operasi < 0 %}
                    PENURUNAN KAS BERSIH
                {% else %}
                    KENAIKAN KAS BERSIH
                {% endif %}
            </td>
            <td></td>
            <td class="right bold">
                {% if arus_kas.kas_bersih_operasi < 0 %}
                    ({{ (-arus_kas.kas_bersih_operasi)|rupiah }})
                {% else %}
                    {{ arus_kas.kas_bersih_operasi|rupiah }}
                {% endif %}
            </td>
        </tr>

        <!-- KAS AKHIR PERIODE -->
        <tr>
            <td class="bold">KAS AKHIR PERIODE, 31 DES</td><td></td>
            <td class="right bold">
                {% set kas_akhir = kas_awal + arus_kas.kas_bersih_operasi %}
                {% if kas_akhir < 0 %}
                    ({{ (-kas_akhir)|rupiah }})
                {% else %}
                    {{ kas_akhir|rupiah }}
                {% endif %}
            </td>
        </tr>

    </table>
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



def get_neraca_lajur_data():
    # AMBIL DATA NERACA LAJUR DARI SUPABASE
    response = supabase.table("neraca_lajur").select("*").execute()

    if not response.data:
        return []

    rows = []
    for r in response.data:
        rows.append({
            "kode_akun": r.get("kode_akun", ""),
            "nama_akun": r.get("nama_akun", ""),

            # kolom laba rugi
            "lr_d": r.get("lr_d", 0) or 0,
            "lr_k": r.get("lr_k", 0) or 0,

            # kolom neraca
            "nr_d": r.get("nr_d", 0) or 0,
            "nr_k": r.get("nr_k", 0) or 0,

            # saldo setelah penutupan
            "aft_d": r.get("aft_d", 0) or 0,
            "aft_k": r.get("aft_k", 0) or 0,
        })

    return rows

def get_transaksi_kas():
    response = supabase.table("input_transaksi").select("*").execute()
    data = response.data or []

    penerimaan = {}
    pengeluaran = {}

    for r in data:
        akun = r.get("nama_akun", "").lower()
        debit = r.get("debit", 0) or 0
        kredit = r.get("kredit", 0) or 0
        no = r.get("no_transaksi")

        # Kas bertambah → debit kas
        if akun == "kas" and debit > 0:
            # cari akun lawan
            lawan = next((x["nama_akun"] for x in data 
                          if x["no_transaksi"] == no and x["kredit"] > 0), "Pendapatan Lainnya")
            penerimaan[lawan] = penerimaan.get(lawan, 0) + debit

        # Kas berkurang → kredit kas
        if akun == "kas" and kredit > 0:
            lawan = next((x["nama_akun"] for x in data 
                          if x["no_transaksi"] == no and x["debit"] > 0), "Beban Lainnya")
            pengeluaran[lawan] = pengeluaran.get(lawan, 0) + kredit

    return penerimaan, pengeluaran


def hitung_laporan_arus_kas():
    penerimaan_raw, pengeluaran_raw = get_transaksi_kas()

    penerimaan = {}
    pengeluaran = {}

    # Klasifikasi aktivitas operasi
    for akun, total in penerimaan_raw.items():
        penerimaan[akun] = total

    for akun, total in pengeluaran_raw.items():
        pengeluaran[akun] = total

    total_penerimaan = sum(penerimaan.values())
    total_pengeluaran = sum(pengeluaran.values())
    kas_bersih_operasi = total_penerimaan - total_pengeluaran

    return {
        "penerimaan": penerimaan,
        "pengeluaran": pengeluaran,
        "total_penerimaan": total_penerimaan,
        "total_pengeluaran": total_pengeluaran,
        "kas_bersih_operasi": kas_bersih_operasi
    }


@app.route("/laporan-keuangan")
def laporan_keuangan():
    rows = get_neraca_lajur_data()
    arus_kas = hitung_laporan_arus_kas()


    # =========================
    #       LABA RUGI
    # =========================
    pendapatan = sum(r["lr_k"] for r in rows if r["kode_akun"].startswith("4"))
    hpp = sum(r["lr_d"] for r in rows if r["kode_akun"].startswith("5"))
    beban_operasional = sum(r["lr_d"] for r in rows if r["kode_akun"].startswith("6"))

    laba_kotor = pendapatan - hpp
    laba_bersih = laba_kotor - beban_operasional

    # =========================
    #    PERUBAHAN EKUITAS
    # =========================
    modal_awal = sum(r["aft_k"] for r in rows if r["kode_akun"].startswith("3"))
    prive = sum(r["aft_d"] for r in rows if r["kode_akun"].startswith("3"))

    total_kenaikan_modal = laba_bersih
    total_penurunan_modal = prive

    modal_akhir = modal_awal + laba_bersih - prive

    # =========================
    #      POSISI KEUANGAN
    # =========================
    aset_lancar_list = [
        r for r in rows
        if r["kode_akun"].startswith("1-1")
    ]

    aset_lancar = sum(
        r["nr_d"] for r in rows
        if r["kode_akun"].startswith(("1-1"))
    )
    aset_tetap_list = [
        r for r in rows
        if r["kode_akun"].startswith("1-2")
    ]


    aset_tetap = sum(
        r["nr_d"] - r["nr_k"]
        for r in rows
        if r["kode_akun"].startswith("1-2")
    )


    total_aset = aset_lancar + aset_tetap
    utang_list = [r for r in rows if r.get("kode_akun", "").startswith("2")]




    utang = sum(r["nr_k"] for r in rows if r["kode_akun"].startswith("2"))
    modal_list = [
        r for r in rows
        if r.get("kode_akun", "").startswith("3-11")
    ]

    ekuitas = modal_akhir

    total_utang_modal = utang + ekuitas
    # Ambil kas awal dari neraca saldo awal
    kas_awal_data = supabase.table("neraca_saldo_awal") \
        .select("Nama_Akun, Debit, Kredit") \
        .eq("Nama_Akun", "Kas") \
        .execute().data

    kas_awal = 0
    if kas_awal_data:
        kas_awal = kas_awal_data[0]["Debit"] - kas_awal_data[0]["Kredit"]


   
    return render_template_string(
        LAPORAN_WEB,
        rows=rows,
        pendapatan=pendapatan,
        hpp=hpp,
        laba_kotor=laba_kotor,
        beban_operasional=beban_operasional,
        laba_bersih=laba_bersih,
        modal_awal=modal_awal,
        prive=prive,
        total_kenaikan_modal=total_kenaikan_modal,
        total_penurunan_modal=total_penurunan_modal,
        modal_akhir=modal_akhir,
        aset_lancar_list=aset_lancar_list,
        aset_lancar=aset_lancar,
        aset_tetap_list=aset_tetap_list,
        aset_tetap=aset_tetap,
        total_aset=total_aset,
        utang_list=utang_list,
        utang=utang,
        modal_list=modal_list,
        ekuitas=ekuitas,
        total_utang_modal=total_utang_modal,
        arus_kas=arus_kas,
        kas_awal=kas_awal,
        )
    
JURNAL_PENUTUP_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Jurnal Penutup</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #FFFCE7;
            padding: 25px;
        }

        h1 {
            color: #DAA520;
            border-left: 6px solid #DAA520;
            padding-left: 12px;
            margin-bottom: 20px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
            border-left: 2px solid #edf553;
        }

        .row {
            display: flex;
            gap: 12px;
            margin-bottom: 10px;
        }

        input {
            padding: 10px;
            border: 1px solid #C9A86A;
            border-radius: 10px;
            font-size: 14px;
        }

        .mid   { width: 220px; }
        .small { width: 90px; }

        button {
            padding: 10px 16px;
            background: #F4C430;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            color: white;
        }

        .add-btn {
            background: #4CAF50;
            margin-top: 10px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 16px;
            color:#614924;
        }
        .total-row td {
            background: #FAE7A5 !important;
            font-weight: bold;
            border-top: 2px solid #edf553;
            border-bottom: 2px solid #edf553;
            border-left: 2px solid #edf553;
        }


        th {
            background: #FAE7A5;
            padding: 12px;
            text-align: center;
            font-weight: bold;
            border-left: 2px solid #f7ee6a;
            border-bottom: 2px solid #f7ee6a;
            color: #614924;
        }

        td {
            padding: 10px;
            border-left: 2px solid #f7ee6a;
            border-bottom: 2px solid #f7ee6a;
            background: #fcfbe1;
            color: #614924,
        }



        .tanggal-cell {
            vertical-align: top;
            text-align: center;
            font-weight: 600;
            width: 110px;
        }

        .akun-debit {
            padding-left: 35px !important;
            text-align: left;
            font-weight: 600;
        }

        .akun-kredit {
            justify-content: left; 
            text-align: left;
            font-weight: 600;
            padding-left: 10%
        }

        .center {
            text-align: center;
            font-weight: 600;
        }
    </style>
</head>

<body>

<h1>📘 Jurnal Penutup</h1>

<div class="card">
    <h2 style="color:#DAA520;">Input Jurnal Penutup</h2>

    <form method="POST">

        <div class="row">
            <input type="date" name="tanggal" required>
        </div>

        <div id="input-area">
            <div class="row">
                <input type="text"   name="nama_akun[]" class="mid" placeholder="Nama Akun" required>
                <input type="text"   name="ref[]" class="small" placeholder="Ref">
                <input type="number" name="debit[]" class="small" placeholder="Debit">
                <input type="number" name="kredit[]" class="small" placeholder="Kredit">
            </div>
        </div>

        <button type="button" class="add-btn" onclick="addRow()">+ Tambah Baris</button>
        <button type="submit">Simpan</button>

    </form>
</div>


<div class="card">
    <h2 style="color:#DAA520;">Daftar Jurnal Penutup</h2>

<table>
    <tr>
        <th>Tanggal</th>
        <th>Nama Akun</th>
        <th>Ref</th>
        <th>Debit</th>
        <th>Kredit</th>
    </tr>

    {% set grouped = {} %}

    {% for r in penutup_entries %}
        {% if r.tanggal not in grouped %}
            {% set _ = grouped.update({ r.tanggal: [] }) %}
        {% endif %}
        {% set _ = grouped[r.tanggal].append(r) %}
    {% endfor %}

    {% for tanggal, rows in grouped.items() %}
        {% for i in range(rows|length) %}
            {% set row = rows[i] %}
            <tr>

                {% if i == 0 %}
                <td class="tanggal-cell" rowspan="{{ rows|length }}">
                    {{ tanggal }}
                </td>
                {% endif %}

                <td class="{% if row.debit > 0 %}akun-debit{% else %}akun-kredit{% endif %}">
                    {{ row.nama_akun }}
                </td>

                <td class="center">{{ row.ref or "" }}</td>

                <td class="center">
                    {% if row.debit > 0 %}
                        Rp {{ "{:,.0f}".format(row.debit).replace(",", ".") }}
                    {% endif %}
                </td>

                <td class="center">
                    {% if row.kredit > 0 %}
                        Rp {{ "{:,.0f}".format(row.kredit).replace(",", ".") }}
                    {% endif %}
                </td>
            </tr>
        {% endfor %}
    {% endfor %}

    <tr class="total-row">

        <td colspan="3" style="text-align:left; padding:15px;">TOTAL</td>
        <td class="center">Rp {{ "{:,.0f}".format(total_debit).replace(",", ".") }}</td>
        <td class="center">Rp {{ "{:,.0f}".format(total_kredit).replace(",", ".") }}</td>

    </tr>

</table>
<style>
table {
    margin-bottom: 25px;
}
</style>

<a href="/dashboard"
   style="background-color: #f1c232; color: white; padding: 12px 25px; border-radius: 10px; font-weight: bold; text-decoration: none; display: inline-block;">
    Kembali ke Dashboard
</a>

</div>


<script>
function addRow() {
    let div = document.createElement("div");
    div.className = "row";

    div.innerHTML = `
        <input type="text"   name="nama_akun[]" class="mid" placeholder="Nama Akun" required>
        <input type="text"   name="ref[]" class="small" placeholder="Ref">
        <input type="number" name="debit[]" class="small" placeholder="Debit">
        <input type="number" name="kredit[]" class="small" placeholder="Kredit">
    `;

    document.getElementById("input-area").appendChild(div);}
</script>

</body>
</html>
"""

@app.route("/jurnal-penutup", methods=["GET", "POST"])
def jurnal_penutup():
    if request.method == "POST":
        tanggal = request.form.get("tanggal")
        nama_akun = request.form.getlist("nama_akun[]")
        ref = request.form.getlist("ref[]")
        debit = request.form.getlist("debit[]")
        kredit = request.form.getlist("kredit[]")

        for i in range(len(nama_akun)):
            if not nama_akun[i].strip():
                continue

            d = float(debit[i]) if debit[i] else 0
            k = float(kredit[i]) if kredit[i] else 0

            supabase.table("jurnal_penutup").insert({
                "tanggal": tanggal,
                "nama_akun": nama_akun[i],
                "ref": ref[i] or None,
                "debit": d,
                "kredit": k
            }).execute()

    data = (
        supabase.table("jurnal_penutup")
        .select("*")
        .order("tanggal")
        .execute()
        .data
    )

    total_debit = sum(x["debit"] for x in data)
    total_kredit = sum(x["kredit"] for x in data)

    return render_template_string(
        JURNAL_PENUTUP_WEB,
        penutup_entries=data,
        total_debit=total_debit,
        total_kredit=total_kredit
    )
NERACA_SESUDAH_PENUTUP_WEB = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Neraca Saldo Setelah Penutupan</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #FFFCE7;
            padding: 20px;
        }
        h1 {
            color: #DAA520;
            border-left: 6px solid #DAA520;
            padding-left: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px;
        }
        th {
            background: #FAF3C3;
            text-align: center;
        }
        td.nama { text-align: left; }
        td.kode { text-align: center; }
        td.ref  { text-align: center; }
        td.num { text-align: right; }
        .total {
            font-weight: bold;
            background: #FFF4C1;
        }
    </style>
</head>
<body>

<h1>Neraca Saldo Setelah Penutupan</h1>

<table>
    <thead>
        <tr>
            <th>Kode Akun</th>
            <th>Nama Akun</th>
            <th>Debit</th>
            <th>Kredit</th>
        </tr>
    </thead>
    <tbody>
        {% for kode, a in akun.items() %}
        <tr>
            <td class="kode">{{ kode }}</td>
            <td class="nama">{{ a.nama }}</td>

            <td class="num">
                {% if a.debit > 0 %}
                    Rp{{ "{:,.0f}".format(a.debit).replace(",", ".") }}
                {% endif %}
            </td>

            <td class="num">
                {% if a.kredit > 0 %}
                    Rp{{ "{:,.0f}".format(a.kredit).replace(",", ".") }}
                {% endif %}
            </td>
        </tr>
        {% endfor %}

        <tr class="total">
            <td colspan="2">Total</td>
            <td class="num">Rp{{ "{:,.0f}".format(total_debit).replace(",", ".") }}</td>
            <td class="num">Rp{{ "{:,.0f}".format(total_kredit).replace(",", ".") }}</td>
        </tr>

    </tbody>
</table>

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

@app.route("/neraca-saldo-setelah-penutupan")
def neraca_saldo_setelah_penutupan():

    # --- ambil data sumber ---
    saldo_awal = supabase.table("neraca_saldo_awal").select("*").execute().data
    transaksi = supabase.table("input_transaksi").select("*").order("tanggal").execute().data
    penyesuaian = supabase.table("jurnal_penyesuaian").select("*").order("tanggal").execute().data
    penutup = supabase.table("jurnal_penutup").select("*").order("tanggal").execute().data

    buku_besar = {}

    # ============================
    # helper sama kayak buku besar
    # ============================
    def fix(n):
        return n.strip().lower() if n else ""

    def get_nama(row):
        return (row.get("nama_akun") or row.get("Nama_Akun") or row.get("akun") or "").strip()

    # ===============================
    # SALDO AWAL  (identik buku besar)
    # ===============================
    for row in saldo_awal:
        nama = get_nama(row)
        key = fix(nama)
        kode = row.get("ref") or row.get("Kode_Akun") or row.get ("kode_akun")

        if key not in buku_besar:
            buku_besar[key] = {"nama": nama, "kode": kode, "rows": []}

        buku_besar[key]["rows"].append({
            "tanggal": "2024-12-01",
            "keterangan": "Saldo Awal",
            "ref": kode,
            "debit": float(row.get("debit") or row.get("Debit") or 0),
            "kredit": float(row.get("kredit") or row.get("Kredit") or 0)
        })

    # ===============================
    # JURNAL UMUM  (identik buku besar)
    # ===============================
    for t in transaksi:
        nama = get_nama(t)
        key = fix(nama)
        kode = t["ref"]

        if key not in buku_besar:
            buku_besar[key] = {"nama": nama, "kode": kode, "rows": []}

        buku_besar[key]["rows"].append({
            "tanggal": t["tanggal"],
            "keterangan": t.get("keterangan", "Transaksi"),
            "ref": kode,
            "debit": float(t["debit"] or 0),
            "kredit": float(t["kredit"] or 0)
        })

    # ===============================
    # PENYESUAIAN (identik buku besar)
    # ===============================
    for p in penyesuaian:
        nama = get_nama(p)
        key = fix(nama)
        kode = p["kode_akun"]

        if key not in buku_besar:
            buku_besar[key] = {"nama": nama, "kode": kode, "rows": []}

        buku_besar[key]["rows"].append({
            "tanggal": p["tanggal"],
            "keterangan": "Penyesuaian",
            "kode_akun": kode,
            "debit": float(p["debit"] or 0),
            "kredit": float(p["kredit"] or 0)
        })

    # ===============================
    # PENUTUP (identik buku besar)
    # ===============================
    for jp in penutup:
        nama = get_nama(jp)
        key = fix(nama)
        kode = jp["ref"]

        if key not in buku_besar:
            buku_besar[key] = {"nama": nama, "kode": kode, "rows": []}

        buku_besar[key]["rows"].append({
            "tanggal": jp["tanggal"],
            "keterangan": "Penutup",
            "ref": kode,
            "debit": float(jp["debit"] or 0),
            "kredit": float(jp["kredit"] or 0)
        })

    # ===============================
    # HITUNG SALDO BERJALAN (sama persis)
    # ===============================
    for akun in buku_besar.values():
        saldo = 0
        for r in akun["rows"]:
            saldo += r["debit"] - r["kredit"]
            r["saldo"] = saldo

    # ===================================================
    # AMBIL SALDO AKHIR UNTUK NERACA (kode 1 – 3 saja)
    # ===================================================
    neraca = {}

    for akun in buku_besar.values():
        kode = str(akun["kode"]).strip()

        if not kode or kode[0] not in ["1", "2", "3"]:
            continue

        rows = akun["rows"]
        saldo_akhir = rows[-1]["saldo"] if rows else 0

        if saldo_akhir == 0:
            continue

        if saldo_akhir > 0:
            d = saldo_akhir; k = 0
        else:
            d = 0; k = abs(saldo_akhir)

        neraca[kode] = {
            "nama": akun["nama"],
            "debit": d,
            "kredit": k
        }

    
    neraca_sorted = dict(sorted(neraca.items(), key=lambda x: x[0]))

    total_debit = sum(v["debit"] for v in neraca_sorted.values())
    total_kredit = sum(v["kredit"] for v in neraca_sorted.values())

    return render_template_string(
        NERACA_SESUDAH_PENUTUP_WEB,
        akun=neraca_sorted,
        total_debit=total_debit,
        total_kredit=total_kredit
    )






# ✅ Pindah ke paling bawah
if __name__ == "__main__":
    app.run(debug=True)
