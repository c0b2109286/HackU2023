from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///board.db'
db = SQLAlchemy(app)

# データベースのclass
class detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    before = db.Column(db.String, nullable=True)
    after = db.Column(db.String, nullable=True)

#データベースの一番古いデータを削除する
def delete_oldest_row():
    posts = detail.query.all()
    oldest_row = detail.query.order_by(detail.id.asc()).first()
    if oldest_row and len(posts) > 15:
        db.session.delete(oldest_row)
        db.session.commit()

# テキストと絵文字をデータベースに格納
def post_value(before, after):
    if len(before) > 0:
        new_post = detail(before = before, after = after)
        db.session.add(new_post)
        db.session.commit()
        delete_oldest_row()


def generate_alien_reply(user_message, conversion_type):
    import openai
    openai.api_key = "自身のopenaiAPI"
    prompt_text = "入力した文章を全て絵文字のみで返すようにしてアルファベットや日本語を返さないように\n"

    if conversion_type == "emoji_to_text":
        print("emoji_to_text")
        prompt_text = "以下の絵文字の意味を予測して文字（複数個あれば文章）に変換してください。日本語で\n"
        if random.randint(0,2)==0:
            prompt_text = "以下の絵文字の占い結果を出力して"

    else:  # default to text_to_emoji
        prompt_text = "入力した文章を全て絵文字のみで返すようにしてアルファベットや日本語を返さないように\n"
    
    question = user_message
    prompt_text += "You: {}\n".format(question)
    prompt_text += "AI:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_text,
        temperature=0.9,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" You:", " AI:"],
    )
    prompt_text += "AI: {}\n".format(response.choices[0].text)
    #print("AI:", response.choices[0].text)
    return response.choices[0].text

@app.route("/", methods = ["POST", "GET"])
def index():
    after_text = ""

    if request.method == "GET":
        posts = detail.query.all()
        return render_template("main_page.html", posts = posts)
    
    else:
        before_text = request.form.get("post_text", "")
        choice = request.form.get("choice", "")

        if before_text:
            after_text = generate_alien_reply(before_text, choice)
            post_value(before_text, after_text)

        posts = detail.query.all()
        return render_template("main_page.html",before_conversion_text = before_text, after_conversion_text = after_text, posts = posts)


@app.route("/board")
def board():
    posts = detail.query.all()
    return render_template("board.html", posts = posts)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=80)
