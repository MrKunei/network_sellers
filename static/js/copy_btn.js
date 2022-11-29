let copyText = document.getSelection('.copy-mail');
copyText.querySelector("input").addEventListener("click", function(){
    let input = copyText.querySelector("text");
    input.select();
    document.execCommand("copy");
    copyText.classList.add("active");
    window.getSelection().removeAllRanges();
    setTimeout(function (){
        copyText.classList.remove("active");
    },2500);
});