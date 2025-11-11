from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL:", SUPABASE_URL)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inisialisasi Flask
app = Flask(__name__)
app.secret_key = "BANDENGLY_123"

# ✅ Halaman utama
@app.route("/")
def index():
    return render_template("index.html")

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
            return render_template("login.html", error="Login gagal! Periksa email & password.")

    return render_template("login.html")


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
            return render_template("register.html", error="Gagal daftar! " + str(e))

    return render_template("register.html")

@app.route("/auth/callback")
def auth_callback():
    from flask import request

    token = request.args.get("access_token")

    if not token:
        return "Token tidak ditemukan di URL verifikasi."

    # Simpan session login
    session["access_token"] = token

    return redirect("/dashboard")



# ✅ Halaman dashboard
@app.route("/dashboard")
def dashboard():
    print("➡️ MASUK KE DASHBOARD")  # <-- ini buat debug di terminal

    if "user_email" not in session:
        print("⛔ Session kosong, redirect login")
        return redirect("/login")

    user_email = session.get("user_email")
    print("✅ USER EMAIL:", user_email)
    return render_template("dashboard.html", user=user_email)




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")





# ✅ Pindah ke paling bawah
if __name__ == "__main__":
    app.run(debug=True)
