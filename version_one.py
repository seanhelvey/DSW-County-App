import json
from time import perf_counter_ns
from functools import reduce
from flask import Flask, render_template, request, Markup

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

""" 
traditional approach with several for loops and using string concatenation.
"""

with open('county_demographics.json') as demographics_data:
    counties = json.load(demographics_data)

def get_unique_states(counties):
    # one way to get the unique states is using a for loop.
    unique_states = []
    for county in counties:
        if county["State"] not in unique_states:
            unique_states.append(county["State"])
    return unique_states

def get_fun_fact_for_state(counties, state):
    # here is another example using a for loop.
    land_area = 0
    for county in counties:
        if county["State"] == state:
            land_area += county["Miscellaneous"]["Land Area"]
    return land_area

def markup_unique_states_with_option_tags(unique_states):
    # a for loop could be used here to process all of the states. notice the string formatting.
    state_options_list = []
    for state in unique_states:
        state_options_list.append("<option value=\"" + state + "\">" + state + "</option>")
    sorted_options_list = sorted(state_options_list)
    options_string = "".join(sorted_options_list)
    options_html = Markup(options_string)
    return options_html

@app.route("/")
def render_main():
    # we can call the function below to create a unique list of states.
    unique_states = get_unique_states(counties)
    unique_states_html = markup_unique_states_with_option_tags(unique_states)
    return render_template('home.html', dropdown = unique_states_html)

@app.route("/response")
def render_response():
    state = request.args['state']
    # we can call the function below to get the fun fact for the chosen state.
    fact = get_fun_fact_for_state(counties, state)
    return render_template('response.html', state=state, fact=f"{fact:,.0f}")
    
if __name__=="__main__":
    app.run(debug=False, port=54321)