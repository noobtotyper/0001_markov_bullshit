from html.parser import HTMLParser
import random


class MarkovTXTGenerator():
    
    def __init__(self):
        self.mk={}
        self.prev="$" # to start from somwhere
    
    def study(self, filetext):
        with open(filetext, "r") as f:
            for line in f.readlines():
                for w in line.split():
                    a=self.mk.get(self.prev,[])
                    a.append(w)
                    self.mk[self.prev]=a
                    self.prev=w
            # To loop at the end of the chain
            a=self.mk.get(self.prev,[])
            a.append("the")
            self.mk[self.prev]=a
            self.prev=w
        return self.mk

    def burn(self,b=100):
        for _ in range (b):
            current=random.choice(self.mk[self.prev])
            self.prev=current
        return current

    def next(self, n=1, as_list=False):
        bs_words=[self.prev]
        for _ in range (n):
            bs_words.append(random.choice(self.mk[self.prev]))
            self.prev=bs_words[-1]
        if as_list:
            return bs_words
        else:
            return " ".join(bs_words)




class BullshitHTMLParser(HTMLParser):
    def add_mk(self, mk):
        self.mk=mk
    def handle_starttag(self, tag, attrs):
        print(f"<{tag}>",end='')
        
    def handle_endtag(self, tag):
        print(f"</{tag}>",end=' ')
        
    def handle_data(self, data):
        #print(len(data)) #to check that data counts chars
        print(self.mk.next(len(data)//5,as_list=False),end=' ') # sneaky division by 5 to account for avg word length
 

def main(corpus="fakecorpus.txt"):
    mk=MarkovTXTGenerator()
    mk.study(filetext=corpus)
    mk.burn()
    parser = BullshitHTMLParser()
    parser.add_mk(mk)

    with open ("MyArticle.html") as f:
        parser.feed("".join([lines for lines in f.readlines()]))

main()