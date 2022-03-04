import selenium.webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from glob import glob
import os

import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# from helper import *

driver = selenium.webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://lichess.org/analysis")
#clicks the opening button
driver.find_elements_by_tag_name('button')[1].click()

#new design, clicking the Lichess from the 3 choices masters, lichess, player

# time.sleep(3)

driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.data > div > button:nth-child(2)')[0].click()
# time.sleep(1)
driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > button')[0].click()
# time.sleep(1)
driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(2) > section.speed > div > button:nth-child(1)')[0].click()
# time.sleep(1)
driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(2) > section.speed > div > button:nth-child(2)')[0].click()
# time.sleep(1)
driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(2) > section.rating > div > button:nth-child(1)')[0].click()
# time.sleep(1)
driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(2) > section.rating > div > button:nth-child(2)')[0].click()
# time.sleep(1)
driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(2) > section.rating > div > button:nth-child(3)')[0].click()
# time.sleep(1)


# driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div.explorer-title > button:nth-child(2)')[0].click()

# #the wheel
# #driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > span')[0].click()
# time.sleep(3)
# driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > button')[0].click()

# #chooses Lichess
# driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > section.db > div > button:nth-child(2)')[0].click()
current_selection = 'Lichess'

# #chooses Masters
# #driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > section.db > div > button:nth-child(1)')[0].click()
# #current_selection = 'Masters'

# #unlight 1600
# driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(3) > section.rating > div > button:nth-child(1)')[0].click()

# #unlight 1800
# driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(3) > section.rating > div > button:nth-child(2)')[0].click()

# #unlight 2000
# driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(3) > section.rating > div > button:nth-child(3)')[0].click()

# #unlight 2500
# #driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(3) > section.rating > div > span:nth-child(5)')[0].click()

# #unlight bullet
# driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(3) > section.speed > div > button:nth-child(1)')[0].click()

#unlight rapid
#driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(3) > section.speed > div > span:nth-child(3)')[0].click()

#unlight classical
#driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > div:nth-child(3) > section.speed > div > span:nth-child(4)')[0].click()

driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > button')[0].click()



def pickle_nodes_and_fens(name):
    f = open(name, 'wb')
    p = pickle.Pickler(f)

    for node in Node.all_nodes:
        p.dump(node)
    p.dump(Node.fens)
    f.close()

def load_nodes_and_fens(name):
    f = open(name, 'rb')
    up = pickle.Unpickler(f)

    all_nodes = []
    while True:
        try:
            all_nodes.append(up.load())
        except:
            break
    fens = all_nodes[-1]
    all_nodes = all_nodes[:-1]
    return all_nodes,fens

