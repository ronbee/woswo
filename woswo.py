import argparse
import collections
import itertools

class InxnI(object):		
	def __init__(self):
		self.inx = collections.defaultdict(list)		

	def __setitem__(self, id, feats):
		for k,v in feats.iteritems():
			self.inx[k].append( (id, v) )

	def __getitem__(self, feats):
		aux = collections.defaultdict(int)		
		norm = 0.0
		for k,v in feats.iteritems():
			for t,w in self.inx[k]:				
				val = v * w
				aux[ t ] += val
				norm += val
		return map( lambda x: (x[0],x[1]/norm) ,  sorted(aux.iteritems(), key=lambda x: - x[1]) )


class WOsWO(object):
	def __init__(self, db=[]):
		self.inx = InxnI()
		for tok in db:
			self.inx[ " ".join(tok) ] = self.feat(tok)

	def __getitem__(self, query):
		return self.inx[ self.feat( [ query ] ) ]

	def combi(self,s):
		pref = map( lambda x: s[0: x+1], range( len(s) ) )
		aux = {}
		for x in ( pref ):
			aux.setdefault(x,0)
			aux[ x ] += 1
		return aux

	def cross( self,fs1,fs2,agg={} ):		
		for k1,v1 in fs1.iteritems():
			for k2,v2 in fs2.iteritems():
				agg[ k1+k2 ] = v1+v2
				agg[ k2+k1 ] = v1+v2

		return agg

	def feat( self, tokens_list ):
		fdic = collections.defaultdict(int)
		combis = map( lambda s: self.combi(s), tokens_list)

		for ii in range(len(combis)):
			for k,v in combis[ii].iteritems():
				fdic[ k ] += v				
			for other in combis[ (ii+1):len(combis) ]:
				self.cross( combis[ii], other, fdic )			
				
		return fdic


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", dest="filename", required=True, help="string db file", metavar="FILE")
	parser.add_argument("-q", "--query", dest="query", required=True, help="query string", metavar="QUERY")
	args = parser.parse_args()
	
	agg = []
	for line in file(args.filename):
		agg.append( line.lower().split() )

	woswo = WOsWO( agg )

	print "-- query: %s --" % args.query.lower()
	for rr in woswo[ args.query.lower() ]:
		print "%s (%f)" % rr
	print "--"

if __name__ == '__main__':
	main()