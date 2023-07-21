const menubarEl = document.querySelector('#menubar');
const aEls = menubarEl.querySelectorAll('a');
const path = window.location.href

aEls.forEach(el => {
    if (el.href === path) {
        el.parentNode.classList.add("selected");
    }
})