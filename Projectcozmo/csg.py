#import some file
import cozmo
from flask import Flask, render_template, request, url_for

#create new flask named "app" and new list named "message"
app = Flask(__name__)
message1=[]

#key words for location and picture
sent_pic = {'pic','picture','photo','photoes'}
sent_lo  = {'location','locate',}

#main webpage (run when it found '/' in the url)
@app.route('/', methods=["GET", "POST"])
def Cozmo(name='name'):
  #when in found 'post' it will add that message in to the list(message1)
  if request.method == 'POST':
     message1.append(request.form['Msg'])
  #run cozmo.html file    
  return render_template('cozmo.html', name=name, message1 = message1,sent_pic = sent_pic,sent_lo = sent_lo)

#main(run the program)
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    
