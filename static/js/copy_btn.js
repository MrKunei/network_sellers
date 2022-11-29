const copyBtn = document.querySelector('.copy')

const inputEl = document.querySelector('.to-copy')

copyBtn.addEventListener('click', () =>{
    const inputValue = inputEl.value.trim();
    if (inputValue) {
        navigator.clipboard.writeText(inputValue)
            .then(() =>{
                inputEl.value = '';
                if (writeBtn.innerText !== 'Copied') {
                    const originalText = writeBtn.innerText;
                    writeBtn.innerText = 'Copied';
                    setTimeout(() => {
                        writeBtn.innerText = originalText;
                    }, 1500);
                }
            })
            .catch(err => {
                console.log('Something went wrong', err);
            })
    }
});