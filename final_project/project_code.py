from flask import Flask, render_template, request, redirect, url_for, session
from bs4 import BeautifulSoup
from fatsecret import Fatsecret
import requests
import json
import os
import plotly
import plotly.express as px
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('welcome.html')


@app.route('/preference', methods=['POST', 'GET'])
def index():
    return render_template('user_preference.html')


@app.route('/handle_form', methods=['POST', 'GET'])
def handle_form():
    headers = {'Authorization': 'Bearer %s' % 'boovLwU4BPpx-X7tEPWSbQvHQkkAGp_g3lHxukYM9SAGtgWpkrkRc-VKL-HddKAAU34rF84x_2Ji301y470F6GwaXjAxUMtslVfNsamfSpLbkiuPDllhszvP3AxOYnYx'}

    user_address = request.form["address"]  # str
    food_types_list = request.form.getlist('like_types')    # list
    food_price = request.form["price"]  # str

    food_types = ",".join(food_types_list).lower()  # convert list into str
    base_url = "https://api.yelp.com/v3/businesses/search?location="+user_address+"&categories="+food_types+"&price="+food_price
    resp_address = requests.get("https://api.yelp.com/v3/businesses/search?location="+user_address+"&categories="+food_types+"&price="+food_price, headers=headers)
    json_str = resp_address.text    # JSON string
    # json.loads(json_str) is a dictionary
    info_list = json.loads(json_str)['businesses']  # list of dictionary

    global table_name
    table_name = "table_"+user_address
    if os.path.exists(table_name):
        os.remove(table_name)

    with open(table_name, "w") as final:
        json.dump(info_list, final)
    return redirect(url_for('process_data'))

def isLeaf(tree):
    parent = tree[0]
    left_child = tree[1]
    right_child = tree[2]
    if left_child is None and right_child is None:
        return True
    else:
        return False

def playLeaf(tree):
    parent = tree[0]
    left_child = tree[1]
    right_child = tree[2]
    return parent

def simplePlay(tree):
    parent = tree[0]
    left_child = tree[1]
    right_child = tree[2]
    if isLeaf(tree) is False:
        print(parent)
        ans = input("Your answer: ")
        if ans.lower() == "yes":
            return simplePlay(left_child)
        if ans.lower() == "no":
            return simplePlay(right_child)
    else:
        return playLeaf(tree)

