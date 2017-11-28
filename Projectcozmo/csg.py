import cozmo
import os
from flask import Flask, render_template, request, url_for,redirect
from flask import send_from_directory
from werkzeug import secure_filename
import COZMO_FULL_VERSION
from multiprocessing import Process
import multiprocessing


UPLOAD_FOLDER = './participants'
ANOTHER_FOLDER = './Intruder_image'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
listpic = os.listdir(r'''C:\Users\PAWEE\Desktop\COZMO-try\Projectcozmo\participants''')
unknown = os.listdir(r'''C:\Users\PAWEE\Desktop\COZMO-try\Projectcozmo\Intruder_image''')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ANOTHER_FOLDER'] = ANOTHER_FOLDER 
message1=[]


#key words in the console
sent_pic = {'pic','picture','photo','photoes'}
sent_lo  = {'location','locate',}
add_pe = {'people','add','add people'}
operate = {'operation', 'operate'}
reset = {'reset'}
kill = {'kill'}


#format that alowed? maybe don't need it
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#picture
@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  
#another pic
@app.route('/up/<filename>')
def up_file(filename):
    return send_from_directory(app.config['ANOTHER_FOLDER'],filename)  
                                                                                            
#main webpage
@app.route('/', methods=["GET", "POST"])
def Cozmo(name='name'):
  if request.method == 'POST':
     message1.append(request.form['Msg'])
     if message1[-1].split(' ')[0] in add_pe:
         with open('C:/Users/PAWEE/Desktop/COZMO-try/Projectcozmo/name_peo.txt',"a+") as file:
              file.write(str(message1[-1].split(' ')[1])+" ")
         #run code for add pic         
         t1 = Process(target=cozmo.run_program, args=(COZMO_FULL_VERSION.remember_face, True))
         t1.daemon = True
         t1.start()
         #cozmo.run_program(COZMO_FULL_VERSION.remember_face, use_viewer=True)
     elif message1[-1] in operate:
       #run code for operation  
         t2 = Process(target=cozmo.run_program, args=(COZMO_FULL_VERSION.inside_conference, True))
         t2.daemon = True
         t2.start()
        #cozmo.run_program(COZMO_FULL_VERSION.inside_conference, use_viewer=True)
     elif message1[-1] in reset:
       #run code for delete all in for:
         t3 = Process(target=cozmo.run_program, args=(COZMO_FULL_VERSION.erase_all, True))
         t3.daemon = True
         t3.start()         
         #cozmo.run_program(COZMO_FULL_VERSION.erase_all, use_viewer=True)
     elif message1[-1] in kill:
       #run code for delete all in for:
         for p in multiprocessing.active_children():
             p.terminate()
         

  return render_template('cozmo.html', name=name, message1 = message1,sent_pic = sent_pic,sent_lo = sent_lo, add_pe = add_pe, operate =operate )

@app.route('/list', methods=["GET", "POST"])
def List(name='name'):
  listpic = os.listdir(r'''C:\Users\PAWEE\Desktop\COZMO-try\Projectcozmo\participants''')
  unknown = os.listdir(r'''C:\Users\PAWEE\Desktop\COZMO-try\Projectcozmo\Intruder_image''')
  return render_template('list.html', name=name ,listpic = listpic, unknown= unknown)

@app.route('/run', methods=["GET", "POST"])
def Run(name='name'):
  p=open_program("") 
  time.sleep(3)
  close_program(p)
  return None

