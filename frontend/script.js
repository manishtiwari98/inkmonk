
if (localStorage.getItem('isLogin') == 'true'){

$.post("http://127.0.0.1:8000/items/",
        {
            authToken : localStorage.getItem('authToken')
        },
        function(data,status){
            if (!data.isVerified){
                localStorage.setItem("isLogin","false");
                window.location.assign("login.html");
            }
            r=data.items;
            console.log(r);

            headRow=document.getElementById('tableHeading');
            tableBody=document.getElementById('tBody');
            var count=0;
            for (name in r[0]) {
                headRow.innerHTML+="<th>" + name +"</th>";
            }
            headRow.innerHTML+="<th>Add Units</th>";
            for (i=0;i< r.length ; i++){
                row=tableBody.insertRow(i);
                row.setAttribute("id","tr"+r[i]['id']);
                for (key in r[i]) {
                    if( key == "id"){
                        row.innerHTML+="<td> SKU-" + r[i][key] +"</td>"
                    }
                    else{
                        row.innerHTML+="<td>" + r[i][key] +"</td>"
                    }
                }
                row.innerHTML+="<td><button type='button' onclick='add(this)'> Add </button></td>";
                
            }
        });
}
else {
    window.location.assign("login.html");
}


function load() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://127.0.0.1:8000/items/");
    xhttp.onload =function(){
    r=xhttp.responseText;
    r=JSON.parse(r);
    document.getElementById("test").innerHTML =   r[0].name;
    }
    xhttp.send();
}


function add(elem){
    rowId=parseInt(elem.parentNode.parentNode.id.slice(2));
    num=prompt("Enter the units to be added of "+ r[rowId -1 ].name + ":");
    num=parseInt(num);
    if(!isNaN(num)){
        $.post(
            'http://127.0.0.1:8000/items/update',
            {   
                'itemId':rowId,
                'noofunits':num,
                'authToken':  localStorage.getItem('authToken')        
            },
            function(data,status){
                if(data.isUpdated){
                    col=document.getElementById('tr'+ rowId).cells[9];
                    col.innerHTML=data.newVal;
                }
            }

        );
    }
    else alert("Please enter valid value");

}
$(document).ready(function(){

$('#txt-search').keyup(function(){
    var searchField = $(this).val();
    if(searchField === '')  {
        $('#filter-records').html('');
        return;
    }
    
    var regex = new RegExp(searchField, "i");
    var output = '<table class="table">';
    var count = 1;
      $.each(r, function(key, val){
        if ((val.name.search(regex) != -1) || (val.description.search(regex) != -1)) {
          output+='<tr id="rw'+val.id +'">';
          output+='<td>'+val.name + '</td>' + '<td>'+val.priceperunit + '</td>' + '<td>'+val.oneUnitQuantity + ' ' + val.measuredIn +'</td>';
          output+='<td>' + '<input type="number" class="input-sm" id="ip'+ val.id + '"  value=0>' + '</td>'
          output+='<td>'+ '<button type="submit" onclick="select(this)"> Add </button>'  +'</td>'
          output+='</tr>'
        }
      });
      output += '</table>';
      $('#filter-records').html(output);
    });
});
var order=[];
function select(elem){
    elem=elem.parentNode.parentNode;
    id=parseInt(elem.id.slice(2));
    noofunits=parseInt(document.getElementById("ip"+id).value);
    order.push({'id':id,'noofunits':noofunits});
    val=r[id -1 ];
    output="<tr>";
        output+="<td>" + val.name + "</td>";
        output+="<td>" + val.priceperunit + "</td>" ;
        output+="<td>"+val.oneUnitQuantity + ' ' + val.measuredIn +"</td>";
        output+="<td>" + noofunits + "</td>";
        totalcost= parseInt(val.priceperunit) * noofunits;
        output+="<td>" +  totalcost + "</td>";
    output+="</tr>";
    
    document.getElementById("selected-objects").innerHTML+=output;
    
    
    
    elem.remove();
}

function disable(){
    modal=document.getElementById("invoiceModal");
    modal.style.display ="none";
    document.getElementById("selected-objects").innerHTML='';
    $("#nameField").val('');
    $("#mobField").val('');

}
function send(){

     

    $.post("http://127.0.0.1:8000/items/createInvoice/",
        {
            data : JSON.stringify(order),
            name :$("#nameField").val(),
            mob  : $("#mobField").val()
        },
        function(data,status){
            modal=document.getElementById("invoiceModal");
            modalContent=document.getElementById("invoice");
            document.getElementById("invoiceId").innerHTML=data.invoiceId;
            document.getElementById("totAmt").innerHTML=data.totAmt;
            modalContent.innerHTML+= document.getElementById("shopItems").innerHTML;
            modalContent.innerHTML+="<button onclick=disable();> DONE </button>"
            modal.style.display ="block";

        });
    
    

}