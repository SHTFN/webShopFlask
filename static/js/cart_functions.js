window.addEventListener('click', function (event) {

    if (event.target.dataset.action === 'plus') {
        // console.log('Plus')
        const counterWrapper = event.target.closest('.counter-wrapper');
        const counter = counterWrapper.querySelector('[data-counter]');
        if (parseInt(counter.innerText) >= 1) {
            counter.innerText = ++counter.innerText
        }
    }

    if (event.target.dataset.action === 'minus') {
        const counterWrapper = event.target.closest('.counter-wrapper');
        const counter = counterWrapper.querySelector('[data-counter]');
        if (parseInt(counter.innerText) > 1) {
            counter.innerText = --counter.innerText
        }
    }
})