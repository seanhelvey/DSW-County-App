import json
from time import perf_counter_ns
from functools import reduce
from flask import Flask, render_template, request, Markup

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

""" 
a more "pythonic" approach with list comprehensions and modern f-string formatting.
"""

with open('county_demographics.json') as demographics_data:
    counties = json.load(demographics_data)

def get_unique_states(counties):
    # a "list comprehension" can be used here as an alternative to a for loop.
    all_states = [county['State'] for county in counties]
    unique_states = list(set(all_states))
    return unique_states

def get_fun_fact_for_state(counties, state):
    # here is another example using a for loop.
    land_area = 0
    for county in counties:
        if county["State"] == state:
            land_area += county["Miscellaneous"]["Land Area"]
    return land_area

def markup_unique_states_with_option_tags(unique_states):
    # a "list comprehension" can be used here as an alternative to a for loop.
    # this example also uses newer python string formatting called f-strings.
    state_options_list = [f"<option value='{state}'>{state}</option>" for state in unique_states]
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
    # now we can call the function below to get the fun fact for the chosen state.
    fact = get_fun_fact_for_state(counties, state)
    return render_template('response.html', state=state, fact=f"{fact:,.0f}")
    
if __name__=="__main__":
    app.run(debug=False, port=54321)