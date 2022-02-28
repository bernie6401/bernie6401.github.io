//blog implement
var title = document.getElementById("title");
var content = document.getElementById("content");
var btn1 = document.getElementById("btn1");
var list = document.getElementById("list");

btn1.addEventListener("click", function()
{
    list.innerHTML = list.innerHTML + 
    `
    <div class="article">
        <h2>${title.value}</h2>
        <p>${content.value}</P>
    </div>
    `;
    title.value = "";
    content.value = "";
})