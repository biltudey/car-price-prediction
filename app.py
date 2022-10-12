
import re
from flask import *
import pickle
import numpy as np
import pandas as pd
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
name = pd.read_csv('name.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
    result_dict =  request.form
    our_dict = {}
    for key,value in result_dict.items():
        our_dict[key]= value
    # print(our_dict)
    for key ,value in our_dict.items():
        #seller_type
        print(key,value)
        if value == 'Individual':
            our_dict[key]= 1
            print(our_dict[key])
        if value == 'Dealer':
            our_dict[key]= 0
        if value == 'Trustmark':
            our_dict[key]= 2
        # fuel
        if value == 'Diesel':
            our_dict[key]= 1
        if value == 'Petrol':
            our_dict[key]= 3
        if value == 'CNG':
            our_dict[key]= 0
        if value == 'LPG':
            our_dict[key]= 2
        
        # transmission
        if value == 'Manual':
            our_dict[key]= 1
        if value == 'Automatic':
            our_dict[key]= 0
        #owner
        if value == 'First Owner':
            our_dict[key]= 0
        if value == 'Second Owner':
            our_dict[key]= 2
        if value == 'Third Owner':
            our_dict[key]= 4
        if value == 'Fourth & Above Owner':
            our_dict[key]= 1
        if value == 'Test Drive Car':
            our_dict[key]= 3
    # print(key,value)

    
    result = [float(x) for x in our_dict.values()]
    
    arr  = [np.array(result)]
    output = model.predict(arr)
    output = round(output[0],0)
    s = name['selling_price'].between(output-20000,output+20000)
    car = list(name[s].sort_values(by='selling_price',ascending=False)[:5]['name'].values)


    return render_template('index.html',submit_value=output,car=car)


if __name__ == '__main__':
    app.run(debug=True)