from flask import render_template, request, redirect, flash, session, url_for,send_from_directory
from filmesvideo import app, db
from models import Filmes
from helpers import recupera_imagem,deleta_arquivo,FormularioFilme
import time

@app.route('/')
def index():
    filmes = Filmes.query.all()
    return render_template('lista.html', titulo='Filmes', filmes=filmes)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioFilme()
    return render_template('Novo.html', titulo= 'Novo filme', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioFilme(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    streaming = form.streaming.data

    filme = Filmes.query.filter_by(nome = nome).first()

    if filme:
        flash('Filme já existente!')
        return redirect(url_for('index'))

    novo_filme = Filmes(nome=nome,categoria=categoria,streaming=streaming)
    db.session.add(novo_filme)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_filme.id}--{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    filme = Filmes.query.filter_by(id=id).first()
    form = FormularioFilme()
    form.nome.data = filme.nome
    form.categoria.data = filme.categoria
    form.streaming.data = filme.streaming
    capa_filme = recupera_imagem(id)
    return render_template('editar.html', titulo= 'Editando Filme',id=id, capa_filme = capa_filme, form = form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioFilme(request.form)

    if form.validate_on_submit():

        filme = Filmes.query.filter_by(id=request.form['id']).first()
        filme.nome = form.nome.data
        filme.categoria = form.categoria.data
        filme.streaming = form.streaming.data

        db.session.add(filme)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(filme.id)
        arquivo.save(f'{upload_path}/capa{filme.id}--{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Filmes.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Filme deletado.')

    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads',nome_arquivo)

