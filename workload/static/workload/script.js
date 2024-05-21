document.querySelector('.filter').addEventListener('click',()=>{
    document.querySelector('.form_filter').classList.remove('hidden');
    document.querySelector('.blur').classList.remove('hidden');
})

document.querySelector('.cancel').addEventListener('click',()=>{
    document.querySelector('.form_filter').classList.add('hidden');
    document.querySelector('.blur').classList.add('hidden');
    
})

document.querySelector('.submit_close').addEventListener('click',()=>{
    document.querySelector('.form_filter').classList.add('hidden');
    document.querySelector('.blur').classList.add('hidden');
})

