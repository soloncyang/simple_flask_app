from flask import Flask, request, render_template, redirect, url_for
from random import randint
app = Flask(__name__)
variant_dict = {}
@app.route("/", methods = ['POST', 'GET'])
def get_utm_page():
    global variant_dict #realistically this would just be a memcached server instead of a python dictionary
    if request.method == 'POST':
        page = request.form.get('page_type')
        if not page:
            #redirect to get
            redirect(url_for("get_utm_page"))
        if variant_dict.get(page):
            variant_dict[page] += 1
        else:
            variant_dict[page] = 1
        return render_template('test_page.html', page=request.form.get('page_type'))
    else:
        utm_id = request.args.get('utm_id')
        #pick abc or cde. random. 0 = a or c, 1 = b or d, 2= c or e
        choice = randint(0,2)
        page_var = None
        if utm_id == '1':
            choices = ['A'] * (1+variant_dict.get('A', 0))\
                + ['B']  * (1+variant_dict.get('B', 0))\
                + ['C']  * (1+variant_dict.get('C', 0))
        elif utm_id == '2':
            choices = ['C']  * (1+variant_dict.get('C', 0))\
                + ['D']  * (1+variant_dict.get('D', 0))\
                + ['E']  * (1+variant_dict.get('E', 0))
        else:
            page_var = 'F' #if nothing is passed in, we'll just display f
        if not page_var:
            length = len(choices)
            choice = randint(0, length-1)
            page_var = choices[choice]
    
        return render_template('test_page.html', page=page_var)

if __name__ == "__main__":
    app.run()
