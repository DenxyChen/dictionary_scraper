from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, validators
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SECRET_KEY'] = 'thisisatopsecretsforme'
db = SQLAlchemy(app)


##################### DATABASE SETUP ####################################

class courses(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    num = db.Column(db.String(length=30), nullable=False, unique=False)
    name = db.Column(db.String(length=30), nullable=False, unique=False)

    def __repr__(self):
        return '[courses {}]'.format(self.num)


class reviews(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    num = db.Column(db.String(length=30), nullable=True, unique=False)
    review = db.Column(db.String(length=30), nullable=False, unique=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))


    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {'id': self.id, 'num': self.num, 'review': self.review, 'course_id': self.id}


#########################################################################

############################### FORMS ###################################

def choice_query():
    return courses.query


class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label='num')


class PostForm(Form):
    course_num = StringField(label='Title:')
    content = TextAreaField('Content', [validators.DataRequired()])


##########################################################################


############################# ADD REVIEW SERVICE ##########################

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    form = PostForm(request.form)
    if request.method == "POST":
        post = reviews(num=request.form["word"], review=request.form["review"])
        db.session.add(post)
        db.session.commit()
        flash('Your review has been added ', 'success')
        return redirect(url_for('courses_page'))
    return render_template('add_review.html', form=form)

@app.route('/get_reviews/<string:id>')
def get_reviews(id):
    try:
        all_reviews = reviews.query.filter(reviews.num == id).all()
        return jsonify(all_reviews=[i.serialize for i in all_reviews])
    except AttributeError:
        return {"all_reviews": [{"id": id, "review": ""}]}

@app.route('/get_all_reviews')
def get_all_reviews():
    all_reviews = reviews.query.all()
    return jsonify(all_reviews=[i.serialize for i in all_reviews])
###########################################################################


if __name__ == '__main__':
    app.run(debug=True)
