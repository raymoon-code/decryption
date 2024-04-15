from flask import Flask, render_template, request, redirect, url_for, flash,send_file
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'wmv'}


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


global key

def generate_key():
    return Fernet.generate_key()

def load_key(key_file):
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

def encrypt_file(key, input_file, output_file):
    cipher = Fernet(key)
    with open(input_file, 'rb') as f:
        data = f.read()
    encrypted_data = cipher.encrypt(data)
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(key, input_file, output_file):
    cipher = Fernet(key)
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

def enter_password():
    while True:
        password = request.form.get("password")
        if password == "1234":
            return True
        else:
            flash("Incorrect password. Please try again.")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_decryption(key,input_file, output_file):
    # Perform decryption logic here and save the decrypted file to output_file_path
    decrypt_file(key, input_file, output_file)
    flash("File decrypted successfully.")
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form.get("password")
        if password != "1234":
            flash("Incorrect password. Please try again.")
            return redirect(request.url)

        input_file = request.files['input_file']
        if input_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        output_file = request.form.get("output_file")
        action = request.form.get("action")

        if input_file and allowed_file(input_file.filename):
            filename = secure_filename(input_file.filename)
            input_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully')
            
            key_file = 'key.key'
            key = load_key(key_file)
            
            input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_file)

            if action == 'encrypt':
                encrypt_file(key, input_file, output_file)
                flash("File encrypted successfully.")
            elif action == 'decrypt':
                perform_decryption(key,input_file_path, output_file_path)
                flash('File decrypted successfully')
                return send_file(output_file_path, as_attachment=True)
            else:
                flash("Invalid action. Please try again.")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
