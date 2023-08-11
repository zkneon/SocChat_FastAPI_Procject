document.addEventListener("DOMContentLoaded", function(){
        let btn = document.querySelector('button[type=submit]');
        btn.addEventListener('click', async function(event){
            event.preventDefault();
            console.log(document.querySelector('textarea[name=message]').value);


        })
    })

document.addEventListener("DOMContentLoaded", function(){
        let btn = document.querySelector('button[type=submit]');
        btn.addEventListener('click', async function(event){
            event.preventDefault();
            let data = {
                "user_id": Number(document.querySelector('.form.m-2').attributes
                    .getNamedItem('content').value),
                "title": document.querySelector('input[name=title]').value,
                "message": document.querySelector('textarea[name=message]').value,
                };
            let response = await fetch("postfeed/add_post", {
                headers: {"Accept": "application/json", "Content-type": "application/json"},
                method: "POST",
                body: JSON.stringify(data),
            });

            let response_json = await response.json();
            console.log(response);
            console.log(response_json);

            if (response.ok){
                let error_block = document.querySelector('#erorr-msg');
                error_block.style.display = "block";
                error_block.classList.replace("alert-danger", "alert-success")
                error_block.innerHTML = response.statusText;
                setTimeout(() => location.href = "/auth_pages/login", 1000)
            } else {
                let error_block = document.querySelector('#erorr-msg');
                error_block.style.display = "block";
                if (response_json.detail[0]){
                    error_block.innerHTML = response_json.detail[0].msg;
                } else {
                    error_block.innerHTML = response_json.detail.reason;

                }

            }

        })
    })