from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Criação automática da tabela no SQLite
def init_db():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pesquisadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Rota principal: formulário de cadastro
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        descricao = request.form['descricao']
        conn = sqlite3.connect('banco.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO pesquisadores (nome, email, telefone, descricao) VALUES (?, ?, ?, ?)",
                    (nome, email, telefone, descricao))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('index.html')

# Página de administração
@app.route('/admin')
def admin():
    conn = sqlite3.connect('banco.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM pesquisadores")
    pesquisadores = cur.fetchall()
    conn.close()
    return render_template('admin.html', pesquisadores=pesquisadores)

# Garante que o banco seja criado ao subir a aplicação
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

