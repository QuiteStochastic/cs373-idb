var result;
var request = new XMLHttpRequest();
 
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status == 200) {
            result = this.responseText; 
        }
    };

// Handle requests to Valar Morghulis API
function get_data(attr) {
    request.open('GET', 'http://valar-morghulis.charuri.me/api/' + attr, false);
    request.send();
    return result;  
}

function get_one(attr, id) {
    request.open('GET', 'http://valar-morghulis.charuri.me/api/' + attr + '/' + id, false);
    request.send();
    return result;  
}

// Handle requests to Pythians API
function pythian_get(attr) {
  request.open('GET', 'http://104.239.139.162/scrape/' + attr, false);
  request.send();
  console.log("herp a derp" + result);
  return result;
}

// Handle requests to GitHub API
function get_commits() {
    request.open('GET', 'https://api.github.com/repos/QuiteStochastic/cs373-idb/stats/contributors',false);
    request.send();
    return result;  
}

function get_issues() {
    request.open('GET', 'https://api.github.com/repos/QuiteStochastic/cs373-idb/issues',false);
    request.send();
    return result;  
}
