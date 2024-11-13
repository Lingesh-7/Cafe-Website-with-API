from flask import Flask, jsonify, render_template,url_for,redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from random import choice
from flask import jsonify
from flask_bootstrap import Bootstrap5

from forums import AddCafe,UpdateForm,DeleteForm,Search



app = Flask(__name__)
app.config['SECRET_KEY'] = "FLASK_KEY"
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes_own.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()








@app.route("/")
def home():
    result=db.session.execute(db.select(Cafe))
    all_cafe=result.scalars().all()

    return render_template("index.html",cafes=all_cafe,is_single=False)


@app.route('/wifi')
def cafe_with_wifi():
    result = db.session.execute(db.select(Cafe).where(Cafe.has_wifi == 1)).scalars().all()
    if len(result) ==1:
        return render_template('index.html',cafes=result[0],is_single=True)
    return render_template('index.html',cafes=result,is_single=False)

@app.route('/plugin')
def cafe_with_plugin():
    result = db.session.execute(db.select(Cafe).where(Cafe.has_sockets == 1)).scalars().all()
    if len(result) ==1:
        return render_template('index.html',cafes=result[0],is_single=True)
    return render_template('index.html',cafes=result,is_single=False)

@app.route('/call')
def cafe_with_call():
    result = db.session.execute(db.select(Cafe).where(Cafe.can_take_calls == 1)).scalars().all()
    if len(result) ==1:
        return render_template('index.html',cafes=result[0],is_single=True)
    return render_template('index.html',cafes=result,is_single=False)

@app.route('/toilet')
def cafe_with_toilet():
    result = db.session.execute(db.select(Cafe).where(Cafe.has_toilet == 1)).scalars().all()
    if len(result) ==1:
        return render_template('index.html',cafes=result[0],is_single=True)
    return render_template('index.html',cafes=result,is_single=False)

@app.route('/seat')
def cafe_with_seats():
    result = db.session.execute(db.select(Cafe).where(Cafe.has_toilet == 1)).scalars().all()
    if len(result) ==1:
        return render_template('index.html',cafes=result[0],is_single=True)
    return render_template('index.html',cafes=result,is_single=False)




@app.route("/random")
def get_random_cafe():
    cafes=db.session.execute(db.select(Cafe)).scalars().all()
    random_cafes=choice(cafes)
    return render_template("index.html",cafes=random_cafes,is_single=True) 


    

@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("search")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    # Note, this may get more than one cafe per location
    all_cafes = result.scalars().all()
    if all_cafes:
        # all_cafes_list=[]
        # for i in all_cafes:
        #     all_cafes_list.append({
        #     "can_take_calls":i.can_take_calls,
        #     "coffee_price":i.coffee_price,
        #     "has_sockets":i.has_sockets,
        #     "has_toilet":i.has_toilet,
        #     "has_wifi":i.has_wifi,
        #     "id":i.id,
        #     "img_url":i.img_url,
        #     "location":i.location,
        #     "map_url":i.map_url,
        #     "name":i.name,
        #     "seats":i.seats,
        #         })
        # return jsonify(cafes=all_cafes_list)
        if len(all_cafes)==1:
            return render_template('index.html',cafes=all_cafes[0],is_single=True)
        return render_template('index.html',cafes=all_cafes,is_single=False)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route("/add",methods=["GET","POST"])
def add_cafe():
    add_form=AddCafe()
    if add_form.validate_on_submit():
        new_cafe=Cafe(
            name=add_form.name.data,
            map_url=add_form.map_url.data,
            img_url=add_form.img_url.data,
            location=add_form.location.data,
            has_sockets=bool(add_form.sockets.data),
            has_toilet=bool(add_form.toilets.data),
            has_wifi=bool(add_form.wifi.data),
            can_take_calls=bool(add_form.call.data),
            seats=add_form.seats.data,
            coffee_price=add_form.price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_new.html",form=add_form)


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record
@app.route("/update-price",methods=["GET","POST"])
def update_price():
    update_form=UpdateForm()
    if update_form.validate_on_submit():
        # new_price=request.form.get("new_price")
        get_cafe=update_form.creditenls.data
        cafe_searched=db.get_or_404(Cafe,get_cafe)
        if cafe_searched:
            new_price=update_form.price.data
            cafe_searched.price=new_price
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return render_template("index.html")
    return render_template("update.html",form=update_form)



# # HTTP DELETE - Delete Record
API_KEY="ithuku-key-eh-theva_illa"
@app.route("/report-closed",methods=["GET","POST"])
def delete_cafe():
    delete_from=DeleteForm()
    if delete_from.validate_on_submit():
        given_api_key=delete_from.creditals.data
        
        if given_api_key==API_KEY:
            cafe_id=delete_from.ids.data
            searching_cafe=db.get_or_404(Cafe,cafe_id)
            if searching_cafe:
                # delete_cafe_=db.session.execute(db.select(Cafe).where(Cafe.id==cafe_id)).scalar()
                db.session.delete(searching_cafe)
                db.session.commit()
                return jsonify(Sucess="Deleted the Cafe"),200
            else:
                return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}),404

    return render_template("delete.html",form=delete_from)


if __name__ == '__main__':
    app.run(debug=True)
