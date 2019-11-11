from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator

class Menu:

    def __init__(self):
        self.style = style_from_dict({
            Token.Separator: '#cc5454',
            Token.QuestionMark: '#673ab7 bold',
            Token.Selected: '#cc5454',  # default
            Token.Pointer: '#0087ff bold',
            Token.Instruction: '',  # default
            Token.Answer: '#f44336 bold',
            Token.Question: '',
        })

    def checkbox_menu(self, menu_items):
        items = self.checkbox_selection_items(menu_items)
        questions = self.checkbox_selections(items)
        selected = prompt(questions, style=self.style)
        return selected

    def checkbox_selections(self, selections):
        questions = [
            {
                'type': 'checkbox',
                'message': 'Select Item',
                'name': 'Items',
                'choices': selections,
                'validate': lambda answer: 'Select at least one part'
                if len(answer) == 0 else True
            }
        ]
        return questions

    def checkbox_selection_items(self, data):
        response = []
        for i in data:
            response.append({'name': i})
        return response