def str_to_arr_and_back(a):
    #a function that switches between pgn and a path and vice versa, interesting kind of function
    if type(a)==str:
        #pgn, convert it to a path array and return it
        x = a.split()
        return [i.split('.')[1] if n%2==0 else i.split('.')[0] for n,i in enumerate(x) ]
    if type(a)==list:
        #path moves array
        str_path = ''
        for i in range(len(a)):
            if i%2==0:
                token = '{}.{} '.format((i//2+1),a[i])
            else:
                token = '{} '.format(a[i])
            str_path+=token
        return str_path.strip()
def read_or_write_to_file(name,write = False):
    if write:
        pickle_nodes_and_fens(name)
        #df = pd.DataFrame([(i.prob,i.pgn) for i in Node.all_nodes],columns = ['prob','pgn'])
        #df.to_csv(name,index = False)
    else:
        #if read
        a,b = load_nodes_and_fens(name)
        Node.all_nodes = a
        Node.fens = b
        #Node.all_nodes = []
        #Node.fens = {}
        #pgns = [i for i in pd.read_csv(name)['pgn']]
        #probs = [i for i in pd.read_csv(name)['prob']]
        #for i in range(len(probs)):
        #    Node(parent = None,prob = probs[i],move = None,pgn = pgns[i],root = True)

    
def get_pos_from_pgn(pgn,driver = '',variant = False):
    if variant:
        prefix = '[Variant "{}"] '.format(variant)
        pgn = prefix+pgn
    command = "document.querySelectorAll('textarea')[0].value='{}'".format(pgn)

    fail_counter = 0
    #assume initial failure to get into the loop
    fail = True
    while fail:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea")))
        try:
            driver.execute_script(command)
            fail = False
        except:
            fail_counter+=1
            time.sleep(1)
            print('slept in get_pos_from_pgn part 1')
            #driver.execute_script(command)

    #click the import pgn button
    # driver.execute_script("document.querySelectorAll('#lichess > div > div.underboard > div.center > div > div > div > button')[0].click()")
    driver.execute_script('document.querySelectorAll("#main-wrap > main > div.analyse__underboard > div > div.pgn > div > button")[0].click()')

    fail_counter = 0
    #assume initial failure to get into the loop
    fail = True
    while fail:
        wait = WebDriverWait(driver, 10)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea")))
        try:
            driver.execute_script(command)
            fail = False
        except:
            fail_counter+=1
            time.sleep(1)
            print('slept in get_pos_from_pgn part 2')

            #driver.execute_script(command)

    driver.execute_script('document.querySelectorAll("#main-wrap > main > div.analyse__underboard > div > div.pgn > div > button")[0].click()')

def get_fen(driver):
    complete_fen = driver.find_elements_by_css_selector('div.analyse__underboard > div > div.pair > input')[0].get_attribute('value')
    my_fen = ' '.join(complete_fen.split(' ')[:2])
    return my_fen
    

def get_move(current_node):
    return input('\nenter your move please. {}'.format(current_node.pgn))

def sort_nodes():
    Node.all_nodes = sorted(Node.all_nodes,key = lambda x:x.prob,reverse = True)


class Node:
    all_nodes = []
    fens = {}
    def __init__(self,parent,prob,move,root = False,pgn = '',fen='',copy = False, local_prob=1):
        self.root = root
        self.prob = prob
        self.local_prob = local_prob
        self.children = []
        self.move = move
        self.parent = parent
        self.fen = ''
        
        if pgn:
            self.pgn = pgn
        else:
            if root==True:
                self.pgn = ''
            else:
                if parent.pgn!='':
                    path_list = str_to_arr_and_back(parent.pgn)
                    path_list.append(move)
                    self.pgn = str_to_arr_and_back(path_list)
                if parent.pgn == '':
                    #its root node
                    self.pgn = str_to_arr_and_back([move])
        if copy==False:
            Node.all_nodes.append(self)
            Node.all_nodes = sorted(Node.all_nodes,key = lambda x:x.prob,reverse = True)

    def update_children_probs(self,prob_inc):
        #either increase by providing an increment, or by providing the new probability right away
        self.prob += prob_inc
        for child in self.children:
            child.update_children_probs(child.local_prob * prob_inc)
        

        
    def __repr__(self):
        return self.pgn+' '+str(self.prob)
    
    def copy(self):
        children = self.children
        new_node = Node(parent = self.parent,prob = self.prob,move = self.move,root = self.root,pgn = self.pgn,copy = True)
        new_node.children = children
        return new_node
    
    def move_(self,move):
        self.pgn = str_to_arr_and_back(str_to_arr_and_back(self.pgn)+[move])

    def create_node(self,move):
        root = False
        new_node = Node(self.parent,self.prob,move,root = root)
        print('length of all_node: {}'.format(len(Node.all_nodes)))
        
    def create_nodes(self):
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody")))
        #time.sleep(1)
        tbody = driver.find_elements_by_tag_name('tbody')[0]
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody > tr")))
        trs = tbody.find_elements_by_tag_name('tr')
        #to remove the sigma
        if len(trs)>1:
            trs = trs[:-1]
        counts = [int(row.text.split(' ')[-1].split('\n')[0].replace(',','')) for row in trs]
        sum_ = sum(counts)
        probs = [i/sum_ for i in counts]
        moves = [tr.text.split(' ')[0] for tr in trs]
        root = False
        nodes = [ Node(self,probs[i]*self.prob,moves[i],root = root, local_prob = probs[i]) for i in range(len(probs))]
        self.children = nodes

#for naming and organizing files
opening_identifier = input('\n Please enter the opening identifier: Also Remember to set the rating and lichess users instead of masters.')
#if opening_identifier in ['']

variant = False
my_turn = False

start_pos = '1.e4 c6 2.d4 d5 3.e5'
start_pos = '1.c4 Nf6 2.Nc3 c5 3.d4 cxd4 4.Qxd4 Nc6'

Node.all_nodes = []
root = Node(None,1,'',root = True,pgn = start_pos)



def output_state(state_counter):
    df = pd.DataFrame([(i.prob,i.pgn) for i in states[-1]],columns = ['prob','pgn'])
    df.to_csv('{}/states/{}.csv'.format(opening_identifier,state_counter),index = False)

def load_states():
    try:
        states = []
        last_state_number = sorted([int(i.split('/')[-1].split('.')[0]) for i in glob('{}/states/*'.format(opening_identifier))])[-1]
        for state in glob('{}/states/*'.format(opening_identifier)):
            pgns = [i for i in pd.read_csv(state)['pgn']]
            probs = [i for i in pd.read_csv(state)['prob']]
            temp_state = []
            for i in range(len(probs)):
                temp_state.append( Node(parent = None,prob = probs[i],move = None,pgn = pgns[i],root = True ,copy = True))
            states.append(temp_state)    
    except:
        last_state_number = 0
        states = []
        raise
    return last_state_number,states

#for regular chess
# variant = False

#or
# variant = 'Crazyhouse'

try:
    os.mkdir(opening_identifier)
    os.mkdir('{}/states'.format(opening_identifier))
except:
    pass

file_name = "{}/{}".format(opening_identifier,opening_identifier)

try:
    state_counter,states = load_states()
except:
    state_counter,states = 0,[]

# time.sleep(1)

def load_last_n(n = -1):
    try:
        f = glob('{}/*.csv'.format(opening_identifier,opening_identifier))
        sorted_f = sorted(f, key = lambda x : int(x.split('/')[-1].split('.')[0].split('_')[-1]))
        read_or_write_to_file(sorted_f[n])
        loaded = True
        counter = int(sorted_f[n].split('/')[-1].split('.')[0].split('_')[-1])
    except:
        # raise
        loaded = False
        counter = 0
    return loaded, counter


loaded, loop_counter = load_last_n()

get_pos_from_pgn(Node.all_nodes[0].pgn,driver = driver,variant = variant)
time.sleep(2)

# loop_counter = 0

if not loaded:
    if not my_turn:
        root.create_nodes()
        Node.all_nodes.pop(0)
        print(Node.all_nodes)
while True:
    loop_counter += 1
    try:
        #time.sleep(1)
        current_node = Node.all_nodes.pop(0)
        try:
            get_pos_from_pgn(current_node.pgn,driver = driver,variant = variant)
        except:
            time.sleep(1)
            print('slept in main loop id1')
            try:
                get_pos_from_pgn(current_node.pgn,driver = driver,variant = variant)
            except:
                raise

        fen = get_fen(driver)
        if fen in Node.fens.keys():
            print("\n\nseen before\n\n")
            old_node = Node.fens[fen]
            old_node.update_children_probs(current_node.prob)
            #old_node.prob += current_node.prob
            sort_nodes()
            continue
        else:
            Node.fens[fen] = current_node

        print(('{:.4f}%'.format((1-current_node.prob)*100)))

        move = input('enter your move please. {} '.format(current_node.pgn))
        if move=='exit':
            break
        if move =='undo':
            load_last_n(-2)
            loop_counter -=1
            continue
        if move == 'pdb':
            import pdb; pdb.set_trace();

        if move == 'skip':
            continue

        if move == 'f':
            #the wheel
            # driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > button')[0].click()
            if current_selection == 'Masters':
                #chooses Lichess
                driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.data > div.explorer-title > button:nth-child(2)')[0].click()
                # driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > section.db > div > button:nth-child(2)')[0].click()
                current_selection = 'Lichess'
            else:
                #chooses Masters
                # driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.config > section.db > div > button:nth-child(1)')[0].click()
                driver.find_elements_by_css_selector('#main-wrap > main > div.analyse__tools > section > div.data > div.explorer-title > button:nth-child(1)')[0].click()
                current_selection = 'Masters'
            load_last_n(-1)
            loop_counter -=1
            continue

        if move == 'test':
            a,b = load_nodes_and_fens()
            Node.all_nodes = a
            Node.fens = b
        current_node.move_(move)
        Node.all_nodes.append(current_node)

        sort_nodes()

        current_node = Node.all_nodes.pop(0)

        get_pos_from_pgn(current_node.pgn,driver = driver,variant = variant)

        try:
            current_node.create_nodes()
        except:
            time.sleep(.001)
            print('slept slept in main loop id2')
            try:
                current_node.create_nodes()
            except:
                time.sleep(1)
                print('slept in main loop id3')
                try:
                    current_node.create_nodes()
                except:
                    raise
        print('CHILDREN of current node: {} '.format(current_node.children))
        # time.sleep(1)
        get_pos_from_pgn(current_node.pgn,driver = driver,variant = variant)
        #time.sleep(2)

        #print(('{:.4f}%'.format((1-current_node.prob)*100)))
        #time.sleep(1)
        read_or_write_to_file(file_name+'_'+str(loop_counter)+'.csv',write = True)
        #pickle_nodes_and_fens()
    except:
        print('\n\n AN ERROR OCCURED \n\n')
        raise
        continue
        # raise
        
