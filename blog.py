from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import secrets
import string

app = Flask(__name__)


def generate_secret_key(length=32):
    """Generate a random secret key."""
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secret_key


random_secret_key = generate_secret_key()
app.secret_key = random_secret_key


class BlogPost:
    def __init__(self, title, content, author, date_posted):
        self.title = title
        self.content = content
        self.author = author
        self.date_posted = date_posted


blog_posts = []


@app.route('/')
def home():
    return render_template('home.html', posts=blog_posts)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        date_posted = datetime.now()
        new_post = BlogPost(title, content, author, date_posted)
        blog_posts.append(new_post)
        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_post.html')


@app.route('/post/<int:index>')
def view_post(index):
    post = blog_posts[index]
    return render_template('post.html', post=post)


# Additional Features


# Enable users to delete their own posts
@app.route('/delete_post/<int:index>')
def delete_post(index):
    del blog_posts[index]
    return redirect(url_for('home'))


# Break down larger functions into smaller ones
def create_post(title, content, author):
    date_posted = datetime.now()
    new_post = BlogPost(title, content, author, date_posted)
    blog_posts.append(new_post)


# Apply proper error handling techniques
@app.route('/edit_post/<int:index>', methods=['GET', 'POST'])
def edit_post(index):
    try:
        post = blog_posts[index]
        if request.method == 'POST':
            post.title = request.form['title']
            post.content = request.form['content']
            post.author = request.form['author']
            return redirect(url_for('view_post', index=index))
        return render_template('edit_post.html', post=post)
    except IndexError:
        flash('Post not found!', 'error')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
