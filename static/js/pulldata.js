var result;

function get_data(attr) {
var Request = new XMLHttpRequest();
 
    Request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status == 200) {
            console.log('Status:', this.status);
            console.log('Headers:', this.getAllResponseHeaders());
            console.log('Body:', this.responseText);
            result = this.responseText; 
        }
    };

    Request.open('GET', 'http://private-e1914-valarmorghulis.apiary-mock.com/api/'+attr,false);
    Request.send();
    return result;  
}



