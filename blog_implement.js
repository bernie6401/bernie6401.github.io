//blog implement
var title = document.getElementById("title");
var content = document.getElementById("content");
var btn1 = document.getElementById("btn1");
var list = document.getElementById("list");

btn1.addEventListener("click", function()
{
    if(title.value != "" && content.value != "")
    {
        list.innerHTML = list.innerHTML + 
        `
        <div class="article">
            <br/>
            <h2>Post Title: ${title.value}</h2>
            <p>Content: ${content.value}</P>
            <br/>
            <hr/>
        </div>
        `;
        title.value = "";
        content.value = "";
    }

    else
    alert('Please enter something!!!');

    console.log(title.value, content.value);
})