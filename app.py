from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from models import db, Usuario, Entrada, Comentario, Categoria

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://root:@localhost/miniblog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    entradas = Entrada.query.all()
    return render_template('index.html', entradas=entradas)

@app.route('/post/<int:post_id>')
def post(post_id):
    entrada = Entrada.query.get_or_404(post_id)
    return render_template('post.html', entrada=entrada)

@app.route('/create_post', methods=['GET', 'POST'])

def create_post():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        nueva_entrada = Entrada(titulo=titulo, contenido=contenido, autor_id=1)  
        db.session.add(nueva_entrada)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_post.html')

@app.context_processor
def inject_categorias():
    categorias = Categoria.query.all()
    return dict(categorias=categorias)

if __name__ == '__main__':
    app.run(debug=True)