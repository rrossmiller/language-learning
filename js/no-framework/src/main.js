import './index.css'
let times = 0
// const btn_div = document.querySelector("#btn_div")
// btn_div.innerHTML = `
// <button class="btn w-64 rounded-full" id="btn">Button</button>
// <button class="btn w-64 rounded-full" id="reset">Reset</button>
// `

const btn = document.querySelector("#btn")
const reset = document.querySelector("#reset")
btn.addEventListener('click', () => {
    times += 1
    btn.innerHTML = `Button ${times}`
})

reset.addEventListener('click', () => {
    times = 0
    btn.innerHTML = `Button`
})