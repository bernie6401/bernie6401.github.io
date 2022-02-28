document.write("Hello World!");
document.write("<h1>Hello World!</h1>");

//how to use string
var phrase = "Hello SBK";
document.write(phrase);
document.write("<br/>");
document.write(phrase + ' haha');
document.write("<br/>");
document.write(phrase.length);
document.write("<br/>");
document.write(phrase.toLowerCase() + phrase.toUpperCase());
document.write("<br/>");
document.write(phrase.charAt(1));
document.write("<br/>");
document.write(phrase.indexOf('A'));    //-1 means not found
document.write("<br/>");
document.write(phrase.substring(0, 100));
document.write("<br/>");


//how to use number
var num = -6;
document.write(Math.abs(num));
document.write("<br/>");
document.write(Math.max(num, 5, 8, 10, 4545));
document.write("<br/>");
document.write(Math.min(num, 5, 8, 10, 4545));
document.write("<br/>");
document.write(Math.round(-5.22));
document.write("<br/>");
document.write(Math.pow(num, 5));
document.write("<br/>");
document.write(Math.sqrt(-5));
document.write("<br/>");
document.write(Math.random());  //just return a num between 0 and 1, u can times 10 to get a num between 1 and 10
document.write("<br/>");


//make a simple calculator
// var a = Number(prompt("Please enter 1 number."));    //like a input function in python
// var b = Number(prompt("Please enter 1 number."));
/*u also can use parseInt and parseFloat to transfer a string to int or float num*/
// document.write(a + b);
// document.write("<br/>");


//array
var scores = [80, 50, 80, 60 ,22, 48, 4, "hello"];
document.write(scores[7]);
document.write("<br/>");
document.write(scores.length);
document.write("<br/>");


//function
function test1(name)
{
    document.write('hello bros, ' + name);
}
test1('SBK');
document.write("<br/>");
function add(num1, num2)
{
    document.write(num1 + num2);
    return num1 + num2;
}
a = add(5, 8.3);
document.write("<br/>");


//if statement
if (a == 13.3)
{
    document.write('True');
    document.write("<br/>");
}
else if (a > 20)
{
    document.write('False')
    document.write("<br/>");
}
//and --> && / or --> || / not --> !


//object
//like dic data type in python
var person = 
{
    name : 'SBK',
    age : 17,
    is_male: true,

    //u also can write function in object
    print_name:function()
    {
        //this means person object, so u can rewrite it like person.name
        document.write(this.name);
    }
};
person.print_name();


//how to use object
var movie = 
{
    movie_name:"365 Dni",
    director:
    [
        "Barbara Białowąs",
        "Tomasz Mandes"
    ],
    producer:
    [

        "Maciej Kawulski",
        "Ewa Lewandowska",
        "Tomasz Mandes"
    ],	
    starring:
    [
        {
            actor_name:"Anna-Maria Sieklucka",
            age:29,
            is_male:false
        },
        {
            actor_name:"Michele Morrone",
            age:31,
            is_male:true
        },
        {
            actor_name:"Bronisław Wrocławski",
            age:70,
            is_male:true
        },
        {
            actor_name:"Otar Saralidze",
            age:32,
            is_male:true
        },
        {
            actor_name:"Magdalena Lamparska",
            age:34,
            is_male:false
        },
        {
            actor_name:"Natasza Urbańska",
            age:44,
            is_male:false
        }
    ],
    duration:114,
    box_office:"9.5B$"
}
document.write("<br/>");
document.write(movie.director.length);
document.write("<br/>");


//while loop
var i = 1;
while(i<=3)
{
    document.write(i);
    document.write("<br/>");
    i += 1;
}
do
{
    document.write(i);
    document.write("<br/>");
    i += 1;
}while(i<=3)


//password verification process
// var password = 123456;
// var input;
// while(password!=input)
// {
//     input = prompt('Please enter your password!')
// }
// alert('Login successfully');

// var i = 1;
// while(i <= 4)
// {
//     input = prompt('Please enter your password!')
//     if (password != input)
//     {
//         i++;
//         alert("Password is incorrect, please enter again.");
//     }
//     else
//     {
//         alert('Login successfully');
//         break;
//     }
//     if (i == 4)
//     {
//         alert('Unsuccessful 3 times. Fuck u hacker.');
//         break;
//     }
// }


//for loop
for (var i = 0; i < 10; i++)
{
    document.write(i);
    document.write("<br/>");
}


//class template
//"this" is just like "self" key word in python
class Phone
{
    constructor(number, year, is_waterproof)
    {
        this.number = number;
        this.year = year;
        this.is_waterproof = is_waterproof;
    }
    phone_age()
    {
        return 2021 - this.year;
    }
}

var phone1 = new Phone("123", 2020, false);
var phone2 = new Phone("sony XZ1", 2021, true);
var phone3 = new Phone("samsong galaxy s2", 2022, true);

document.write(phone1.is_waterproof);


//how to get html element
//window is a global object and document is a sub-object of window that in charge of manipulating html file
var a_href = document.getElementById("kawaii_bunny")
a_href.href = 'https://google.com';

var text = document.getElementById("id-1");
text.style.color = 'grey';
console.log(a_href)

//u must use id to get the element
var img = document.getElementById("img");
img.width = 50;


//event listener
//u can add this in html file or write in js file

img.addEventListener("click", function()
{
    spec = this.width;
    this.width = spec - 10;
    this.height = spec - 10;
})//"this" means the img element
img.addEventListener("mouseover", function()
{
    this.src = "./img/icon_list.jpg"
})

//write event listener in html file
function handle_click(element)
{
    element.innerText = "Fuck u";
    element.style.color = "red";
}