const buttons = document.querySelectorAll('.copy-btn')
const copyTexts = document.querySelectorAll('.copy-text')

buttons.forEach((button, index) => {
    button.addEventListener('click', () => {
        const copiedText = copyTexts[index].innerText
        navigator.clipboard.writeText(copiedText)
    })
})
