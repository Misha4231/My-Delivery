document.addEventListener('DOMContentLoaded', function(){

    function addressAutocomplete(containerElement, callback,options){
        const inputContainerElement = document.createElement('div')
        inputContainerElement.setAttribute('class','input-container')
        containerElement.appendChild(inputContainerElement)

        const inputElement = document.createElement('input')
        inputElement.setAttribute('type','text')
        inputElement.setAttribute('name','address')
        inputElement.setAttribute('placeholder', options.placeholder)
        inputContainerElement.appendChild(inputElement);
        
        const MIN_ADDRESS_LENGTH = 3;
        const DEBOUNCE_DELAY = 300;

        let currentTimeout;
        let currentPromiseReject;
        var currentItems
        let focusedItemIndex

        function setActive(items, index){
            if (!items || !items.length) return false

            for(var i=0;i<items.length;i++){
                items[i].classList.remove('autocomplete-active')
            }
            
            items[index].classList.add('autocomplete-active')
            inputElement.value = currentItems[index].formatted
            callback(currentItems[index])
        }

        inputElement.addEventListener('keydown', function(e){
            var autocompleteItemsElement = containerElement.querySelector('.autocomplete-items')
            if (autocompleteItemsElement){
                var itemElement = autocompleteItemsElement.getElementsByTagName('div')
                if (e.keyCode == 40){
                    e.preventDefault()
                    focusedItemIndex = focusedItemIndex !== itemElement.length -1 ? focusedItemIndex +1:0
                    setActive(itemElement, focusedItemIndex)
                } else if(e.keyCode == 38){
                    e.preventDefault()
                    focusedItemIndex = focusedItemIndex !== 0 ? focusedItemIndex - 1 : focusedItemIndex = (itemElement.length -1)
                    setActive(itemElement, focusedItemIndex)
                } else if (e.keyCode == 13){
                    e.preventDefault()
                    if (focusedItemIndex > -1){
                        closeDropDownList()
                    }
                }
            } else{
                if (e.keyCode == 40){
                    var event = document.createElement('Event')
                    event.initEvent('input',true,true)
                    inputElement.dispatchEvent(event)
            }
        }
        })
        

        inputElement.addEventListener('input', function(e){
            const currentValue = this.value

            if (currentTimeout){
                clearTimeout(currentTimeout)
            }

            if (currentPromiseReject){
                currentPromiseReject({
                    canceled: true
                })
            }

            if(!currentValue || currentValue.length < MIN_ADDRESS_LENGTH){
                return false
            }

            currentTimeout = setTimeout(() => {
                currentTimeout = null

                const promise = new Promise((resolve,reject) => {
                    currentPromiseReject = reject
                    const apiKey = '4a156b2543e24639a17a5041e37fe93f'

                    var url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${encodeURIComponent(currentValue)}&format=json&limit=5&apiKey=${apiKey}`;                
                    fetch(url)
                    .then(response => {
                        currentPromiseReject = null

                        if (response.ok){
                            response.json().then(data => resolve(data))
                        } else{
                            response.json().then(data => reject(data))
                        }
                    })
                })

                promise.then((data) => {
                    currentItems = data.results;

                    const autocompleteItemsElement = document.createElement('div')
                    autocompleteItemsElement.setAttribute('class','autocomplete-items')
                    inputContainerElement.appendChild(autocompleteItemsElement)

                    data.results.forEach((result, index) => {
                        const itemElement = document.createElement('div')
                        itemElement.innerHTML = result.formatted
                        autocompleteItemsElement.appendChild(itemElement)
                    
                        itemElement.addEventListener('click', function(e){
                            inputElement.value = currentItems[index].formatted
                            callback(currentItems[index])
                            closeDropDownList()
                        })
                    })

                }, (err) => {
                    if (!err.canceled){
                        console.log(err);
                    }
                })
            },DEBOUNCE_DELAY)
        })
        function closeDropDownList(){
            var autocompleteItemsElements = inputContainerElement.querySelectorAll('.autocomplete-items')
            if (autocompleteItemsElements){
                autocompleteItemsElements.forEach(function(autocompleteItemsElement){
                    inputContainerElement.removeChild(autocompleteItemsElement)
                })
                
            }
            focusedItemIndex = -1
        }

    }

    addressAutocomplete(
        document.getElementById('autocomplete-container'),
        (data) => {
            console.log("Selected option: ");
            console.log(data);
        }, {placeholder:"Enter an address here"})
})