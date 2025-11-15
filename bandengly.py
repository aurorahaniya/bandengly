from flask import Flask, render_template_string, request, redirect, url_for, session
from supabase import create_client
from dotenv import load_dotenv
import os

# Load .env
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
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(135deg, #ade8f4, #caf0f8);
      color: hsl(200, 84%, 75%);
      font-family: 'Poppins', sans-serif;
      height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      margin: 0;
    }
    h1 {
      font-weight: 700;
      font-size: 2.5rem;
      color: #03045e;
    }
    p {
      font-size: 1.1rem;
      color: #023047;
    }
    .btn-login {
      background-color: #0077b6;
      color: #f1f1f1;
      border-radius: 10px;
      padding: 10px 25px;
      font-weight: 500;
      transition: 0.3s;
      text-decoration: none;
    }
    .btn-login:hover {
      background-color: #005f86;
      transform: scale(1.05);
    }
    footer {
      position: absolute;
      bottom: 20px;
      font-size: 0.9rem;
      color: #03045e;
    }
  </style>
</head>
<body>
  <main>
    <h1>Selamat Datang di <strong>Bandengly!</strong></h1>
    <p class="mt-3">Website siklus akuntansi berbasis Flask + Supabase.</p>
    <a href="/login" class="btn-login mt-4 d-inline-block">Masuk dengan Email</a>
  </main>

  <footer>© 2025 Bandengly — Made with Flask + Supabase</footer>
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
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(135deg, #ade8f4, #caf0f8);
      font-family: 'Poppins', sans-serif;
      color: #023047;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .login-card {
      background: rgba(255, 255, 255, 0.85);
      border-radius: 15px;
      padding: 40px 50px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
      width: 100%;
      max-width: 400px;
    }
    h2 {
      color: #03045e;
      font-weight: 700;
      text-align: center;
      margin-bottom: 30px;
    }
    .form-control {
      border-radius: 8px;
      border: 1px solid #90e0ef;
    }
    .btn-login {
      background-color: #0077b6;
      color: white;
      border-radius: 8px;
      padding: 10px;
      font-weight: 500;
      width: 100%;
      transition: 0.3s;
    }
    .btn-login:hover {
      background-color: #005f86;
      transform: scale(1.02);
    }
    .link {
      display: block;
      text-align: center;
      margin-top: 15px;
      color: #03045e;
      text-decoration: none;
      font-weight: 500;
    }
    .link:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="login-card">
    <h2>Masuk dengan Email</h2>
    <form method="POST" action="/login">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" id="email" name="email" class="form-control" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" name="password" class="form-control" required>
      </div>
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

            session["user_email"] = email
            session["token"] = user.session.access_token
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
  <title>Daftar Akun | Bandengly</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(135deg, #ade8f4, #caf0f8);
      font-family: 'Poppins', sans-serif;
      color: #023047;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .register-card {
      background: rgba(255, 255, 255, 0.85);
      border-radius: 15px;
      padding: 40px 50px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
      width: 100%;
      max-width: 400px;
    }

    h2 {
      color: #03045e;
      font-weight: 700;
      text-align: center;
      margin-bottom: 30px;
    }

    .form-control {
      border-radius: 8px;
      border: 1px solid #90e0ef;
    }

    .btn-primary {
      background-color: #0077b6;
      border: none;
    }

    .btn-primary:hover {
      background-color: #023e8a;
    }
  </style>
</head>
<body>
  <div class="register-card">
    <h2>Daftar Akun</h2>
    <form method="POST" action="/register">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" name="email" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Kata Sandi</label>
        <input type="password" class="form-control" id="password" name="password" required>
      </div>
      <button type="submit" class="btn btn-primary w-100">Daftar</button>
      <p class="text-center mt-3">
        Sudah punya akun? <a href="/login">Masuk</a>
      </p>
    </form>
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
  <title>Dashboard</title>

  <!-- Tambahkan Bootstrap biar rapi -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Bandengly Dashboard</a>
      <div class="d-flex">
        <a href="/logout" class="btn btn-outline-light">Logout</a>
      </div>
    </div>
  </nav>

  <div class="container mt-5">
    <div class="card shadow-sm p-4">
      <h3 class="mb-3">Selamat datang, {{ user }} 👋</h3>
      <p>Ini adalah halaman dashboard utama kamu.</p>

      <hr>
      <div class="row text-center">
        <div class="col-md-4 mb-3">
          <div class="card border-0 shadow-sm p-3">
            <h5>📦 Data Produk</h5>
            <p>Kelola produk atau stok di sini.</p>
            <a href="#" class="btn btn-primary btn-sm">Buka</a>
          </div>
        </div>
        <div class="col-md-4 mb-3">
          <div class="card border-0 shadow-sm p-3">
            <h5>🛒 Transaksi</h5>
            <p>Lihat daftar transaksi penjualan.</p>
            <a href="#" class="btn btn-primary btn-sm">Buka</a>
          </div>
        </div>
        <div class="col-md-4 mb-3">
          <div class="card border-0 shadow-sm p-3">
            <h5>👤 Profil</h5>
            <p>Perbarui informasi akun kamu.</p>
            <a href="#" class="btn btn-primary btn-sm">Buka</
"""

# ✅ Halaman dashboard
@app.route("/dashboard")
def dashboard():
    print("➡️ MASUK KE DASHBOARD")  # <-- ini buat debug di terminal

    if "user_email" not in session:
        print("⛔ Session kosong, redirect login")
        return redirect("/login")

    user_email = session.get("user_email")
    print("✅ USER EMAIL:", user_email)
    return render_template_string(DASHBOARD_WEB, user=user_email)




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")





# ✅ Pindah ke paling bawah
if __name__ == "__main__":
    app.run(debug=True)
