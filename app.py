from flask import Flask, render_template, request, redirect
import os
import psycopg2

app = Flask(__name__)

# Obtém a URL do banco de dados da variável de ambiente
DATABASE_URL = os.environ.get("DATABASE_URL")

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS pesquisadores (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        descricao = request.form.get('descricao')

        print(f"[DEBUG] Recebido: {nome}, {email}, {telefone}, {descricao}")

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO pesquisadores (nome, email, telefone, descricao) 
            VALUES (%s, %s, %s, %s)
        """, (nome, email, telefone, descricao))
        conn.commit()
        print("[DEBUG] Cadastro inserido com sucesso.")
        cur.close()
        conn.close()
        return redirect('/')
    return render_template('index.html')

@app.route('/admin')
def admin():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pesquisadores")
    pesquisadores = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin.html', pesquisadores=pesquisadores)

if __name__ == '__main__':
    # Inicializa o banco de dados antes de rodar a aplicação
    init_db()
    app.run(host='0.0.0.0', port=10000)

