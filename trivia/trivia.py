import html
import numpy as np
import os
import pandas as pd
import random
import requests

def make_trivia_game(number_of_categories=5, num_questions_per_category=5):
    category=pd.DataFrame.from_dict(requests.post("https://opentdb.com/api_category.php").json()['trivia_categories'])
    def get_trivia(category_id):
        #&difficult=hard,medium,easy
        request=f'https://opentdb.com/api.php?amount={num_questions_per_category}&category={category_id}&type=multiple'
        return pd.DataFrame.from_dict(requests.post(request).json()['results'])
    trivia=pd.concat(map(get_trivia,category.sample(number_of_categories)['id'].values),axis=0)
    trivia.index=trivia.index+1
    
    
    with open('trivia_slides.md', 'w') as f:
        print(f'# Trivia Game {datetime.date.today().strftime("%b %d %Y")}', file=f)
        print('---',file=f)
        print('',file=f)
        print(f'# Trivia Game {datetime.date.today().strftime("%b %d %Y")}', file=f)
        print(f'Tonights Categories Are:', file=f)
        print('',file=f)
        for idx,(category,_) in enumerate(trivia.groupby('category')['category']):
            print(f'{idx+1}. *{html.unescape(category)}*', file=f)
        print('',file=f)
        print('---',file=f)
        print('',file=f)
        for category, questions in trivia.groupby('category'):
            print(f'# {html.unescape(category)}', file=f)
            print(f'#### Difficulties in this round', file=f)
            for diff,count in questions['difficulty'].value_counts().to_dict().items():
                print(f'- {html.escape(diff)}: {count}', file=f)
            print('',file=f)
            print('---',file=f)
            print('',file=f)
            for (idx,question) in questions.iterrows():
                q=html.unescape(question['question'])
                print(f'# Question {idx}',file=f)
                print(f'##### - **Category**: {html.unescape(category)}',file=f)
                print(f'##### - **Difficulty**: {html.unescape(question["difficulty"])}',file=f)
                print(f'*{q}*',file=f)
                print('',file=f)
                choices=question['incorrect_answers'].copy()
                choices.append(question['correct_answer'])
                random.shuffle(choices)
                for choice in np.unique(choices):
                    c=html.unescape(choice)
                    print(f'1. {c}', file=f)
                print('',file=f)
                print('---',file=f)
                print('',file=f)
            print(f'# ANSWERS: {html.unescape(category)}', file=f)
            #TODO Add an Image?
            print('---',file=f)
            print('',file=f)
            print(f'# ANSWERS: {html.unescape(category)}', file=f)
            for (idx, question) in questions.iterrows():
                q=html.unescape(question['question'])
                a=html.unescape(question['correct_answer'])
                print(f'{idx}. {a}',file=f)
            print('---',file=f)
            print('',file=f)
    
    os.system('darkslide -i trivia_slides.md')

