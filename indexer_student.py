# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
"""
import pickle

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0
        
    def get_total_words(self):
        return self.total_words
        
    def get_msg_size(self):
        return self.total_msgs
        
    def get_msg(self, n):
        return self.msgs[n]
        
    # implement
    def add_msg(self, m):
        self.msgs.append(m)
        self.total_msgs += 1
        
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    # implement
    def indexing(self, m, l):
        m_list = m.split()
        
        # remove punctuations and make sure not to remove roman numbers
        for item in m_list:
            if len(m_list) > 1:
                if not item[0].isalpha():
                    item = item[1:]
                elif not item[-1].isalpha():
                    item = item[:-1]
    
        for item in m_list:
            try:
                if l not in self.index[item]:
                    self.index[item].append(l)
            except:
                self.index[item] = [l]
                self.total_words += 1

    # implement: query interface
#'''
#return a list of tupple. if index the first sonnet (p1.txt), then
#call this function with term 'thy' will return the following:
#[(7, " Feed'st thy light's flame with self-substantial fuel,"),
# (9, ' Thy self thy foe, to thy sweet self too cruel:'),
# (9, ' Thy self thy foe, to thy sweet self too cruel:'),
# (12, ' Within thine own bud buriest thy content,')]
#          
#'''         
       
    def search(self, term):
        msgs = []
        # deal with the case when the term is a phrase
        terms = term.split()
        index = set()
        try:
            index.update(self.index[terms[0]])
            for i in terms[1:]:
                index_new = set(self.index[i])
                index = index.intersection(index_new) 
            
            index = list(index)
            index.sort()
            
            for i in index:
                if term in self.msgs[i]:
                    msgs.append( (i, self.msgs[i]) )    
        except:
            pass 
        
        return msgs

class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
        # implement: 1) open the file for read, then call
        # the base class's add_msg_and_index
    def load_poems(self):
        poem_file = open(self.name, 'r')
        poem = poem_file.readlines()
        poem_file.close()
        
        for line in poem:
            self.add_msg_and_index(line.strip())
            
        # each item is one line of the 1st sonnet
    def get_poem(self, p):
        poem = []
        p_roman = self.int2roman[p] + '.'
        index_start = self.index[p_roman][0]
        p_roman_next = self.int2roman[p+1] + '.'
        index_end = self.index[p_roman_next][0]
        
        for i in range(index_start, index_end):
            poem.append(self.msgs[i])
               
        return poem

if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    # the next two lines are just for testing
    p3 = sonnets.get_poem(3)
    s_love = sonnets.search("love")