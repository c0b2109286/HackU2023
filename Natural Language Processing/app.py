from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_message = ""
    alien_reply = ""
    conversion_type = "text_to_emoji"  # default
    if request.method == 'POST':
        user_message = request.form.get('user_message', "")
        conversion_type = request.form.get('conversion_type', "text_to_emoji")
        
        if user_message:  # Check if user_message is not empty
            alien_reply = generate_alien_reply(user_message, conversion_type)
            
    return render_template('index2.html', user_message=user_message, alien_reply=alien_reply)

def generate_alien_reply(user_message, conversion_type):
    import openai
    openai.api_key ="your api key"
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

if __name__ == '__main__':
    app.run(debug=True)
