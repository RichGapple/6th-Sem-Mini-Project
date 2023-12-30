var socket = io();

socket.on("disconnect",()=>{
    toaster("Server Down & Disconnected","white-text red darken-3 ");
    var btn_li=document.getElementsByClassName("btn");
    for(var i = 0; i < btn_li.length; i++)
        btn_li[i].disabled=true;
    btn_li=document.getElementsByClassName("btn-large");
    for(var i = 0; i < btn_li.length; i++)
        btn_li[i].disabled=true;
    document.getElementById("shopping_list").style.display="None";
    document.getElementById("error_log_div").style.display="block";
    document.getElementById("error_log_span").innerText="Internal Server Disconnected";
    document.getElementById("error_log_button").disabled=false;
});

socket.on("ppp",(status)=>{
    if(status=="Success")
    {
    toaster("Task Completion "+String(status),"white-text green darken-2 ");
    document.getElementById("info_butt").innerHTML = `<strong><span class="material-icons-round">
    file_download
    </span></strong>`;
    document.getElementById("info_butt").classList.remove("red");
    document.getElementById("info_butt").classList.add("green");
    document.getElementById("pybort_button").disabled=true;
    }

    else{
        toaster("Task Failed ","white-text red darken-3");
        document.getElementById("info_butt").innerHTML = `<strong>Process Failed ...</strong>`;
    }
});

socket.on("notification",(data)=>{
    console.log("Notif : ",data);
    toaster(data,"white-text green darken-2 ");
});

socket.on("exception2front",(data)=>{
    console.log("Exception : ",data);
    toaster(data,"white-text red darken-3",false);
    document.getElementById("error_log_div").style.display="block";
    document.getElementById("error_log_span").innerText=data;
    document.getElementById("error_log_button").disabled=false;
});

socket.on("Free Space",(status)=>{
    if(status=="Success")
        toaster("Cache Cleared","green-text white text-darken-2");
    else
        toaster("Cache Clear Failed","white-text red darken-2");
});