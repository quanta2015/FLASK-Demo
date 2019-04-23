import os, json, time, functools
from flask import Blueprint, render_template,current_app,request,flash,redirect,url_for,session,g

bp = Blueprint('index', __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        usr = session.get('usr')
        if usr is None:
            return redirect(url_for('index.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/')
def home():
    # session.clear()
    data = []
    path = current_app.root_path + '/data'
    files = os.listdir(path)
    files.sort()

    for f in files:
        if not f.endswith(".json"): continue
        fpath = path + '/' + f
        with open(fpath,'r') as load_f:
            cnt = json.load(load_f)
            data.append(cnt)

    return render_template('index.html', data=data)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'GET':
        return render_template('new.html')
    else:
        de = request.form['m-date']
        tl = request.form['m-title']
        co = request.form['m-content'] 
        data = { "date":  de, "title": tl, "content": co }

        if len(tl)==0 or len(co)==0:
            flash('error')
        else:
            pre = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            file = current_app.root_path + '/data/' + pre + '.json'
            with open(file,"w") as f:
                json.dump(data,f)
                flash('add blog success!')
                return redirect(url_for('index.home'))

        return render_template('new.html')



@bp.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = current_app.root_path + '/data/upload.txt'
        f.save(filename)
        flash('upload success!')
    return render_template('upload.html')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        usr = request.form['m-usr']
        pwd = request.form['m-pwd']
        data = { "usr": usr, "pwd": pwd }
        session.clear()
        session['usr'] = usr
        session['pwd'] = pwd
        if (usr=='zhang' and pwd=='a'): 
            flash('Login success!')
            session['isLogin'] = True
            return redirect(url_for('index.home'))
        else:
            flash('usr or password is invaild')
    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.home'))