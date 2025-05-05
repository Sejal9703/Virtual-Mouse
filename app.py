# from flask import Flask, render_template, redirect, url_for
# import subprocess

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/eye_mouse')
# def eye_mouse():
#     return render_template('eye_mouse.html')

# @app.route('/start_eye')
# def start_eye():
#     subprocess.Popen(['python', 'workingeyemouse.py'])
#     return redirect(url_for('eye_mouse'))

# @app.route('/hand_gesture')
# def hand_gesture():
#     return render_template('hand_gesture.html')

# @app.route('/start_hand')
# def start_hand():
#     subprocess.Popen(['python', 'handgesture.py'])
#     return redirect(url_for('hand_gesture'))

# @app.route('/voice_control')
# def voice_control():
#     return render_template('voice_control.html')

# @app.route('/start_voice')
# def start_voice():
#     subprocess.Popen(['python', 'voice.py'])
#     return redirect(url_for('voice_control'))

# if __name__ == '__main__':
#     app.run(debug=True)
