import urllib2
from bs4 import BeautifulSoup


from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler



def getURLs(userIn):
	
	#replaced by server #userIn = input('Enter Search Parameter:')

	f = open('/Users/Isaac.Fimbres@ibm.com/Desktop/output.txt','w')

	#From Lynda
	n = 0
	url = 'https://www.lynda.com/search?q=' + userIn
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	url = urllib2.urlopen(req).read()
	soup = BeautifulSoup(url, "html.parser")
	for line in soup.find_all('a'):
		if line.get('href').startswith('https://www.lynda.com/'):
			if n > 0:
				f.write(line.get('href'))
				f.write('\n')
			n = n + 1
			#print(line.get('href'))


	p = 0
	url = 'https://www.ted.com/search?q=' + userIn
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	url = urllib2.urlopen(req).read()
	soup = BeautifulSoup(url, "html.parser")
	for line in soup.find_all('a'):
		if line.get('href').startswith('/read/') or line.get('href').startswith('/talks/') or line.get('href').startswith('/read/'):
			if p > 0:
				f.write('https://www.ted.com' + line.get('href'))
				f.write('\n')
			p = p + 1
			#print(line.get('href'))



	url = 'https://www.coursera.org/courses?languages=en&query=' + userIn + "&userQuery=" + userIn
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	url = urllib2.urlopen(req).read()
	soup = BeautifulSoup(url, "html.parser")
	for line in soup.find_all('a'):
		if line.get('href').startswith('/learn/'):
			#if p > 0:
			f.write('https://www.coursera.org'+ line.get('href'))
			f.write('\n')
			#print(line.get('href'))
			#p = p + 1
			#print(line.get('href'))
	f.close()

	##DB STUFF


	from cloudant.client import Cloudant
	from cloudant.error import CloudantException
	from cloudant.result import Result, ResultByKey


	client = Cloudant("ae11f357-074c-42ec-88c0-d46fd1dbc8c8-bluemix", "1d9351f791650b12e456f49ed45005b03944e40e4be6066057450e616cb8382c", url="https://ae11f357-074c-42ec-88c0-d46fd1dbc8c8-bluemix:1d9351f791650b12e456f49ed45005b03944e40e4be6066057450e616cb8382c@ae11f357-074c-42ec-88c0-d46fd1dbc8c8-bluemix.cloudant.com")
	client.connect()

	databaseName = "urls"

	try :
		client.delete_database(databaseName)
	except CloudantException:
		print "There was a problem deleting '{0}'.\n".format(databaseName)
	else:
		print "'{0}' successfully deleted.\n".format(databaseName)

	databaseName = "urls"

	myDatabase = client.create_database(databaseName)

	if myDatabase.exists():
	   print "'{0}' successfully created.\n".format(databaseName)


	#Read file and put into sample data
	with open("/Users/Isaac.Fimbres@ibm.com/Desktop/output.txt", "r") as ins:
		sampleData = []
		for line in ins:
			sampleData.append(line)
		
		

	#sampleData = [
	#    [1, "one", "boiling", 100],
	#    [2, "two", "hot", 40],
	#    [3, "three", "warm", 20],
	#    [4, "four", "cold", 10],
	#    [5, "five", "freezing", 0]
	#]

	# Create documents using the sample data.
	# Go through each row in the array
	for document in sampleData:
		# Retrieve the fields in each row.
		url = document

		# Create a JSON document that represents
		# all the data in the row.
		jsonDocument = {
			"url" : url,
			#"name" : website,
		}

		# Create a document using the Database API.
		newDocument = myDatabase.create_document(jsonDocument)

		# Check that the document exists in the database.
		if newDocument.exists():
			print "Document '{0}' successfully created.".format(url)

	f = open('/Users/Isaac.Fimbres@ibm.com/Desktop/output.json','w')

	result_collection = Result(myDatabase.all_docs, include_docs=True)

	# "Retrieved full document:\n{0}\n".format(result_collection[0])
 
	f.write("[")

	for result in result_collection:
		f.write('"'+str(result)+'"')
		f.write(",\n")
	f.write('""')
	f.write("]")
	

	#end_point = '{0}/{1}'.format("<url>", databaseName + "/_all_docs")
	#params = {'include_docs': 'true'}
	#response = client.r_session.get(end_point, params=params)
	#print "{0}\n".format(response.json())
	
	f.close()
	f = open('/Users/Isaac.Fimbres@ibm.com/Desktop/output.json','r')
	jsonURLs = f.read()
	f.close()
		
	try :
		client.delete_database(databaseName)
	except CloudantException:
		print "There was a problem deleting '{0}'.\n".format(databaseName)
	else:
		print "'{0}' successfully deleted.\n".format(databaseName)

	client.disconnect()
	
	return jsonURLs


class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/json")
		self.end_headers()
		#write to wfile (response)
		self.wfile.write(getURLs(self.path))
		
def main():
	PORT = 8000
	server = HTTPServer(('', PORT), RequestHandler)
	server.serve_forever()
	
if __name__=="__main__":
	main()

