import json
from time import perf_counter_ns
from functools import reduce
from flask import Flask, render_template, request, Markup

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

""" 
a more efficient approach using the dictionary data structure to avoid multiple loops.
our fun fact is the chosen state's total land area.
we want to create a dictionary that looks like this where each state maps to the total land area.
state_fact_dictionary = {
    'AL': 50645,
    'AK': 570640,
    ... 
}
"""

state_fact_dictionary = {}

with open('county_demographics.json') as demographics_data:
    counties = json.load(demographics_data)

def markup_unique_states_with_option_tags(unique_states):
    # a "list comprehension" can be used here as an alternative to a for loop.
    # this example also uses newer python string formatting called f-strings.
    state_options_list = [f"<option value='{state}'>{state}</option>" for state in unique_states]
    sorted_options_list = sorted(state_options_list)
    options_string = "".join(sorted_options_list)
    options_html = Markup(options_string)
    return options_html

def get_state_fact_dictionary(counties):
    # if we already have this data, no need to process everything again, just return it.
    if state_fact_dictionary:
        return state_fact_dictionary
    else:
        # populate the dictionary in one loop instead of looping multiple times for the state list and fun fact.
        for county in counties:
            if county["State"] in state_fact_dictionary:
                state_fact_dictionary[county["State"]] += county["Miscellaneous"]["Land Area"]
            else:
                state_fact_dictionary[county["State"]] = county["Miscellaneous"]["Land Area"]
    return state_fact_dictionary

@app.route("/")
def render_main():
    # we can call the function below to create a dictionary of states and facts.
    state_fact_dictionary = get_state_fact_dictionary(counties)
    unique_states_html = markup_unique_states_with_option_tags(state_fact_dictionary.keys())
    return render_template('home.html', dropdown = unique_states_html)

@app.route("/response")
def render_response():
    state = request.args['state']
    # if we chose to create a dictionary instead, then we can get the fun fact from it here.
    fact = state_fact_dictionary[state]
    return render_template('response.html', state=state, fact=f"{fact:,.0f}")
    
if __name__=="__main__":
    app.run(debug=False, port=54321)