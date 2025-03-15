#Kütüphaneler
from flask import Flask, render_template,request, redirect, url_for, session
#Bulmaca kütüphanesi (quiz.py'ye bak)
from quiz import Quiz, Question
#Veritabanı kütüphanesi
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
#from speech import speech_tr

app = Flask(__name__)
#gizli anahtar (ÇOK ÖNEMLİ!!!):
app.secret_key = "deneme_ortami"
#SQLite'a bağlantı
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///diary.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Veritabanı oluşturmak
db = SQLAlchemy(app)
#Tablo oluşturmak

#Görev #1. Veritabanı oluşturmak
class Skor(db.Model):
    #Gerekli alanları oluşturmak
    #Puanımız
    id = db.Column(db.Integer, primary_key=True)
    #Başlık
    skor = db.Column(db.Integer, primary_key=False, nullable=False)
    #Açıklama
    subtitle = db.Column(db.String(300), nullable=False)
    #Yazı
    text = db.Column(db.Text, nullable=False)

    #Objeyi çıktı olarak vermek
    def __repr__(self):
        return f'<Card {self.id}>'

#Bulmacaya sorular ekleme:

quiz = Quiz()
quiz.add_question(Question("Küresel ısınmanın en büyük nedeni nedir?", ["Deneme1", "Deneme2", "Deneme3", "Deneme4"], 3))
quiz.add_question(Question("SORU DENEME2", ["Deneme1", "Deneme2"], 0))

#Sayfayı çalıştırma
@app.route('/')
def index():
    #Veritabanındaki objeleri çıktı vermek
    #Görev #2. Veritabanındaki objelerin index.html içinde gözükmesini sağlamak
    #skorlar = Skor.query.order_by(Skor.id).all()
    session["current_question"] = 0
    session["score"] = 0
    return render_template(url_for("quiz_view"))

@app.route("/quiz", methods=["GET", "POST"])
def quiz_view():
    #Eğer cevap doğruysa puan değişkenimize puan eklemek:
    if request.method == "POST":
        selected_option = request.form.get("option")
        current_question_index = session.get("current_question")
        if selected_option is None:
                correct_option = quiz.questions[current_question_index].correct_option
                if int(selected_option) == correct_option:
                    session["score"] += 1
        #Eğer session bulmacamızdaki soruları aştıysa kullanıcıyı sonuçlar sayfasına atmak:
        session["current_question"] += 1
        if session["current_question"] >= len (quiz.questions):
                return redirect(url_for("results"))
    current_question_index = session.get("current_question")
    question = quiz.question[current_question_index]
    return render_template("quiz.html", question=question, question_index=current_question_index +1, total_questions=len(quiz.questions))

@app.route("/results")
def results():
      score = session.get("score")
      total_questions = len(quiz.questions)
      return f"<h1 style = 'font: menu' >Sonuç: {score}/{total_questions}</h1>"

def form_create():
    if request.method == 'POST':
        skor = request.form['score']

        #Veritabanına paslamak için bir obje oluşturmak

        #Görev #2. Veritabanında veri depolamak için bir yöntem
        skordb = Skor(skor=skor)

        db.session.add(skordb)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('reslults.html')


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	app.run(debug=True)