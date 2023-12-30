document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('select');
  var instances = M.FormSelect.init(elems);
});

function toaster(data,classes="",rounded=true)
{
  if(rounded)
    M.toast({html: "<strong>"+data+"</strong>", classes: 'rounded '+classes ,displayLength:1500});
  else
    M.toast({html: "<strong>"+data+"</strong>", classes: classes ,displayLength:1500});
}