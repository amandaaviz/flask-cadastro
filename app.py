from flask import Flask, render_template, request, redirect
import os
import psycopg2
from urllib.parse import urlparse
import sys

app = Flask(__name__)

# Obtém a URL do banco de dados da variável de ambiente
DATABASE_URL = os.environ.get("DATABASE_URL")


if not DATABASE_URL:
    print("Erro: A variável de ambiente DATABASE_URL não está definida.")
    sys.exit(1)


def get_connection():
    """Ajusta a URL para compatibilidade com psycopg2 e retorna uma conexão."""
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL_fixed = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    else:
        DATABASE_URL_fixed = DATABASE_URL
    return psycopg2.connect(DATABASE_URL_fixed)

def init_db():
    try:
        conn = get_connection()
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
        print("Tabela criada com sucesso (ou já existia).")
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        descricao = request.form.get('descricao')

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO pesquisadores (nome, email, telefone, descricao) 
                VALUES (%s, %s, %s, %s)
            """, (nome, email, telefone, descricao))
            conn.commit()
            cur.close()
            conn.close()
            print("[DEBUG] Cadastro inserido com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir cadastro: {e}")
        return redirect('/')
    return render_template('index.html')

@app.route('/admin')
def admin():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pesquisadores")
        pesquisadores = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('admin.html', pesquisadores=pesquisadores)
    except Exception as e:
        return f"Erro ao acessar banco de dados: {e}"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
