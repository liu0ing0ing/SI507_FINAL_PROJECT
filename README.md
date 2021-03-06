# SI507_FINAL_PROJECT

### Running code instruactions

API: </br>
  - All my API keys are provided in my code(project_code.py). There is no special operations to access API keys. Just run the code. </br>

Instruction of interaction: </br>
  - STEP 1: (prompts) Run the code, click the link in the command line prompts. It will direct you to a webpage(Welcome page). </br>
  - STEP 2: (HTML) Click the link, "Let us know your preference!", to fill out the form. </br>
  - STEP 3: (HTML) You can enter your address, the food types you want to eat, and the price level you can accept, to let the program know your preference. </br>
  - STEP 4: (HTML) Click "Submit Form", and turn back to the command line prompts. </br>
  - STEP 5: (prompts) A question will show, follow the instruction and answer it. </br>
  - STEP 6: (HTML) After choosing a restaurant, the menu will show as HTML. Select the dishes you want to eat and click "Submit Form". </br>
  - STEP 7: (prompts) Back to the command line prompts, it will ask you whether you want to see the nutritional information in a plot or in text format. </br>
  - STEP 8: (prompts) Enter "yes" to see a plot; enter "no" to see the information in text form. Both of them will show as HTML. </br></br>


notes: </br>
  - After STEP 5, a json file of the tree(tree_json.json) will be written out. Use read_tree_json.py to read it. </br></br>


### Data structure description

  - Data will be in a tree data structure, which looks like this.
![alt_text](https://github.com/liu0ing0ing/SI507_FINAL_PROJECT/blob/main/tree.png?raw=true)</br>
  - After STEP4, collecting users’ preferences, we have cached data, which will be stored as a JSON file. The data is ordered based on the distance from the restaurant to the user’s address. We will first ask the user if they want to go to the first restaurant, which is the nearest one, listed in the JSON file. If the answer is “yes”, the webpage of the restaurant will show up. If the answer is “no”, the first row will be deleted and the program will ask which parameter(distance, rating score, price, transactions) that the user wants to adjust. </br></br>


