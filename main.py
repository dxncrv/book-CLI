import os, csv, json, datetime

def preflight():
    consolidate_data_csv()
    if not os.path.isfile('data.json'):
        create_data_json()

def consolidate_data_csv():
    list_csv = get_list_csv()
    if len(list_csv) != 0:
        new_data_csv = []
        for i in list_csv:
            with open( i, 'r') as f:
                data = list(csv.reader(f))
            for row in data:
                if len(row) == 5:
                    row[4] = 'cc'
                    new_data_csv.append(row)
            if 'interest' in str(data).lower():
                for row in data:
                    row.append('sav')
                    new_data_csv.append(row)
            else:
                for row in data:
                    if len(row) == 4:
                        row.append('chk')
                        new_data_csv.append(row)
        new_data_csv = sorted(new_data_csv, key = lambda i: i[0], reverse=True)
        new_data_csv.insert(0, ['date','description','debit','credit','account'])
        if not os.path.isfile('data.csv'):
            with open('data.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerows(new_data_csv)
            print ('oh yea, we talkin now...')
            del_csvs()
        else:
            with open('data.csv', 'r') as f:
                reader = csv.reader(f)
                data_csv = list(reader)
                old_data_csv = []
                for row in data_csv:
                    if row != []:
                        old_data_csv.append(row)
                diff = []
                for row in new_data_csv:
                    if row not in old_data_csv:
                        diff.append(row)
                if len(diff) != 0:
                    for row in new_data_csv:
                        if row not in old_data_csv:
                            old_data_csv.append(row)
                    new_data_csv = old_data_csv
                    new_data_csv = sorted(new_data_csv, key = lambda i: i[0], reverse=True)
                    with open('data.csv', 'w') as f:
                        writer = csv.writer(f)
                        writer.writerows(new_data_csv)
                        print('nice, new stuff added...')
                        del_csvs()
                else:
                    print('''shit fam, we already covered that. 
trashing files...''')
                    del_csvs()
    elif os.path.isfile('data.csv'):
        pass
    else:
        print('give me csv files, dawg...')    

# HELPERS #
def create_data_json():
    with open('data.json', 'w+') as f:
        f.write('{"debited":[],"credited":[]}')
def del_csvs():
    list_csv = get_list_csv()
    for i in list_csv:
        if i != 'data.csv':
            os.remove(i)
def get_list_csv():
    list_csv = []
    for file in os.listdir():
        if file.startswith('cibc') and file.endswith('.csv'):
            list_csv.append(file)
    return list_csv

def val_date(date):
    try:
        if datetime.datetime.strptime(date, '%Y-%m-%d').date():
            return True
    except ValueError:
        return False

def val_desc(desc):
    desc_list = []
    with open('data.csv', 'r') as f:
        data = list(csv.reader(f))
        for row in data[1:]:
            if row != []:
                desc_list.append(row[1])
    for row in desc_list:
        if desc in row.lower():
            return row

# JSON CALs #
def cal_balance():
    with open('data.json', 'r') as f:
        data = json.load(f)
    balance = 0
    for i in data['debited']:
        balance -= float(i['amount'])
    for i in data['credited']:
        balance += float(i['amount'])
    print ('balance: ' + "%.2f" % round(balance, 2))
def cal_entries_total():
    total = 0
    with open('data.json', 'r') as f:
        data = json.load(f)
    for i in data['debited']:
        total += 1
    for i in data['credited']:
        total += 1
    print('entries: ' + str(total))
def cal_cashback():
    cb = 0
    with open('data.json', 'r') as f:
        data = json.load(f)
        for i in data['credited']:
            if 'cashback' in i['description'].lower():
                cb += float(i['amount'])
    if cb != 0:
        print('cashback: ' + "%.2f" % round(cb, 2))
def cal_interest():
    interest = 0
    with open('data.json', 'r') as f:
        data = json.load(f)
        for i in data['credited']:
            if 'interest' in i['description'].lower():
                interest += float(i['amount'])
    if interest != 0:
        print('interest: ' + "%.2f" % round(interest, 2))

# ESSENTIALS #
def add_entry():
    os.system('cls' if os.name == 'nt' else 'clear')
    new_entry = ['', '', '', '', '']
    print('''YYYY-MM-DD 
or [x] to cancel''')
    user_input = ''
    while new_entry[0] == '':
        if user_input == 'x':
            break
        else:
            user_input = input('date > ')
            if val_date(user_input):
                new_entry[0] = user_input
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in new_entry:
        if i != '':
            print(i, end=' , ')
    print ('''enter description 
or [x] to cancel''')
    while new_entry[1] == '':
        if user_input == 'x':
            break
        else:
            desc = input('search > ')
            if desc == 'x':
                user_input = 'x'
                break
            elif val_desc(desc):
                print (val_desc(desc))
                user_input = input('confirm? [y/n] > ')
                if user_input == 'y' or user_input == '':
                    new_entry[1] = val_desc(desc)
            elif val_desc(desc) == None:
                user_input = input('not found, add? [y/n] > ')
                if user_input == 'y' or user_input == '':
                    new_entry[1] = desc
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in new_entry:
        if i != '':
            print(i, end=' , ')
    print('''debit or credit?  
or [x] to cancel''')
    while new_entry[2] == '' and new_entry[3] == '':
        if user_input == 'x':
            break
        else:
            user_input = input('[d] or [c] > ').lower()
            if user_input == 'd':
                new_entry[2] = input('amount > ')
            elif user_input == 'c':
                new_entry[3] = input('amount > ')
            else:
                pass
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in new_entry:
        if i != '':
            print(i, end=' , ')
    print('''account? [chk], [sav], [cc] 
or [x] to cancel''')
    while new_entry[4] == '':
        if user_input == 'x':
            break
        else:
            user_input = input('acct > ').lower()
            if any(x in user_input for x in ['chk', 'sav', 'cc']):
                new_entry[4] = user_input
    os.system('cls' if os.name == 'nt' else 'clear')
    print(', '.join(new_entry))
    if user_input != 'x':
        user_input = input('proceed? [y/n] > ')
        if user_input == 'y' or user_input == '':
            with open('data.csv', 'r') as f:
                data = list(csv.reader(f))
            data.insert(1, new_entry)
            with open('data.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            print('entry added')
        else:
            print ('canceled')
    else:
        print('canceled')
    main()

def pop_json(choice):
    with open('data.json', 'r') as f:
        data = json.load(f)
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        data_csv = list(reader)[1:]
        data_csv = [i for i in data_csv if i != []]
        if choice == 'chk':
            data_csv = [i for i in data_csv if i[4] == 'chk']
        if choice == 'sav':
            data_csv = [i for i in data_csv if i[4] == 'sav']
        if choice == 'cc':
            data_csv = [i for i in data_csv if i[4] == 'cc']
        pop_debited(data_csv, data)
        pop_credited(data_csv, data)
    with open('data.json', 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)
def pop_debited(data_csv, data):
    pop_list_deb = []
    for row in data_csv:
        if row != []:
            if row[2] != '':
                if {'date':row[0], 'description':row[1], 'amount':row[2]} not in data['debited']:
                    pop_list_deb.append({'date':row[0], 'description':row[1], 'amount':row[2]})
    for i in pop_list_deb:
        data['debited'].append(i)
        data['debited'] = sorted(data['debited'], key = lambda i: i['date'])
def pop_credited(data_csv, data):
    pop_list_cre = []
    for row in data_csv:
        if row != []:
            if row[3] != '':
                if {'date':row[0], 'description':row[1], 'amount':row[3]} not in data['credited']:
                    pop_list_cre.append({'date':row[0], 'description':row[1], 'amount':row[3]})
    for i in pop_list_cre:
        data['credited'].append(i)
        data['credited'] = sorted(data['credited'], key = lambda i: i['date'])

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        preflight()
        if os.path.isfile('data.csv'):    
            cal_balance()
            cal_entries_total()
            cal_cashback()
            cal_interest()
            print('')
            print ('[net], [chk], [sav], [cc]')
            if os.path.isfile('data.csv'):
                print('[a] - add entry')
            print ('[x] - exit')
            choice = input('> ').lower()
            if choice == 'net' or choice == 'chk' or choice =='sav' or choice == 'cc':
                create_data_json()
                pop_json(choice)
            if choice == 'a':
                add_entry()
            elif choice == 'x':
                exit()
        else:
            break

if __name__ == '__main__':
    main()