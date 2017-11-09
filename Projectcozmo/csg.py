import cozmo
from flask import Flask, render_template, request, url_for
from multiprocessing import Pool
from func import remember_face
cozmo.run_program(remember_face.cozmo_program, use_3d_viewer=False, use_viewer=False)
app = Flask(__name__)
message1=[]
#key words for location and picture
sent_pic = {'pic','picture','photo','photoes'}
sent_lo  = {'location','locate',}

#main webpage
@app.route('/', methods=["GET", "POST"])
def Cozmo(name='name'):
  if request.method == 'POST':
     message1.append(request.form['Msg'])  
  return render_template('cozmo.html', name=name, message1 = message1,sent_pic = sent_pic,sent_lo = sent_lo)

@app.route('/list', methods=["GET", "POST"])
def List(name='name'):
  return render_template('list.html', name=name, fa = remember_face.faces_mem)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    