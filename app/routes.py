from .import app
from flask import render_template, request, redirect, url_for, flash
from app.models import User, db, Post
from flask_login import login_user, logout_user, current_user
import requests
from bs4 import BeautifulSoup

class Player:
    team = []
    api = 'https://www.fangraphs.com/teams/'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':


        r = request.form
        if r.get('confirm_password') == r.get('password'):
            data = {
                'first_name': r.get('first_name'),
                'last_name': r.get('last_name'),
                'email': r.get('email'),
                'first_name': r.get('first_name'),
                'password': r.get('password')
            }
            u = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'])
            u.hash_password(u.password)
            db.session.add(u)
            db.session.commit()
            flash('You have registered Succesfully', 'primary')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        r = request.form
        user = User.query.filter_by(email=r.get('email')).first()
        if user is None or not user.check_password(r.get('password')):
            flash('You have used either an incorrect email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=r.get('remember_me'))
        flash('You have logged in succesfully!', 'success')
        return redirect(url_for('index'))
    return render_template('login.html')
@app.route('/logout')
def logout():
    logout_user()
    flash('You have sucessfully logged out', 'info')
    return redirect(url_for('login'))


@app.route('/create_post', methods=['POST'])
def create_post():
    if request.method == 'POST':
        r = request.form
        data = {
            "post_body": r.get('input'),
            'user_id': current_user.id
        }
        pp = data['post_body'.lower()]
        res = requests.get(f"{Player.api}/{pp}")
        page = BeautifulSoup(res.content, 'html.parser')
        table = page.find(class_='tablesort')
        tlist = [i for i in table]
        for i in range(len(tlist)):
            playerr = []
            for stat in tlist[i]:
                if not tlist[0] or tlist[-1]:
                    playerr.append(stat.text)
                    Player.team.append(playerr)
                    for i in Player.team:
                        if len(i) > 1:
                            data['post_body'] == (f"{i[0]}| Age: {i[1]} | G: {i[2]} | PA: {i[3]} | HR: {i[4]} | SB: {i[5]} | BB%: {i[6]} | K%: {i[7]} | ISO: {i[8]} | BABIP: {i[9]} | AVG: {i[10]} | OBP: {i[11]} | SLG: {i[12]} | wOBA: {i[13]} | wRC+: {i[14]} | BsR: {i[15]} | Off: {i[16]} | Def: {i[17]} | WAR: {i[18]}")
        
        
        p = Post(body=data['post_body'], user_id=data['user_id'])
        db.session.add(p)
        db.session.commit()
    return redirect(url_for('index'))
