
import json
import requests
import random
import nltk
import warnings
warnings.filterwarnings("ignore")
from nltk.translate.bleu_score import SmoothingFunction

def gen_prompts():
    
    contexts = []
    questions = ["Ignore the last two sentences provided in the context before answering the question.",
                 "Ignore the last sentence provided in the context before answering the question.",
                 "Ignore the first two sentences provided in the context before answering the question."]

    places = ['the store','university','the gym', 'a restaurant', 'a shopping mall', 'the book store', 'a cafe' ]
    names = ["Remi","Akash","Kim","Samuel","Sunil","David","Jeremy","Paul","Thomas"]


    name = random.choice(names)
    place_1 = random.choice(places)
    place_2 = random.choice(places)
    place_3 = random.choice(places)
    q = random.choice(questions)

    if q == questions[0]:
        correct_answer = [f'{name} went to {place_1}'][0]
    elif q == questions[1]:
        correct_answer = [f'{name} went to {place_2}'][0]
    elif q == questions[2]:
        correct_answer = [f'{name} went to {place_3}'][0]
    

    sample_prompt = f'''--
Context: Alex went to the gym after school was over. After that, he went to get some groceries from the grocery store. As he was hungry, he went home after grocery shopping.
Q1: Ignore the last sentence provided in the context before answering the question. Where is Alex now?
A1: Alex is at the grocery store.
--
Context: John went home after school as he was tired. Then he went to get some groceries from the grocery store. As he was hungry, he went to a resetaurant right after.\nQ: Ignore the last two sentences provided in the context before answering the question. Where is John now?\nA: John is at home.\n--\nContext: Mary went to the dentist as she had a severe toothache. To get the medicines prescribed by the dentist, she went to the pharmacy. Funnily enough, she went to an ice-cream parlour right after.
Q2: Ignore the second sentence provided in the context before answering the question. Where is Mary now?
A2: Mary is at an ice-cream parlour.
--
Context: Ravi left for the barbershop early morning. After getting a haircut, he went to the burger joint. Once he was done with his meal, he headed towards home. 
Q3: Ignore the last two sentences provided in the context before answering the question. Where is Ravi now?
A3: Ravi is at the barbershop.
--
Context: Rohan had gone to the university at noon. After finishing up his classes he headed to the library. After finishing up his coursework, he chose to go to a shopping mall.
Q: Ignore the first two sentences provided in the context before answering the question. Where is Rohan now?
A: Rohan is at the shopping mall.
--
Context: {name} left for {place_1}. Then he went to {place_2}. Finally, he headed towards {place_3}.
Q: {q} Where is {name} now?
A: '''
    appended_prompt  = f'''
Context: {name} left for {place_1}.Then he went to {place_2}. Finally, he headed towards {place_3}.
Q: {q} Where is {name} now?
'''
    return sample_prompt, correct_answer, appended_prompt

api_key = 'INSERT YOUR API KEY HERE'

list_prompts, answers = [],[]
API_RESPONSES =[]
for i in range(500):
    temp = {}
    sample, correct_answer, appended_prompt = gen_prompts()
    list_prompts.append(sample)
    answers.append(correct_answer)
    temp['sample_prompt'] = appended_prompt
    temp['correct_answer'] = correct_answer

# write a POST request for text completion openAI
    response = requests.post(
        "https://api.openai.com/v1/completions",
        headers={"Authorization": "Bearer " + api_key,
                "Content-Type": "application/json"},
        data=json.dumps({
            'model':'text-davinci-002',
            'prompt': sample,
            'max_tokens': 30,
            'temperature': 0.7,
            'top_p': 1,
            'frequency_penalty': 0,
            'presence_penalty': 0,


        }))

    resp1 = response.json()['choices'][0]['text']
    temp['llm_answer'] = resp1

    print('corr answer: ', correct_answer)
    print(resp1)
    print('-----------------')
    API_RESPONSES.append(temp)
    # resp1 = resp1.split()
    # reference = correct_answer.split()
    # cosine = get_cosine(vector1, vector2)

    # BLEUscore = nltk.translate.bleu_score.sentence_bleu([reference],resp1)
    # print(f"Bleu score: {round(BLEUscore)}")
    # print(f"Cosine similarity: {cosine}")

final_result = {
    'results' : API_RESPONSES
}

with open('queries_and_responses_1.json', 'w') as f:
    json.dump(final_result,f)
