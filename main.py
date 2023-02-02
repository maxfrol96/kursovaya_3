import requests
import datetime

URL = 'https://www.jsonkeeper.com/b/45XD'

class transaction:
    def __init__(self, trans_date, trans_desc, trans_from, trans_to, trans_amount, trans_curr):
        self.trans_date = trans_date
        self.trans_desc = trans_desc
        self.trans_from = trans_from
        self.trans_to = trans_to
        self.trans_amount = trans_amount
        self.trans_curr = trans_curr

    def blur_from(self):
        if self.trans_from == 'Данные об отправителе отсутствуют':
            card = 'Данные об отправителе отсутствуют'
        else:
            if self.trans_from[0:4] == 'Счет':
                len_number = 20
            else:
                len_number = 16
            card_number = self.trans_from[len(self.trans_from) - len_number:len(self.trans_from)]
            card_name = self.trans_from.replace(card_number, '')
            if len_number == 16:
                card_number = card_number[0:6] + '******' + card_number[12:16]
                card_number = ' '.join(card_number[i * 4:(i + 1) * 4] for i in range(4))
            else:
                card_number = '****************' + card_number[16:20]
                card_number = ' '.join(card_number[i * 4:(i + 1) * 4] for i in range(5))
            card = card_name + card_number
        return card

    def blur_to(self):
        if self.trans_to[0:4] == 'Счет':
            len_number = 20
        else:
            len_number = 16
        card_number = self.trans_to[len(self.trans_to) - len_number:len(self.trans_to)]
        card_name = self.trans_to.replace(card_number, '')
        if len_number == 16:
            card_number = card_number[0:6] + '******' + card_number[12:16]
            card_number = ' '.join(card_number[i * 4:(i + 1) * 4] for i in range(4))
        else:
            card_number = '****************' + card_number[16:20]
            card_number = ' '.join(card_number[i * 4:(i + 1) * 4] for i in range(5))
        card = card_name + card_number
        return card

    def get_date(self):
        trans_date = datetime.datetime.strptime(self.trans_date, '%Y-%m-%dT%H:%M:%S.%f')
        return trans_date.date()

    def info(self):
        return f'{transaction.get_date(self)} {self.trans_desc}\n' \
               f'{transaction.blur_from(self)} -> {transaction.blur_to(self)}\n' \
               f'{self.trans_amount} {self.trans_curr}\n'

transactions_list = sorted(
    requests.get(URL).json(),
    key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True
)

last_5_trans = []

for trans in transactions_list:
    if trans['state'] == 'EXECUTED':
        if 'from' in trans:
            last_5_trans.append(transaction(trans['date'], trans['description'], trans['from'], trans['to'],
                                            trans['operationAmount']['amount'],
                                            trans['operationAmount']['currency']['name']))
        else:
            last_5_trans.append(transaction(trans['date'], trans['description'], 'Данные об отправителе отсутствуют',
                                            trans['to'], trans['operationAmount']['amount'],
                                            trans['operationAmount']['currency']['name']))
    if len(last_5_trans) == 5:
        for trans in last_5_trans:
            print(trans.info())
        break