def printTree(tree, prefix = '', bend = '', answer = ''):
    """Recursively print a 20 Questions tree in a human-friendly form.
       TREE is the tree (or subtree) to be printed.
       PREFIX holds characters to be prepended to each printed line.
       BEND is a character string used to print the "corner" of a tree branch.
       ANSWER is a string giving "Yes" or "No" for the current branch."""
    text, left, right = tree
    if left is None  and  right is None:
        print(f'{prefix}{bend}{answer}It is {text}')
    else:
        print(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree(left, prefix, '+-', "Yes: ")
        printTree(right, prefix, '`-', "No:  ")


@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    open_file = open(table_name, "r")
    a = json.loads(open_file.read())
    open_file.close()
    a_sort_dist = sorted(a, key=lambda x: x['distance'])

    flag = True
    # try:
    while flag:

        Tree = \
            ("Do you have specific restaurant?",
             ("Is it " + a_sort_dist[0]['name'] +"?",
              ('I got it', None, None),
              ('distance?',
               ('Adjust distance for you', None, None),
               ('rating?', ('Adjust rating for you', None, None),
                ('Delivery?', ('select delivery for you', None, None), ('select pickup for you', None, None))))),
             (redirect('/preference'), None, None))

        # printTree(Tree)
        output = simplePlay(Tree)

        if output == 'I got it':
            session['alias'] = a_sort_dist[0]['alias']
            session['name'] = a_sort_dist[0]['name']
            return redirect(url_for('menu'))
        elif output.split()[1] == 'distance':
            a_sort_dist.pop(0)
        elif output.split()[1] == 'rating':
            a_sort_dist.pop(0)
            a_sort_dist = sorted(a_sort_dist, key=lambda x: (-x['rating'], x['distance']))
        elif output.split()[1] == 'delivery':
            a_sort_dist.pop(0)
            a_sort_dist = list(filter(lambda i: i['transactions'] == ['delivery'] or i['transactions'] == ['delivery', 'pickup'], a_sort_dist))
        elif output.split()[1] == 'pickup':
            a_sort_dist.pop(0)
            a_sort_dist = list(filter(lambda i: i['transactions'] == ['pickup'] or i['transactions'] == ['delivery', 'pickup'], a_sort_dist))

    # except:
    #     redirect(url_for('/preference'))



@app.route('/menu')
def menu():
    alias = session['alias']
    restaurant_name = session['name']
    menu_url = "https://www.yelp.com/menu/"+alias

    resp = requests.get(menu_url)
    bs = BeautifulSoup(resp.text, 'html.parser')
    menu_all = bs.find_all('h4')
    menu_list = []
    for d in menu_all:
        one_dish = d.text.strip()
        menu_list.append(one_dish)

    return render_template('menu_list.html', menu_list=menu_list, restaurant_name = restaurant_name)


@app.route('/handle_menu', methods=['POST'])
def dishes():
    selected_dishes = request.form.getlist('dish')

    fs = Fatsecret(consumer_key='97bfcb08999645158c288ba91346f5c6',
                           consumer_secret='ac06fa6b3aa249e1b3b88242c6ffd7e1')

    nutri_name = ['Calories', 'Fat', 'Carbs', 'Protein']
    nutri_all = []
    dish_name = []
    total = []
    for i in range(len(selected_dishes)):
        dish = selected_dishes[i]
        # one_name = fs.foods_search(dish)[0]['food_name']
        one_description = fs.foods_search(dish)[0]['food_description']
        one_nutrition = one_description.split(" - ")
        nutri_all.append(one_nutrition)
        one_nutri = one_nutrition[1]
        one_nutri_list = one_nutri.split(" | ")
        total.append(one_nutri_list)
        dish_name.append(dish)

    nutri_dict_text = dict(zip(dish_name, nutri_all))

    nutri_values = [[float(ele[0].split(' ')[1][:-4]) for ele in total],
                    [float(ele[1].split(' ')[1][:-1]) for ele in total],
                    [float(ele[2].split(' ')[1][:-1]) for ele in total],
                    [float(ele[3].split(' ')[1][:-1]) for ele in total]]
    nutri_dict = dict(zip(nutri_name, nutri_values))


    session['cal'] = nutri_dict['Calories']
    session['fat'] = nutri_dict['Fat']
    session['car'] = nutri_dict['Carbs']
    session['pro'] = nutri_dict['Protein']
    session['num'] = len(nutri_dict['Calories'])
    session['name'] = dish_name
    session['nutrition'] = nutri_dict_text

    print("Would you like to see the nutrition information from a histogram? If no,the information will show up in the text form.")
    info_format = input("Your answer: ")
    if info_format.lower() == "yes":
        return redirect('dish_info')
    if info_format.lower() == "no":
        return redirect('dish_info_text')



@app.route('/dish_info')
def info():
    cal = session['cal']
    fat = session['fat']
    car = session['car']
    pro = session['pro']
    num = session['num']
    name = session['name']

    df = pd.DataFrame({
        'Nutrition': ['Calories']*num + ['Fat']*num + ['Carbs']*num + ['Protein']*num,
        'Amount': cal + fat + car + pro,
        'Dishes': name*4
    })

    fig = px.bar(df, x='Nutrition', y='Amount', color='Dishes',
                 barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('nutrition_info.html', graphJSON=graphJSON)

@app.route('/dish_info_text')
def info_text():
    name = session['name']
    nutrition = session['nutrition']
    nutri_all_list = [ele for ele in list(nutrition.values())]
    total_list = list(zip(name, nutri_all_list))

    return render_template('nutrition_info_text.html', total_list=total_list)



if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)