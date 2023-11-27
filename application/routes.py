from flask import render_template, redirect, url_for, flash, request, make_response, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from application import app
from application.models import *
from application.forms import *
from application.utils import save_image, parse_date, get_user, flash_errors


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CreatePostForm()

    if form.validate_on_submit():
        post = Post(
            author_id=current_user.id,
            caption=form.caption.data,
            photo=save_image(form.post_pic.data, 'posts')
        )

        db.session.add(post)
        db.session.commit()
        flash('Your image has been posted!', 'success')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    posts = Post.query\
        .order_by(Post.post_date.desc())\
        .paginate(page=page, per_page=3)
    
    flash_errors(form)
    return render_template('index.html', title='Home', form=form, posts=posts, parse_date=parse_date)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/<string:username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    posts = user.posts
    reverse_posts = posts[::-1]
    return render_template('profile.html', title=f'{user.fullname} Profile', posts=reverse_posts, user=user)


@app.route('/<username>/posts')
@login_required
def posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author_id=user.id)\
        .order_by(Post.post_date.desc())\
        .paginate(page=page, per_page=3)
    
    if posts.total == 0:
        flash('This user currently has no posts.', 'error')
        return redirect(url_for('profile', username=username))
    
    return render_template('posts.html', title=f'{user.fullname} Posts', posts=posts, user=user, parse_date=parse_date)


@app.route('/comments/<string:post_id>', methods=["GET", "POST"])
@login_required
def comments(post_id):
    form = PostCommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            commenter_id=current_user.id,
            post_id=post_id,
            text=form.text.data
        )

        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('comments', post_id=post_id))
    
    comments = Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.comment_date.desc())
    
    flash_errors(form)
    return render_template('comments.html', title=f'{post_id} Comments', form=form, comments=comments, parse_date=parse_date, get_user=get_user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))

    form = SignUpForm()
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            fullname=form.fullname.data,
            email=form.email.data,
            password=form.password.data
        )
        
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('profile', username=current_user.username))
    
    flash_errors(form)
    return render_template('signup.html', title='Signup', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('profile', username=current_user.username))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
    
    flash_errors(form)
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.password = form.new_password.data

        if user.password != form.old_password.data:
            flash('Your password is incorrect.', 'error')
            return redirect('reset_password')

        db.session.commit()
        flash('Password changed', 'success')
        logout_user()
        return redirect(url_for('login'))
    
    flash_errors(form)
    return render_template('reset_password.html', title=f'Reset {current_user.fullname} Password', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data

        user = User.query.filter_by(email=email).first()
        return redirect(url_for('verification_reset_password', user_id=user.id))
    
    flash_errors(form)
    return render_template('forgot_password.html', title='Forgot Password', form=form)


@app.route('/verification_reset_password/<string:user_id>', methods=['GET', 'POST'])
def verification_reset_password(user_id):
    form = VerificationResetPasswordForm()

    user = User.query.get(user_id)
    if form.validate_on_submit():
        user.password = form.new_password.data

        db.session.commit()
        flash('Password changed', 'success')
        return redirect(url_for('login'))
    
    flash_errors(form)
    return render_template('verification_reset_password.html', title=f'Verification Reset {user.fullname} Password', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.username = form.username.data
        user.fullname = form.fullname.data
        user.bio = form.bio.data
        
        if form.profile_pic.data:
            user.profile_pic = save_image(form.profile_pic.data, 'profile_pics')

        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('profile', username=current_user.username))

    form.username.data = current_user.username
    form.fullname.data = current_user.fullname
    form.bio.data = current_user.bio

    flash_errors(form)
    return render_template('edit_profile.html', title=f'Edit {current_user.fullname} Profile', form=form)


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        post = Post(
            post_pic=form.post_pic.data,
            caption=form.caption.data
        )
        
        db.session.add(post)
        db.session.commit()
        flash('Your post has been successfully uploaded!', 'success')
        return redirect(url_for('profile', username=current_user.username))
    
    flash_errors(form)
    return render_template('create_post.html', title=f'Create {current_user.fullname} Post', form=form)


@app.route('/edit_post/<string:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = EditPostForm()

    post = Post.query.get(post_id)

    if current_user.id != post.author_id:
        flash('You do not own this post.', 'error')
        return redirect(url_for('profile', username=current_user.username))

    if form.validate_on_submit():
        post.caption = form.caption.data
        
        db.session.commit()
        flash('Your post has been successfully edited!', 'success')
        return redirect(url_for('profile', username=current_user.username))
    
    form.caption.data = post.caption
    
    flash_errors(form)
    return render_template('edit_post.html', title=f'Edit {current_user.fullname} Post', form=form)


@app.route('/like', methods=["GET", "POST"])
@login_required
def like():
    data = request.json
    post_id = int(data['postId'])
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if not like:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return make_response(jsonify({'status': True}), 200)
    
    db.session.delete(like)
    db.session.commit()
    return make_response(jsonify({'status': False}), 200)


@app.route('/follow', methods=["GET", "POST"])
@login_required
def follow():
    data = request.json
    user_id = int(data['userId'])
    relation = Relation.query.filter_by(follower_id=user_id, following_id=current_user.id).first()
    if not relation:
        relation = Relation(follower_id=user_id, following_id=current_user.id)
        db.session.add(relation)
        db.session.commit()
        return make_response(jsonify({'status': True}), 200)
    
    db.session.delete(relation)
    db.session.commit()
    return make_response(jsonify({'status': False}), 200)


if __name__ == '__main__':
    app.run(debug=True)
