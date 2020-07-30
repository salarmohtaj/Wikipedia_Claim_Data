# Load your usual SpaCy model (one of SpaCy English models)
import spacy
nlp = spacy.load('en')

# load NeuralCoref and add it to the pipe of SpaCy's model
import neuralcoref
coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')

# You're done. You can now use NeuralCoref the same way you usually manipulate a SpaCy document and it's annotations.
doc = nlp(u'David Mannes was both a musician and an activist. He believed music to be a universal language, and that it could be used to bridge divides between races and social classes in America.[citation needed]')
print(doc._.coref_resolved)
print(doc._.has_coref)
print(doc._.coref_clusters)
print(doc._.coref_scores)
#span = doc[1:]
#print(span._.is_coref)
#print(span._.coref_cluster.main)
#print(doc._.coref_clusters[1].mentions[-1].start)


import spacy
import neuralcoref
nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)

doc = nlp(u'My sister has a dog. She loves him')

print(doc._.coref_clusters)
print(doc._.coref_clusters[1].mentions)
print(doc._.coref_clusters[1].mentions[-1])
print(doc._.coref_clusters[1].mentions[-1]._.coref_cluster.main)
print("_________")
token = doc[-1]
print(token._.in_coref)
print(token._.coref_clusters)
print("_________")
span = doc[-1:]
print(span._.is_coref)
print(span._.coref_cluster.main)
print(span._.coref_cluster.main._.coref_cluster)
print("_________")