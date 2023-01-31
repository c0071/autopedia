from flask import Flask, render_template, request, redirect,flash
from models import db, AutolabelModel, AutomodelsModel, LotModel
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#@app.before_first_request
def create_table():
    db.create_all()
    label1=AutolabelModel('Ford','USA',1903)
    label2 = AutolabelModel('GAZ', 'Russia', 1933)
    label3 = AutolabelModel('BMW', 'Germany', 1906)
    db.session.add(label1)
    db.session.add(label2)
    db.session.add(label3)

    model1 = AutomodelsModel('Focus', 1, 1999)
    model2 = AutomodelsModel('Газель', 2, 1994)
    model3 = AutomodelsModel('X7', 3, 2018)
    db.session.add(model1)
    db.session.add(model2)
    db.session.add(model3)

    lot1 = LotModel(1, 700000, 25000, 2015,'Red',"Yekaterinburg")
    lot2 = LotModel(1, 750000, 35000, 2012,'Grey',"Yekaterinburg")
    lot3 = LotModel(3,1250000, 35000, 2018,'Yellow',"Yekaterinburg")
    db.session.add(lot1)
    db.session.add(lot2)
    db.session.add(lot3)
    db.session.commit()


@app.route("/index")
@app.route("/")
def index():
    lots=LotModel.query.all()
    labels=AutolabelModel.query.all()
    return render_template('index.html', lots=lots,labels=labels)



@app.route("/index/create", methods=['post','get'])
def lot_create_user():
    if request.method=="GET":
        models = AutomodelsModel.query.all()
        return render_template('lot_create.html',models=models)
    if request.method=="POST":
        model_name=request.form['model']
        model = AutomodelsModel.query.filter_by(label=model_name).first()
        price=request.form['price']
        mileage=request.form['mileage']
        prod_year=request.form['prod_year']
        color=request.form['color']
        location = request.form['location']
        if 'file' not in request.files:
            flash("No file part")
            return render_template('lot_create.html')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template('lot_create.html')
        if file:
            file.save(os.path.join(f"static/img/labels", f"{model_name}.png"))
        lot = LotModel(model.id, price, mileage,prod_year, color, location)
        db.session.add(lot)
        db.session.commit()
        return redirect("/lots")


@app.route("/labels")
def label_list():
    labels=AutolabelModel.query.all()
    return render_template('labels.html', autolabels=labels)

@app.route("/labels/<l_id>")
def label(l_id):
    label = AutolabelModel.query.filter_by(id=l_id).first()
    return render_template('label.html', autolabel=label)

@app.route("/labels/create", methods=['post','get'])
def label_create():
    if request.method=="GET":
        return render_template('label_create.html')
    if request.method=="POST":
        label_name=request.form['label']
        country = request.form['country']
        f_year=request.form['f_year']
        l_year=request.form['l_year']
        if l_year=="":
            l_year=None
        if 'file' not in request.files:
            flash("No file part")
            return render_template('label_create.html')
        file=request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template('label_create.html')
        if file:
            file.save(os.path.join(f"static/img/labels", f"{label_name}.png"))
        label = AutolabelModel(label_name, country, f_year,l_year)
        db.session.add(label)
        db.session.commit()
        return redirect("/labels")


@app.route("/models")
def model_list():
    models=AutomodelsModel.query.all()
    return render_template('models.html', automodels=models)

@app.route("/models/<m_id>")
def model(m_id):
    model = AutomodelsModel.query.filter_by(id=m_id).first()
    return render_template('model.html', automodel=model)

@app.route("/models/create", methods=['post','get'])
def model_create():
    if request.method=="GET":
        return render_template('model_create.html')
    if request.method=="POST":
        label_name=request.form['label']
        producer = request.form['producer']
        f_year=request.form['f_year']
        l_year=request.form['l_year']
        if l_year=="":
            l_year=None
        model = AutomodelsModel(label_name, producer, f_year,l_year)
        db.session.add(model)
        db.session.commit()
        return redirect("/models")

@app.route("/lots")
def lots_list():
    lots=LotModel.query.all()
    return render_template('lots.html', autolots=lots)

@app.route("/lots/<l_id>")
def lot(l_id):
    lot = LotModel.query.filter_by(id=l_id).first()
    return render_template('lot.html', autolot=lot)

@app.route("/lots/create", methods=['post','get'])
def lot_create_admin():
    if request.method=="GET":
        models = AutomodelsModel.query.all()
        return render_template('lot_create.html',models=models)
    if request.method=="POST":
        model_name=request.form['model']
        model = AutomodelsModel.query.filter_by(label=model_name).first()
        price=request.form['price']
        mileage=request.form['mileage']
        prod_year=request.form['prod_year']
        color=request.form['color']
        location = request.form['location']
        if 'file' not in request.files:
            flash("No file part")
            return render_template('lot_create.html')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template('lot_create.html')
        if file:
            file.save(os.path.join(f"static/img/labels", f"{model_name}.png"))
        lot = LotModel(model.id, price, mileage,prod_year, color, location)
        db.session.add(lot)
        db.session.commit()
        return redirect("/lots")

@app.route("/api/index/update/<label>")
def update_main(label):
    label_id=AutolabelModel.query.filter_by(label=label).first().id
    models=AutomodelsModel.query.filter_by(prod_id=label_id).all()
    lots=[]
    for model in models:
        lots.extend(LotModel.query.filter_by(model_id=model.id).all())
    print(lots)
    labels = AutolabelModel.query.all()
    return render_template('index.html', lots=lots, labels=labels)


@app.route("/api/index/updatemodel/<model>")
def update_main1(model):
    models=AutomodelsModel.query.filter_by(label=model).first_or_404()
    lots=LotModel.query.filter_by(model_id=models.id).all()
    print(lots)
    labels = AutolabelModel.query.all()
    return render_template('index.html', lots=lots, labels=labels)

app.run()