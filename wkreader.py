# -*- coding: utf-8 -*-
import json
import requests
import re

class wkreader:
    """Reading the WK known kanji/vocab"""
    def __init__(self, api_key):
        self.api = api_key
        self.seen_kanji = 0
        self.known_kanji = 0
        self.__load()
    
    def __load(self):
        """Get known kanji from WK up to user's level"""
        try:
            url = "https://www.wanikani.com/api/user/%s/%s/" % (self.api, 'kanji')
            resp = requests.get(url=url)
            self.data = json.loads(resp.content)
            f = open('kanji_cache.txt', 'w')
            json.dump(self.data, f)
            f.close
        except:
            #API call failed, used cached kanji
            print "Using file data."
            f = open('kanji_cache.txt', 'r')
            self.data = json.load(f)
        self.__index_kanji()

    def __index_kanji(self):
        """Sort kanji by srs level"""
        self.kanji = dict()
        for t in [u'apprentice', u'guru', u'enlighten', u'master',u'burned']:
            self.kanji[t] = set()
        for k in self.data['requested_information']:
            if (k[u'user_specific']):
                self.kanji[k[u'user_specific'][u'srs']].add(k[u'character'])

    def test_sentence(self,sent, threshold=90):
        """Find known kanji by srs level, kick back if sentence is over known threshold"""
        num_kanji = 0
        known_kanji = 0
        for k in re.findall(u'[\u4E00-\u9FFF]', sent, re.UNICODE):
            num_kanji += 1
            if (k in self.kanji['burned']) or (k in self.kanji['enlighten']):
                known_kanji += 1
        if (num_kanji == 0):
            return False;
        self.seen_kanji += num_kanji
        self.known_kanji += known_kanji
        if ((known_kanji / float(num_kanji)) >= (threshold/float(100))):
            return True
#            print "%d/%d: %s" % (known_kanji, num_kanji, sent.encode('utf-8'))

if __name__ == "__main__":
    import sys, getopt, codecs
    infile = ''
    threshold = 90
    api = ''
    pre_context = False
    post_context = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:t:a:bp", ["infile=", "threshold=", "api=", "before", "post"])
    except getopt.GetoptError:
        print 'wkreader.py -a <apikey> -i <inputfile> [-t <threshold>]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'wkreader.py -a <apikey> -i <inputfile> [-t <threshold>]'
            sys.exit()
        elif opt in ('-i', '--infile'):
            infile = arg
        elif opt in ('-t', '--threshold'):
            threshold = int(arg)
        elif opt in ('-a', '--api'):
            api = arg
        elif opt in ('-b', '--before'):
            pre_context = True
        elif opt in ('-p', '--post'):
            post_context = True
    print "File: %s\nAPI Key: %s\nKnown Threshold: %d\nBefore: %r\nPost: %r" % (infile, api, threshold, pre_context, post_context)
    wk = wkreader(api)
    last_line = ''
    last_print = False
    with codecs.open(infile, "r", "utf-8") as f:
        for line in f:
            if post_context and last_print:
                print line.encode('utf-8')
            if wk.test_sentence(line, threshold):
                print '-' * 20
                if pre_context:
                    print last_line.encode('utf-8')
                print line.encode('utf-8')
                last_print = True
            else:
                last_print = False
            last_line = line

    print '-' * 15
    print "Overall: %d / %d" % (wk.known_kanji, wk.seen_kanji)
