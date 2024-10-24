from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MEME_FOLDER'] = 'memes/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Assurer que les dossiers existent
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MEME_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_meme', methods=['POST'])
def create_meme():
    # Vérifier si le fichier est dans la requête
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    text = request.form.get('text', '')

    # Si l'utilisateur n'a pas sélectionné de fichier
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Ouvrir l'image et ajouter du texte
        img = Image.open(filepath)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', size=90) 

        # Utiliser textbbox pour obtenir la taille du texte
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Ajouter du texte au centre avec la couleur bleue
        position = ((img.width - text_width)/2, (img.height - text_height)/2)
        draw.text(position, text, (87, 174, 231), font=font)

        # Enregistrer le mème
        meme_filename = f"meme_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        meme_path = os.path.join(app.config['MEME_FOLDER'], meme_filename)
        img.save(meme_path)

        return render_template('meme.html', meme_image=meme_filename)

    else:
        return redirect(request.url)

@app.route('/memes/<filename>')
def send_meme(filename):
    return send_from_directory(app.config['MEME_FOLDER'], filename)

@app.route('/gallery')
def gallery():
    memes = os.listdir(app.config['MEME_FOLDER'])
    memes = [meme for meme in memes if allowed_file(meme)]
    return render_template('gallery.html', memes=memes)

if __name__ == '__main__':
    app.run(debug=True)
