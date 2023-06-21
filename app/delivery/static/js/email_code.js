var code;

document.querySelector('#email-sender-button').addEventListener('click', function(event){
    var email = document.querySelector('#email-input').value
    if (email){
        var url = '/customer/give_email_code/'
        var csrftoken = getCookie('csrftoken')
        fetch(url,{
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({send_email: email})
        }).then(response => response.json()).then(data => {
            code = data.code
        })

    } else{
        document.querySelector('#specify-email-error').textContent = ' - You should specify email'
    }
})

