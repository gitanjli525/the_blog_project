import requests

url = 'http://www.myblogger.codes/'



def test_add_post():
    myobj = {'title': 'somevalue2','tline':"tag",'slug':"test_slg525"
            ,'content':"content",'img_file':"img"}

    x = requests.post(url = url + 'add_post/gitanjli525/0', data = myobj)

def test_add_user():
    myobj = {'uname' : "gitanjli",'email':"abhishekkumar260.ak@gmail.com"}

    x = requests.post(url = url + 'signup', data = myobj)

def test_send_feedback(name,email,phone,message):
    myobj = {'name' : name,'email':email,'phone':phone,'message'
    :message}

    x = requests.post(url = url + 'contact', data = myobj)

# test_add_post()
# test_add_user()
test_send_feedback('HAPPY','SOME@MAIL.COM','9354954597','MY MESSAGE')