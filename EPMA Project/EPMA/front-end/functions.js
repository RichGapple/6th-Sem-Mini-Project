function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * 
 charactersLength));
   }
   Kount+=1;
   return(result+String(Kount));
}

function delete_row(x)
{
    x=x.slice(4);
    console.log(x);
    var dModal = M.Modal.getInstance(document.getElementById("modal_delete_row"));
    dModal.open();
    d=db[x]
    document.getElementById("deletion_modal_contents").innerHTML=`
    <table><tr><th>Shape Name</th><th>Shape Dimensions</th><th>Shape ID</th></tr><tr><td class="red-text text-darken-3"><strong>${d.shape_name}</strong></td><td class="red-text text-darken-3"><strong>${d.dimensions}</strong></td><td class="red-text text-darken-3"><strong>${d.id}</strong></td></table>
    <span id="deletion_id" class="h">${d.id}</span>
    `
}

function table_refresh()
{
    tb = document.getElementById("table_body");
    var st="";
    for (var row in db)
    { 
        row=db[row];
        st+=`<tr><td>${row.shape_name}</td><td>${row.dimensions}</td><td>${row.id}</td><td><i id="del_${row.id}" onclick="delete_row(this.id)" class="material-icons red-text text-darken-3 icon_button">delete</i></td></tr>`;
    }
    tb.innerHTML=st;
}