#Kütüphaneler
from flask import Flask, render_template,request, redirect, url_for, session
#Bulmaca kütüphanesi (quiz.py'ye bak)
from quiz import Quiz, Question
#Veritabanı kütüphanesi
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "deneme_ortami"

#Soruları ekleme 
#Ayrıntılar: 1. parametre: Question("[Sorulacak soru]"), 2. parametre: Liste halinde olası cevaplar, 3. parametre: index şekilinde doğru cevap (mesela 2. mümkün cevap soğru ise bu parametre 1 olur çünkü index 0'dan başlar).
quiz = Quiz() #<-- Bu satır Quiz() sınıfının bir instanceını oluşturur.
quiz.add_question(Question("Küresel ısınmanın önde gelen nedeni nedir?", ["Sera gazlarının normalden yüksek derecede atmosfere salınımı.", "Kloroflorokarbonlar gibi gazların atmosferde azalması."], 0))
quiz.add_question(Question("Birinci soru'dan yola çıkarak sence küresel ısınma nasıl engellenebilir?", ["Hayvanların çıkardığı atık gazlarını azaltmak için çiftçiliği azaltmak.", "Ağaçların havaya saldığı gazlardan dolayı ağaçlandırma çalışmalarını azaltmak.", "Arabaların ve sanayi tesislerinin atmosfere yaydığı sera gazlarını azaltmak."], 2))
#quiz.add_question(Question("Sence küresel ısınma çevreye uyguladığı hangi farklılıklardan dolayı engellenmesi önemli bir olay?"), ["Küresel ısınma ismine karşın havayı soğuttuğu için insanlar daha fazla soğuk algınlığı geçiriyor, ismindeki ısınmanın nedeni ise hastanelerin insanların vücut ısısıyla ısınması anlamına geliyor.", "Küresel ısınma çevreyi daha sıcak hale getirdiği için doğanın dengesi bozuluyor ve insanlar da bu olaydan etkileniyor.", "Küresel ısınma sadece daire yani küre şeklindeki ülkeleri etkiliyor. Bu ülkeler dünya'nın ekonomisini kontrol ettiği için oradaki insanların sıcaklamaması önemli."], 1)


@app.route("/")
def index():
	session["current_question"] = 0
	session["score"] = 0	
	
	return redirect(url_for("quiz_view"))

@app.route("/quiz/", methods=["GET", "POST"])
def quiz_view():
	if request.method == "POST":
		selected_option = request.form.get("option")
		current_question_index = session.get("current_question")
		if selected_option is not None:
			correct_option = quiz.questions[current_question_index].correct_option
			
			if int(selected_option) == correct_option:
				session["score"] += 1
				
				
		session["current_question"] += 1
		#Eğer kullanıcı quiz.questions listesindeki elemanların sayısını aştıysa onu puan sayfasına yönlendirme:
		if session["current_question"] >= len(quiz.questions):
			return redirect(url_for("results"))
		
	current_question_index = session.get("current_question")
	question = quiz.questions[current_question_index]
	
	return render_template("quiz.html", question=question)

@app.route("/results")
def results():
	score = session.get("score")
	total_questions = len(quiz.questions)
	
	return render_template("results.html", score=score, total_questions=total_questions)


if __name__ == "__main__":
	app.run(debug=True)