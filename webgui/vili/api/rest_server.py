from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello World!'

@app.route('/test_album_title')
def test_album_title():
  return '{"album": "This is the album name)"}'

@app.route('/test_return_toc')
def test_return_toc():
    file = open('/tmp/media_metadata/toc.json', 'r')
    #web.header('Access-Control-Allow-Origin', '*')
    return file.read()

#requires album metadata in tmp folder
@app.route('/album_details')
def album_details():
  user_data=1
  #user_data = web.input(id=1)
  #file = open('"/tmp/media_metadata/album_" + user_data.id + ".json"', 'r')
  file = open('/tmp/media_metadata/album_' + user_data + '.json', 'r')
  return file.read()
  #return user_data.id

if __name__ == '__main__':
    app.debug = True
#    app.run(host='0.0.0.0')
    app.run()
