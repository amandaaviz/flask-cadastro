from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Cria banco de dados e tabela se não existir
def init_db():
    conn = sqlite3.connect('banco.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS pesquisadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            descricao TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Página inicial: formulário
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

# Página do administrador
@app.route('/admin')
def admin():
    conn = sqlite3.connect('banco.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM pesquisadores")
    dados = cur.fetchall()
    conn.close()
    return render_template('admin.html', dados=dados)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

app.run(host='0.0.0.0', port=10000)
