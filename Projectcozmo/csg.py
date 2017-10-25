import cozmo
from flask import Flask, render_template, request, url_for
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
  print(message1)   
  return render_template('cozmo.html', name=name, message1 = message1,sent_pic = sent_pic,sent_lo = sent_lo)

@app.route('/try')
def tried():
  return render_template('try.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    