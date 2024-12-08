from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Game, Developer, Platform, Review
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)


with app.app_context():
    db.create_all()
    if not User.query.first():
        admin = User(username='admin', password=generate_password_hash('password'))
        db.session.add(admin)
        db.session.commit()

# Authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')



@app.route('/games')
def games():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    games = Game.query.all()
    return render_template('games.html', games=games)

@app.route('/games/add', methods=['GET', 'POST'])
def add_game():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    developers = Developer.query.all()
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        release_date = datetime.strptime(request.form['release_date'], '%Y-%m-%d')
        developer_id = request.form['developer_id']
        game = Game(title=title, genre=genre, release_date=release_date, developer_id=developer_id)
        db.session.add(game)
        db.session.commit()
        flash('Game added successfully!', 'success')
        return redirect(url_for('games'))
    return render_template('add_game.html', developers=developers)

@app.route('/games/edit/<int:id>', methods=['GET', 'POST'])
def edit_game(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    game = Game.query.get(id)
    developers = Developer.query.all()
    if request.method == 'POST':
        game.title = request.form['title']
        game.genre = request.form['genre']
        game.release_date = datetime.strptime(request.form['release_date'], '%Y-%m-%d')
        game.developer_id = request.form['developer_id']
        db.session.commit()
        flash('Game updated successfully!', 'success')
        return redirect(url_for('games'))
    return render_template('edit_game.html', game=game, developers=developers)

@app.route('/games/delete/<int:id>')
def delete_game(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    game = Game.query.get(id)
    db.session.delete(game)
    db.session.commit()
    flash('Game deleted successfully!', 'success')
    return redirect(url_for('games'))



# CRUD for Developers
@app.route('/developers')
def developers():
    developers = Developer.query.all()
    return render_template('developers.html', developers=developers)

@app.route('/developers/add', methods=['GET', 'POST'])
def add_developer():
    if request.method == 'POST':
        name = request.form['name']
        founded = request.form['founded']
        headquarters = request.form['headquarters']
        developer = Developer(name=name, founded=founded, headquarters=headquarters)
        db.session.add(developer)
        db.session.commit()
        flash('Developer added successfully!', 'success')
        return redirect(url_for('developers'))
    return render_template('add_developer.html')

@app.route('/developers/edit/<int:id>', methods=['GET', 'POST'])
def edit_developer(id):
    developer = Developer.query.get(id)
    if request.method == 'POST':
        developer.name = request.form['name']
        developer.founded = request.form['founded']
        developer.headquarters = request.form['headquarters']
        db.session.commit()
        flash('Developer updated successfully!', 'success')
        return redirect(url_for('developers'))
    return render_template('edit_developer.html', developer=developer)

@app.route('/developers/delete/<int:id>')
def delete_developer(id):
    developer = Developer.query.get(id)
    db.session.delete(developer)
    db.session.commit()
    flash('Developer deleted successfully!', 'success')
    return redirect(url_for('developers'))

# CRUD for Platforms
@app.route('/platforms')
def platforms():
    platforms = Platform.query.all()
    return render_template('platforms.html', platforms=platforms)

@app.route('/platforms/add', methods=['GET', 'POST'])
def add_platform():
    if request.method == 'POST':
        name = request.form['name']
        manufacturer = request.form['manufacturer']
        release_year = request.form['release_year']
        platform = Platform(name=name, manufacturer=manufacturer, release_year=release_year)
        db.session.add(platform)
        db.session.commit()
        flash('Platform added successfully!', 'success')
        return redirect(url_for('platforms'))
    return render_template('add_platform.html')

@app.route('/platforms/edit/<int:id>', methods=['GET', 'POST'])
def edit_platform(id):
    platform = Platform.query.get(id)
    if request.method == 'POST':
        platform.name = request.form['name']
        platform.manufacturer = request.form['manufacturer']
        platform.release_year = request.form['release_year']
        db.session.commit()
        flash('Platform updated successfully!', 'success')
        return redirect(url_for('platforms'))
    return render_template('edit_platform.html', platform=platform)

@app.route('/platforms/delete/<int:id>')
def delete_platform(id):
    platform = Platform.query.get(id)
    db.session.delete(platform)
    db.session.commit()
    flash('Platform deleted successfully!', 'success')
    return redirect(url_for('platforms'))

# CRUD for Reviews
@app.route('/reviews')
def reviews():
    reviews = Review.query.all()
    return render_template('reviews.html', reviews=reviews)

@app.route('/reviews/add', methods=['GET', 'POST'])
def add_review():
    games = Game.query.all()
    if request.method == 'POST':
        game_id = request.form['game_id']
        rating = request.form['rating']
        review_text = request.form['review_text']
        reviewer_name = request.form['reviewer_name']
        review = Review(game_id=game_id, rating=rating, review_text=review_text, reviewer_name=reviewer_name)
        db.session.add(review)
        db.session.commit()
        flash('Review added successfully!', 'success')
        return redirect(url_for('reviews'))
    return render_template('add_review.html', games=games)

@app.route('/reviews/edit/<int:id>', methods=['GET', 'POST'])
def edit_review(id):
    review = Review.query.get(id)
    games = Game.query.all()
    if request.method == 'POST':
        review.game_id = request.form['game_id']
        review.rating = request.form['rating']
        review.review_text = request.form['review_text']
        review.reviewer_name = request.form['reviewer_name']
        db.session.commit()
        flash('Review updated successfully!', 'success')
        return redirect(url_for('reviews'))
    return render_template('edit_review.html', review=review, games=games)

@app.route('/reviews/delete/<int:id>')
def delete_review(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('reviews'))

if __name__ == '__main__':
    app.run(debug=True)
