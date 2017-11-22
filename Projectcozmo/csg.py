import cozmo
import os
import subprocess
import time
from flask import Flask, render_template, request, url_for,redirect
from flask import send_from_directory
from werkzeug import secure_filename
from func import remember_face
UPLOAD_FOLDER = './people pic'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
listpic = os.listdir(r'''C:\Users\PAWEE\Desktop\multi upload case\people pic''')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
message1=[]
#key words for location and picture
sent_pic = {'pic','picture','photo','photoes'}
sent_lo  = {'location','locate',}

def open_program(path_name):
    return subprocess.Popen(path_name)
def close_program(p):
    p.terminate() 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)  
                               
#main webpage
@app.route('/', methods=["GET", "POST"])
def Cozmo(name='name'):
  if request.method == 'POST':
     message1.append(request.form['Msg'])

  return render_template('cozmo.html', name=name, message1 = message1,sent_pic = sent_pic,sent_lo = sent_lo)

@app.route('/list', methods=["GET", "POST"])
def List(name='name'):
  listpic = os.listdir(r'''C:\Users\PAWEE\Desktop\Github\Cozmo-Test\people pic''')
  return render_template('list.html', name=name, fa = remember_face.faces_mem,listpic = listpic)

@app.route('/run', methods=["GET", "POST"])
def Run(name='name'):
  p=open_program("") 
  time.sleep(3)
  close_program(p)
  return None

