function sayHello() {
    alert("Hello World")
 }
 

function detail(id) {
    // var A="AP01"
    // var B =A+1
    // alert(id),
    // var product_id = Object.freeze(id).product_id;
    // alert('1');
    // alert(typeof(id));
    product_id =id.substring(0,id.length-2),
    // alert(product_id);
    document.getElementById(product_id).style.display = "block";
    // document.getElementById(B).style.display = "none";
    // document.getElementById("myDIV").style.display = "none";
}
function cancel(id){
    // var A="AP01"
    // var B =A+1
    document.getElementById(id).style.display = "none";
}