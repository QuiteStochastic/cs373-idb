var result;    

function get_characters() {
var Request = new XMLHttpRequest();
 
 Request.onreadystatechange = function () {
  if (this.readyState === 4 && this.status == 200) {
    console.log('Status:', this.status);
    console.log('Headers:', this.getAllResponseHeaders());
    console.log('Body:', this.responseText);
    result = this.responseText; 
}
};

Request.open('GET', 'http://private-a36489-got2.apiary-mock.com/characters',false);

Request.send();
return result;
}



