var formInputsAll = document.querySelectorAll('.auth-form-input')

formInputsAll.forEach(function(formInput){
    formInput.addEventListener('input', handleInputChange)
})


function handleInputChange(event){
    var allInputsHaveValue
    formInputsAll.forEach(function(formInput){
        if(formInput.value){
            allInputsHaveValue = true;
        } else{
            allInputsHaveValue = false;

            return
        }
    })
    if(allInputsHaveValue){
        document.querySelector('.auth-submit-button').style.backgroundColor = '#e7a043'
    } else{
        document.querySelector('.auth-submit-button').style.backgroundColor = '#7e7e7e'
    }
    
}