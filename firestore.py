import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("ServiceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

#post data
doc_ref = db.collection(u'users').document(u'alovelace')
#field of the document
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})

# Then query for documents
users_ref = db.collection(u'parking_spot')
docs = users_ref.get()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
