from flask import Flask, redirect, request, render_template, session, url_for
from mysql import connector 

app = Flask(__name__)
app.secret_key = '12345'

def get_db_connection():
    return connector.connect(
        host="localhost",
        database="projeto_batman",
        user="root",
        password="endryw123"
    )

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("user")
    password = request.form.get("password")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and user['password'] == password:
            session['user'] = {
                'username': user['username'],
                'role': user['role']
            }
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('home') + "?error=Credenciais inválidas")

    except Exception as e:
        print(f"Erro: {e}")
        return redirect(url_for('home') + "?error=Erro no servidor")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bat_items")
        items = cursor.fetchall()
    except Exception as e:
        print(f"Erro: {e}")
        items = []
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return render_template("dashboard.html",
                         items=items,
                         role=session['user']['role'])

@app.route("/add_item", methods=["POST"])
def add_item():
    if 'user' not in session or session['user']['role'] not in ['gerente', 'adm']:
        return redirect(url_for('dashboard'))
    
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    description = request.form.get('description')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bat_items (name, quantity, description) VALUES (%s, %s, %s)",
            (name, quantity, description)
        )
        conn.commit()
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('dashboard'))

@app.route("/delete_item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    if 'user' not in session or session['user']['role'] != 'adm':
        return redirect(url_for('dashboard'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bat_items WHERE id = %s", (item_id,))
        conn.commit()
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect(url_for('dashboard'))

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)