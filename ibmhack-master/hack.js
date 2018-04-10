function searchFunction() {


	//////////////////////////////////// THIS IS WHERE THE MAGIC HAPPENS BRUHH
	var _search = function(args) {
		var results = document.getElementById("searchResults");
		var searchInput =  document.getElementById("searchText");
		while (results.firstChild) {
		    results.removeChild(results.firstChild);
		}

		_addResult(searchInput, 'http://www.google.com', 'dsfdsafdsafdsa');
	}
	////////////////////////////////////////////////////////////////////////

	var _addResultHidden = function(args) {
		var input = args.input;
		var results = document.getElementById("searchResults");

		var newEntry = document.createElement('div');
		newEntry.className = "search-result";


		var h3 = document.createElement('h3');
		var a = document.createElement('a');
		a.href = args.directLink; 
		a.innerHTML = input.value;
		a.target='_blank';
		h3.appendChild(a);

		newEntry.appendChild(h3);

		a = document.createElement('a');
		a.className = 'search-link';
		a.href= '#';
		a.target='_blank';
		a.innerHTML = args.webLink;

		newEntry.appendChild(a);

		p = document.createElement('p');
		p.innerHTML = args.p;

		newEntry.appendChild(p);
		
		results.appendChild(newEntry);

		var line = document.createElement('div');
		line.className = "hr-line-dashed";
		results.appendChild(line);
	}


	var _addResult = function(title, link, description) {
		var arg = {
			input: title,
			directLink: link,
			webLink: link,
			p: description
		};

		_addResultHidden(arg);
	}

	//// BUTTON SETUP
	var button = document.getElementById("searchButton");

	button.addEventListener('click', _search);
	button.onclick = function(){
		console.log(document.getElementById("searchText").value);
		getData(document.getElementById("searchText").value);
	}

	document.getElementById("searchText").addEventListener("keyup", function(event) {
	    event.preventDefault();
	    if (event.keyCode === 13) {
	        document.getElementById("searchButton").click();
    }
});
}



document.addEventListener("DOMContentLoaded", function(event){
	searchFunction();
});

function getData(key) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		document.getElementById("ready").innerHTML = this.responseText;
	};
	xhttp.open("GET", "http://127.0.0.1:8000/" + key , true);
	xhttp.send();
}