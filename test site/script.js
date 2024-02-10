function makebid(){
    var bid = document.getElementById('bid').value;
    
}
function searchcompany(){
    var company = document.getElementById('company').value;
    var url = 'https://www.google.com/search?q=' + company;
    window.open(url, '_blank');

}

//add event listener for dom 
document.addEventListener('DOMContentLoaded', function (){}) 
{
    document.getElementById('makebid').addEventListener('click', makebid);
}