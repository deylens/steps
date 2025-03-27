from enum import IntEnum


class States(IntEnum):
    START = 0
    QUESTIONS = 1
    INSTRUCTION = 2
    CHOICE_CHILD = 3
    ADD_CHILD = 4
    ADD_NAME = 5
    ADD_DATE = 6
    RESULT = 7
    HISTORY = 8
    ANONYMOUS = 9
    AGE = 10


DATA = {
    "id_user": None,
    "child": [{"name": "Max", "date": "12.12.2012"}],
    "questions": [
        {
            "name": "First skill",
            "approve": None,
            "creteria": "this is first question",
            "recommendation": "first recommend",
        },
        {
            "name": "Second skill",
            "approve": None,
            "creteria": "this is second question",
            "recommendation": "second recommend",
        },
        {
            "name": "Third skill",
            "approve": None,
            "creteria": "this is third question",
            "recommendation": "third recommend",
        },
    ],
}

TEXT = {
    "greetings": "Приветсвуем Вас! \n"
    "Этот бот предназначен для диагностики и раннего выявления задержек психо-моторного развитя у детей \n"
    "Для перехода к опросу - выберите Диагностика \n"
    "Для дополнительной информации выберете Инструкция",
    "instruction": "Для начала диагностики, на стартовом меню выберете Диагностика \n"
    "Далее Вам предложат: \n"
    "добавить ребенка для отслеживания истории диагностики\n"
    "выбрать ребенка, если вы ранее проходили тестирование\n"
    "а так же можете пройти тестирование анонимно - в таком случае\n"
    "результаты отслеживаться не будут и вы не сможете отслеживать изменения",
    "history": "В данном разделе имеются данные о результатах тестирования \n"
    "пройденных ранее. Для возвращения на стартовую страницу, нажмите Назад",
    "anonymous": "При анонимном прохождении ребенка - данные не сохраняются,\n"
    "и ослеживание истории опроса невозможно",
}
